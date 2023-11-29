import random
import sys
import json
from datetime import datetime
from time import sleep
from migration.connector.source.odps.source import OdpsSource
import travel.util.validation_util as validation_util
from migration.connector.source.mysql.source import MysqlSource
from migration.connector.source.pg.source import PGSource
from concurrent.futures import ThreadPoolExecutor, CancelledError
from migration.connector.destination.clickzetta.destination import ClickZettaDestination
import logging
logging.basicConfig(level=logging.DEBUG)

def _format_job_id():
    unique_id = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    format_unique_id = unique_id.replace('-', '').replace(':', '').replace('.', '').replace(' ', '') \
                       + str(random.randint(10000, 99999))
    return format_unique_id


def write_validation_table_result(source_df_result, destination_df_result, out_path, source_table, destination_table, uid:str):
    print(f'processing {source_table} and {destination_table}')
    try:
        if source_df_result.equals(destination_df_result):
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is equal with {destination_table} result.\n')
        else:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is not equal with {destination_table} result. \n')
            diff_result = source_df_result.sort_index().sort_index(axis=1).compare(destination_df_result.sort_index().sort_index(axis=1),
                                                   result_names=(source_table,
                                                                 destination_table))
            with open(f'{out_path}/{uid}_diff_result.csv', 'a') as f:
                f.write(diff_result.to_csv(index=True))
    except Exception as e:
        raise e

def check_validation(source, destination, source_table, destination_table, out_path, uid, validation_type,
                     check_schema=0, is_source_filter=False, is_dest_filter=False,
                     source_filter_columns=None, source_filter_values=None,
                     dest_filter_columns=None, dest_filter_values=None, pk_column=None):
    source_df_result = None
    destination_df_result = None
    if check_schema:
        check_schema_result = validation_util.schema_table_validation(source, destination, source_table, destination_table)
        only_in_source_cols = check_schema_result['only_in_source_cols']
        only_in_destination_cols = check_schema_result['only_in_dest_cols']
        if len(only_in_source_cols) > 0 or len(only_in_destination_cols) > 0:
            with open(f'{out_path}/{uid}_diff_schema_result.txt', 'a') as f:
                f.write(
                    f'{source_table} has columns {only_in_source_cols} not in {destination_table}.\n')
                f.write(
                    f'{destination_table} has columns {only_in_destination_cols} not in {source_table}.\n')
        return

    if int(validation_type) == 0:
        source_df_result, destination_df_result = validation_util.gen_basic_validation_table_result(source, destination, source_table, destination_table)
    elif int(validation_type) == 1:
        source_df_result, destination_df_result = validation_util.multidimensional_validation_table(source, destination, source_table, destination_table)
    elif int(validation_type) == 2:
        diff_result = validation_util.data_diff_table_validation(source, destination, source_table, destination_table)
        if len(diff_result) == 0:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is equal with {destination_table} result.\n')
        else:
            with open(f'{out_path}/{uid}_result.txt', 'a') as f:
                f.write(
                    f'{source_table} result is not equal with {destination_table} result. \n')

            with open(f'{out_path}/{uid}_diff_result.csv', 'a') as f:
                for line in diff_result:
                    f.write(line)
            return
    elif int(validation_type) == 3:
        source_df_result, destination_df_result = validation_util.count_table_validation(source, destination, source_table, destination_table)
    elif int(validation_type) == 4:
        source_df_result, destination_df_result = validation_util.count_partition_table_validation(
            source, destination, source_table, destination_table, is_source_filter, is_dest_filter,
            source_filter_columns, source_filter_values, dest_filter_columns, dest_filter_values)
    elif int(validation_type) == 5:
        result = validation_util.pk_id_table_validation(source, destination, source_table, destination_table, pk_column)
        only_in_source_table = result['only_in_source_list']
        only_in_destination_table = result['only_in_dest_list']
        if len(only_in_source_table) > 0 or len(only_in_destination_table) > 0:
            with open(f'{out_path}/{uid}_pk_check_result.txt', 'a') as f:
                f.write(
                    f'{source_table} has {only_in_source_table} not in {destination_table}.\n')
                f.write(
                    f'{destination_table} has {only_in_destination_table} not in {source_table}.\n')
        return
    elif int(validation_type) == 6:
        result = validation_util.pk_id_partition_table_validation(source, destination,
                                                                  source_table, destination_table, pk_column,
                                                                  is_source_filter, is_dest_filter,
                                                                  source_filter_columns, source_filter_values,
                                                                  dest_filter_columns, dest_filter_values)
        only_in_source_table = result['only_in_source_list']
        only_in_destination_table = result['only_in_dest_list']
        if len(only_in_source_table) > 0 or len(only_in_destination_table) > 0:
            with open(f'{out_path}/{uid}_pk_check_result.txt', 'a') as f:
                f.write(
                    f'{source_table} has {only_in_source_table} not in {destination_table}.\n')
                f.write(
                    f'{destination_table} has {only_in_destination_table} not in {source_table}.\n')
        return
    elif int(validation_type) == 7:
        source_result, destination_result = validation_util.line_by_line_without_ddl_validation(source, destination, source_table, destination_table)
        with open(f'{out_path}/{uid}_line_by_line_result.txt', 'a') as f:
            only_in_source = set(source_result)-set(destination_result)
            only_in_destination = set(destination_result)-set(source_result)
            f.write(
                f'{source_table} has {only_in_source} not in {destination_table}.\n')

            f.write(
                f'{destination_table} has {only_in_destination} not in {source_table}.\n')
        return
    else:
        raise Exception(f"Unsupported validation type {validation_type}")
    write_validation_table_result(source_df_result, destination_df_result, out_path, source_table, destination_table, uid)

