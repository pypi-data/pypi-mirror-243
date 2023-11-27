import argparse
from datetime import datetime
import time
import sys
import sqlglot
from travel.util.config import Config

def main():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    parser = argparse.ArgumentParser(description='a sqlglot shell')
    parser.add_argument('-c', '--config', type=str, dest='config', default='config.json',
                        help=f'clickzetta lakehouse config file. default: config.json')
    parser.add_argument('-t', '--timeout', type=int, dest='timeout', default=30,
                        help=f'cancel sql if it runs too long. default: 30 seconds')
    parser.add_argument('-s', '--source', type=str, dest='source', default='doris',
                        help=f'sql dialect that transpile from. default: doris')
    parser.add_argument('-a', '--action', type=str, default='t',
                        help=f'action to perform: "t" transpile only, "a" view ast, "r" transpile and run. default: "t"')
    parser.add_argument('sqlfile', type=str,
                        help=f'file that contains only one sql.')
    args = parser.parse_args()

    src = args.source
    dest = 'clickzetta'
    action = args.action

    try:
        conf = Config(args.config)
    except Exception as ex:
        if action == 'r':
            print(ex)
            sys.exit(1)

    conn = conf.get_cz_conn()
    hints = conf.get_hints()
    hints['hints']['sdk.job.timeout'] = args.timeout

    with open(args.sqlfile, 'r') as f:
        sql = f.read()
        print('-- original sql: --')
        print(sql)

    if action == 'a':
        print('-- ast expression: --')
        print(repr(sqlglot.parse_one(sql, read=src)))
    elif action == 't' or action == 'r':
        trans_sql = sqlglot.transpile(sql, read=src, write=dest)[0]
        print('-- transpiled sql: --')
        print(trans_sql)
        if action == 'r':
            ts = time.time()
            cursor = conn.cursor()
            try:
                cursor.execute(trans_sql, parameters=hints)
                ts = time.time() - ts
                job_id = cursor.get_job_id()
                print('-- execute succeed')
                print(f'-- job_id: {job_id}')
                print('-- duration: {:.3f} seconds'.format(ts))
            except Exception as ex:
                job_id = cursor.get_job_id()
                print('-- execute failed')
                print(f'-- job_id: {job_id}')
                print('-- duration: {:.3f} seconds'.format(ts))
                print(f'-- reason: {ex}')
            finally:
                cursor.close()
    else:
        print(f'unknown action: "{action}"')
        sys.exit(1)
