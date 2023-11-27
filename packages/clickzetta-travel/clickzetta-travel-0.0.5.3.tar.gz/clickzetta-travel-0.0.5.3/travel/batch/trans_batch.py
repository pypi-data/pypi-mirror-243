import sys
import os
import time
import shutil
import argparse
import sqlglot
from datetime import datetime
from difflib import SequenceMatcher
from travel.util.util import split_sql
from travel.util.config import Config


def main():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    parser = argparse.ArgumentParser(description='transpile sqls and run them')
    parser.add_argument('-c', '--config', type=str, dest='config', default='config.json',
                        help=f'clickzetta lakehouse config file. default: config.json')
    parser.add_argument('-t', '--timeout', type=int, dest='timeout', default=30,
                        help=f'cancel sql if it runs too long. default: 30 seconds')
    parser.add_argument('-s', '--source', type=str, dest='source', default='doris',
                        help=f'sql dialect that transpile from. default: doris')
    parser.add_argument('-o', '--output', type=str, dest='output', default=now,
                        help=f'output folder, stores transpiled sqls and runtime information.')
    parser.add_argument('--stop', type=int, dest='stop', default=0,
                        help=f'stop if too many sqls failed to run. default: 0, means do not stop')
    parser.add_argument('sqlfiles', type=str, nargs='+',
                        help=f'sql fiels to transpile and run.')
    args = parser.parse_args()

    src = args.source
    dest = 'clickzetta'

    try:
        conf = Config(args.config)
    except Exception as ex:
        print(ex)
        sys.exit(1)
    conn = conf.get_cz_conn()
    hints = conf.get_hints()
    hints['hints']['sdk.job.timeout'] = args.timeout

    total = 0
    empty = 0
    trans_ok = 0
    trans_err = 0
    valid = 0
    run_ok = 0
    run_err = 0
    stop_limit = args.stop
    TRANS_ERR = 'failed to transpile'
    SUCCESS = 'success'
    reasons = dict()  # { excpetion: { sql_id ... } }

    def no_longer_than(s: str, length: int = 120) -> str:
        p = f'{s[:116]} ...' if len(s) > length else s
        return p

    def sql2file(prefix, src_sql, src_ex=None, dest_sql=None, dest_ex=None):
        if src_sql:
            with open(f'{prefix}.{src}.sql', 'w') as w:
                w.write(src_sql)
                if src_ex:
                    w.write('\n\n--exception:\n')
                    for l in str(src_ex).split('\n'):
                        w.write(f'-- {l}\n')
        if dest_sql:
            with open(f'{prefix}.{dest}.sql', 'w') as w:
                w.write(dest_sql)
                if dest_ex:
                    w.write(f'\n\n-- exception for job_id: {job_id}\n')
                    for l in str(dest_ex).split('\n'):
                        w.write(f'-- {l}\n')

    print(f'output to {args.output}')
    os.makedirs(args.output, exist_ok=True)
    with conn.cursor() as cursor, open(f'{args.output}/log.txt', 'w') as log_file, open(f'{args.output}/summary.txt',
                                                                                        'w') as summary_file:
        def log(s: str):
            print(s)
            log_file.write(s)
            log_file.write('\n')

        def summary(s: str):
            print(s)
            summary_file.write(s)
            summary_file.write('\n')

        stop = False
        for input in args.sqlfiles:
            if stop:
                break
            log(f'splitting {input} ...')
            with open(input, 'r') as f:
                content = f.read()
            sqls = split_sql(content)
            for q in sqls:
                try:
                    total += 1
                    log(f'transpiling sql {total} ...')
                    s = sqlglot.transpile(q, read=src, write=dest)[0].strip()
                    trans_ok += 1
                except Exception as ex:
                    log(f'failed to transpile sql {total}, reason {ex}')
                    trans_err += 1
                    if TRANS_ERR in reasons:
                        reasons[TRANS_ERR].add(total)
                    else:
                        reasons[TRANS_ERR] = {total}
                    log(no_longer_than(q))
                    sql2file(f'{args.output}/{total}', q, src_ex=ex)
                    continue
                try:
                    if s:
                        if s.lower().startswith('set '):
                            empty += 1
                            log(f'skip query {total}, reason: set, query: {s}')
                            continue
                        valid += 1
                        log(f'executing sql {total} ...')
                        ts = time.time()
                        cursor.execute(f'{s}', parameters=hints)
                        ts = time.time() - ts
                        log('job {} finished in {:.3f} seconds.'.format(cursor.get_job_id(), ts))
                        sql2file(f'{args.output}/{total}', q, dest_sql=s)
                        if SUCCESS in reasons:
                            reasons[SUCCESS].add(total)
                        else:
                            reasons[SUCCESS] = {total}
                        run_ok += 1
                    else:
                        empty += 1
                        log(f'skip query {total}, reason: empty, orig query: {q}')
                except KeyboardInterrupt as ki:
                    log('user interrupted, skip left queries')
                    stop = True
                    break
                except Exception as ex:
                    job_id = cursor.get_job_id()
                    log(f'failed to run sql {total}, job_id: {job_id}, reason {ex}')
                    run_err += 1
                    k = str(ex)
                    if k in reasons:
                        reasons[k].add(total)
                    else:
                        reasons[k] = {total}
                    log(no_longer_than(s))
                    sql2file(f'{args.output}/{total}', q, dest_sql=s, dest_ex=ex)
                    if stop_limit > 0 and run_err >= stop_limit:
                        log(f'{run_err} sql failed, stop.')
                        stop = True
                        break

        if stop:
            summary(f'\nsummary: (use interrupted or too many errs)')
        else:
            summary(f'\nsummary:')
        summary(f'original sql      : {total}')
        if total > 0:
            summary('transpiled        : {}, {:.2f}%'.format(trans_ok, 100.0 * trans_ok / total))
            summary('transpile failed  : {}, {:.2f}%'.format(trans_err, 100.0 * trans_err / total))
        if empty > 0:
            summary(f'empty or set sql  : {empty}')
        summary(f'valid for running : {valid}')
        if valid > 0:
            summary('run succeed       : {}, {:.2f}%'.format(run_ok, 100.0 * run_ok / valid))
            summary('run failed        : {}, {:.2f}%'.format(run_err, 100.0 * run_err / valid))
        if reasons:
            summary('\nclassified failed reasons:')
            if SUCCESS in reasons:
                folder = f'{args.output}/success'
                os.makedirs(folder, exist_ok=True)
                for n in reasons.pop(SUCCESS):
                    shutil.move(f'{args.output}/{n}.{src}.sql', f'{folder}/')
                    shutil.move(f'{args.output}/{n}.{dest}.sql', f'{folder}/')
            if TRANS_ERR in reasons:
                folder = f'{args.output}/trans_fail'
                summary(f'trans_fail\t{len(reasons[TRANS_ERR])}\t{TRANS_ERR}')
                os.makedirs(folder, exist_ok=True)
                for n in reasons.pop(TRANS_ERR):
                    shutil.move(f'{args.output}/{n}.{src}.sql', f'{folder}/')
            # merge similar reasons
            classified = dict()
            for r in reasons.keys():
                for c in classified.keys():
                    if SequenceMatcher(None, r, c).ratio() > 0.9:
                        classified[c] |= reasons[r]
                        break
                else:
                    classified[r] = reasons[r]
            for i, (k, v) in enumerate(sorted(classified.items(), key=lambda item: len(item[1]), reverse=True)):
                folder = f'{args.output}/reason_{i}'
                summary(f'reason_{i}\t{len(v)}\t{k}')
                os.makedirs(folder, exist_ok=True)
                for n in v:
                    shutil.move(f'{args.output}/{n}.{src}.sql', f'{folder}/')
                    shutil.move(f'{args.output}/{n}.{dest}.sql', f'{folder}/')

    if os.path.islink('last'):
        os.unlink('last')
    os.symlink(args.output, 'last')

    conn.close()