def validate(source, destination, source_tables, destination_tables, validation_type,
             out_path, executor, check_schema=0, is_source_filter=False, is_dest_filter=False,
             source_filter_columns=None, source_filter_values=None, dest_filter_columns=None,
             dest_filter_values=None, pk_column=None):
    if len(source_tables) != len(destination_tables):
        raise Exception("Source tables and destination tables should have the same length")
    uid = _format_job_id()
    try:
        for source_table, destination_table in zip(source_tables, destination_tables):
            executor.submit(check_validation, source, destination, source_table,
                            destination_table, out_path, uid, validation_type,
                            check_schema, is_source_filter, is_dest_filter,
                            source_filter_columns, source_filter_values,
                            dest_filter_columns, dest_filter_values, pk_column)
    except Exception as e:
        raise e


def get_source_connection_params(source_engine_conf):
    if source_engine_conf['db_type'].lower() == 'odps':
        return {
            'id': source_engine_conf['id'],
            'key': source_engine_conf['key'],
            'project': source_engine_conf['project'],
            'endpoint': source_engine_conf['endpoint'],
            'db_type': 'odps',
        }
    host = source_engine_conf['host']
    port = source_engine_conf['port']
    username = source_engine_conf['username']
    password = source_engine_conf['password']
    db_type= source_engine_conf['db_type']
    database = source_engine_conf['database']
    return {
        'host': host,
        'port': port,
        'user': username,
        'password': password,
        'db_type': db_type,
        'database': database,
    }

def get_destination_connection_params(destination_engine_conf):
    service = destination_engine_conf['service']
    workspace = destination_engine_conf['workspace']
    instance = destination_engine_conf['instance']
    vcluster = destination_engine_conf['vcluster']
    username = destination_engine_conf['username']
    password = destination_engine_conf['password']
    if 'schema' in destination_engine_conf:
        schema = destination_engine_conf['schema']
    else:
        schema = None
    instance_id = destination_engine_conf['instanceId']

    return {
        'service': service,
        'workspace': workspace,
        'instance': instance,
        'vcluster': vcluster,
        'username': username,
        'password': password,
        'schema': schema,
        'instanceId': instance_id,
    }

def construct_source_engine(connection_dict: dict):
    db_type = connection_dict['db_type']
    if db_type == 'mysql':
        return MysqlSource(connection_dict)
    elif db_type == 'postgres':
        return PGSource(connection_dict)
    elif db_type == 'odps':
        return OdpsSource(connection_dict)
    else:
        raise Exception(f"Unsupported db type {db_type}")

def construct_destination_engine(connection_dict: dict):
    return ClickZettaDestination(connection_dict)


def get_source_tables(source_tables_file):
    source_tables = []
    with open(source_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            source_tables.append(line.strip())
    return source_tables

def get_destination_tables(destination_tables_file):
    destination_tables = []
    with open(destination_tables_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            destination_tables.append(line.strip())
    return destination_tables


if __name__ == '__main__':
    source_engine_conf = sys.argv[1]
    destination_engine_conf = sys.argv[2]
    source_tables_file = sys.argv[3]
    destination_tables_file = sys.argv[4]
    validation_type = sys.argv[5]
    out_path = sys.argv[6]
    concurrency = int(sys.argv[7])
    check_schema = 0
    is_source_filter = False
    is_dest_filter = False
    source_filter_columns = None
    source_filter_values = None
    dest_filter_columns = None
    dest_filter_values = None
    pk_column = None
    if int(validation_type) == 4:
        is_source_filter = True if int(sys.argv[8]) == 1 else False
        is_dest_filter = True if int(sys.argv[9]) == 1 else False
        if is_source_filter:
            source_filter_columns = sys.argv[10].strip().split(',')
            source_filter_values = sys.argv[11].strip().split(',')
        if is_dest_filter:
            if is_source_filter:
                dest_filter_columns = sys.argv[12].strip().split(',')
                dest_filter_values = sys.argv[13].strip().split(',')
            else:
                dest_filter_columns = sys.argv[10].strip().split(',')
                dest_filter_values = sys.argv[11].strip().split(',')
    if int(validation_type) == 5:
        assert len(sys.argv) == 9
        pk_column = sys.argv[8]

    if int(validation_type) == 6:
        is_source_filter = True if int(sys.argv[8]) == 1 else False
        is_dest_filter = True if int(sys.argv[9]) == 1 else False
        if is_source_filter:
            source_filter_columns = sys.argv[10].strip().split(',')
            source_filter_values = sys.argv[11].strip().split(',')
        if is_dest_filter:
            if is_source_filter:
                dest_filter_columns = sys.argv[12].strip().split(',')
                dest_filter_values = sys.argv[13].strip().split(',')
            else:
                dest_filter_columns = sys.argv[10].strip().split(',')
                dest_filter_values = sys.argv[11].strip().split(',')
        if is_source_filter and is_dest_filter:
            pk_column = sys.argv[14]
        elif is_source_filter and not is_dest_filter:
            pk_column = sys.argv[12]
        elif not is_source_filter and is_dest_filter:
            pk_column = sys.argv[12]
        else:
            pk_column = sys.argv[10]



    try:
        executor = ThreadPoolExecutor(max_workers=concurrency)
        source_engine_conf = json.load(open(source_engine_conf))
        source = construct_source_engine(get_source_connection_params(source_engine_conf))
        destination_engine_conf = json.load(open(destination_engine_conf))
        destination = construct_destination_engine(get_destination_connection_params(destination_engine_conf))
        source_tables = get_source_tables(source_tables_file)
        destination_tables = get_destination_tables(destination_tables_file)
        validate(source, destination, source_tables, destination_tables, validation_type,
                 out_path, executor, check_schema, is_source_filter, is_dest_filter,
                 source_filter_columns, source_filter_values, dest_filter_columns,
                 dest_filter_values, pk_column)
        executor.shutdown(wait=True)
    except Exception as e:
        print('validation error:', e)
        raise e

