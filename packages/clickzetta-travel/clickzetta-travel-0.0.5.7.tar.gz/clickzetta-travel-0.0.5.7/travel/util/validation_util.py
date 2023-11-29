import pandas as pd
import streamlit as st
from migration.connector.destination.base import Destination
from migration.connector.source import Source
from migration.util import validation_util, validation_table_util, validation_partition_table_util

def count_partition_table_validation(source: Source, destination: Destination, source_table: str,
                                     destination_table: str, is_source_filter: bool,
                                     is_dest_filter: bool, source_filter_columns: list,
                                     source_filter_values: list, dest_filter_columns: list, dest_filter_values: list):
    try:
        result_dict = validation_partition_table_util.count_validation(source_table, destination_table,
                                                             source,
                                                             destination, is_source_filter, is_dest_filter,source_filter_columns, source_filter_values,dest_filter_columns, dest_filter_values)
        source_dict = {}
        destination_dict = {}
        source_keys = []
        destination_keys = []
        for key in result_dict:
            if 'source' in key:
                if '_source_' in key:
                    final_key = key.replace('_source_', '_')
                elif 'source_' in key:
                    final_key = key.replace('source_', '')
                source_dict[final_key] = [result_dict[key]]
                source_keys.append(key)
            elif 'destination' in key:
                if '_destination_' in key:
                    final_key = key.replace('_destination_', '_')
                elif 'destination_' in key:
                    final_key = key.replace('destination_', '')
                destination_dict[final_key] = [result_dict[key]]
                destination_keys.append(key)
        d_value = int(result_dict['source_count']) - int(result_dict['destination_count'])
        percentage = d_value / int(result_dict['source_count'])
        source_dict['difference'] = [d_value]
        source_dict['percentage'] = [percentage]
        destination_dict['difference'] = 0
        destination_dict['percentage'] = 0

        source_df = pd.DataFrame.from_dict(source_dict, orient='index')
        destination_df = pd.DataFrame.from_dict(destination_dict, orient='index')
        return source_df, destination_df
    except Exception as e:
        raise e
def count_table_validation(source: Source, destination: Destination, source_table: str, destination_table: str):
    try:
        result_dict = validation_table_util.count_validation(source_table, destination_table,
                                                                                        source,
                                                                                        destination)
        source_dict = {}
        destination_dict = {}
        source_keys = []
        destination_keys = []
        for key in result_dict:
            if 'source' in key:
                if '_source_' in key:
                    final_key = key.replace('_source_', '_')
                elif 'source_' in key:
                    final_key = key.replace('source_', '')
                source_dict[final_key] = [result_dict[key]]
                source_keys.append(key)
            elif 'destination' in key:
                if '_destination_' in key:
                    final_key = key.replace('_destination_', '_')
                elif 'destination_' in key:
                    final_key = key.replace('destination_', '')
                destination_dict[final_key] = [result_dict[key]]
                destination_keys.append(key)

        source_df = pd.DataFrame.from_dict(source_dict, orient='index')
        destination_df = pd.DataFrame.from_dict(destination_dict, orient='index')
        return source_df, destination_df
    except Exception as e:
        raise e
def gen_basic_validation_result(source: Source, destination: Destination, source_query: str, destination_query: str):
    try:
        result_dict = validation_util.basic_validation(source, destination, source_query, destination_query)
        source_dict = {}
        destination_dict = {}
        source_keys = []
        destination_keys = []
        for key in result_dict:
            if 'source' in key:
                if '_source_' in key:
                    final_key = key.replace('_source_', '_')
                elif 'source_' in key:
                    final_key = key.replace('source_', '')
                source_dict[final_key] = [result_dict[key]]
                source_keys.append(key)
            elif 'destination' in key:
                if '_destination_' in key:
                    final_key = key.replace('_destination_', '_')
                elif 'destination_' in key:
                    final_key = key.replace('destination_', '')
                destination_dict[final_key] = [result_dict[key]]
                destination_keys.append(key)

        source_df = pd.DataFrame.from_dict(source_dict, orient='index')
        destination_df = pd.DataFrame.from_dict(destination_dict, orient='index')
        return source_df, destination_df
    except Exception as e:
        raise e

def gen_basic_validation_table_result(source: Source, destination: Destination, source_table: str, destination_table: str):
    try:
        result_dict = validation_table_util.basic_validation(source, destination, source_table, destination_table)
        source_dict = {}
        destination_dict = {}
        source_keys = []
        destination_keys = []
        for key in result_dict:
            if 'source' in key:
                if '_source_' in key:
                    final_key = key.replace('_source_', '_')
                elif 'source_' in key:
                    final_key = key.replace('source_', '')
                source_dict[final_key] = [result_dict[key]]
                source_keys.append(key)
            elif 'destination' in key:
                if '_destination_' in key:
                    final_key = key.replace('_destination_', '_')
                elif 'destination_' in key:
                    final_key = key.replace('destination_', '')
                destination_dict[final_key] = [result_dict[key]]
                destination_keys.append(key)

        source_df = pd.DataFrame.from_dict(source_dict, orient='index')
        destination_df = pd.DataFrame.from_dict(destination_dict, orient='index')
        return source_df, destination_df
    except Exception as e:
        raise e

def multidimensional_validation(source: Source, destination: Destination, source_query: str, destination_query: str):
    try:
        source_result, destination_result = validation_util.multidimensional_validation(source_query, destination_query,
                                                                                        source,
                                                                                        destination)
        source_df_result = pd.DataFrame()
        destination_df_result = pd.DataFrame()
        source_df_result['column_name'] = [row[0] for row in source_result]
        source_df_result['column_type'] = [row[1] for row in source_result]
        source_df_result['row_count'] = [row[2] for row in source_result]
        source_df_result['not_null_proportion'] = [row[3] for row in source_result]
        source_df_result['distinct_proportion'] = [row[4] for row in source_result]
        source_df_result['distinct_count'] = [row[5] for row in source_result]
        source_df_result['is_unique'] = [row[6] for row in source_result]
        source_df_result['min_value'] = [row[7] for row in source_result]
        source_df_result['max_value'] = [row[8] for row in source_result]
        source_df_result['avg_value'] = [row[9] for row in source_result]
        source_df_result['stddev_pop_value'] = [row[10] for row in source_result]
        source_stddev_sample_value = []
        for row in source_result:
            if str(row[11]) == 'nan' or str(row[11]) == 'None':
                source_stddev_sample_value.append(None)
            else:
                source_stddev_sample_value.append(row[11])
        source_df_result['stddev_sample_value'] = source_stddev_sample_value

        destination_df_result['column_name'] = [row[0] for row in destination_result]
        destination_df_result['column_type'] = [row[1] for row in destination_result]
        destination_df_result['row_count'] = [row[2] for row in destination_result]
        destination_df_result['not_null_proportion'] = [row[3] for row in destination_result]
        destination_df_result['distinct_proportion'] = [row[4] for row in destination_result]
        destination_df_result['distinct_count'] = [row[5] for row in destination_result]
        destination_df_result['is_unique'] = [row[6] for row in destination_result]
        destination_df_result['min_value'] = [row[7] for row in destination_result]
        destination_df_result['max_value'] = [row[8] for row in destination_result]
        destination_df_result['avg_value'] = [row[9] for row in destination_result]
        destination_df_result['stddev_pop_value'] = [row[10] for row in destination_result]
        destination_stddev_sample_value = []
        for row in destination_result:
            if str(row[11]) == 'nan' or str(row[11]) == 'None':
                destination_stddev_sample_value.append(None)
            else:
                destination_stddev_sample_value.append(row[11])
        destination_df_result['stddev_sample_value'] = destination_stddev_sample_value

        return source_df_result, destination_df_result
    except Exception as e:
        raise e

def multidimensional_validation_table(source: Source, destination: Destination, source_table: str, destination_table: str):
    try:
        source_result, destination_result = validation_table_util.multidimensional_validation(source_table, destination_table,
                                                                                        source,
                                                                                        destination)
        source_df_result = pd.DataFrame()
        destination_df_result = pd.DataFrame()
        source_df_result['column_name'] = [row[0] for row in source_result]
        source_df_result['column_type'] = [row[1] for row in source_result]
        source_df_result['row_count'] = [row[2] for row in source_result]
        source_df_result['not_null_proportion'] = [row[3] for row in source_result]
        source_df_result['distinct_proportion'] = [row[4] for row in source_result]
        source_df_result['distinct_count'] = [row[5] for row in source_result]
        source_df_result['is_unique'] = [row[6] for row in source_result]
        source_df_result['min_value'] = [row[7] for row in source_result]
        source_df_result['max_value'] = [row[8] for row in source_result]
        source_df_result['avg_value'] = [row[9] for row in source_result]
        source_df_result['stddev_pop_value'] = [row[10] for row in source_result]
        source_stddev_sample_value = []
        for row in source_result:
            if str(row[11]) == 'nan' or str(row[11]) == 'None':
                source_stddev_sample_value.append(None)
            else:
                source_stddev_sample_value.append(row[11])
        source_df_result['stddev_sample_value'] = source_stddev_sample_value

        destination_df_result['column_name'] = [row[0] for row in destination_result]
        destination_df_result['column_type'] = [row[1] for row in destination_result]
        destination_df_result['row_count'] = [row[2] for row in destination_result]
        destination_df_result['not_null_proportion'] = [row[3] for row in destination_result]
        destination_df_result['distinct_proportion'] = [row[4] for row in destination_result]
        destination_df_result['distinct_count'] = [row[5] for row in destination_result]
        destination_df_result['is_unique'] = [row[6] for row in destination_result]
        destination_df_result['min_value'] = [row[7] for row in destination_result]
        destination_df_result['max_value'] = [row[8] for row in destination_result]
        destination_df_result['avg_value'] = [row[9] for row in destination_result]
        destination_df_result['stddev_pop_value'] = [row[10] for row in destination_result]
        destination_stddev_sample_value = []
        for row in destination_result:
            if str(row[11]) == 'nan' or str(row[11]) == 'None':
                destination_stddev_sample_value.append(None)
            else:
                destination_stddev_sample_value.append(row[11])
        destination_df_result['stddev_sample_value'] = destination_stddev_sample_value

        return source_df_result, destination_df_result
    except Exception as e:
        raise e


def line_by_line_validation(source: Source, destination: Destination, source_query: str, destination_query: str):
    try:
        result = validation_util.line_by_line_validation(source_query, destination_query, source, destination)
        source_df_result = pd.DataFrame()
        destination_df_result = pd.DataFrame()
        source_result = result['source_result']
        destination_result = result['destination_result']
        columns = result['columns']
        for index, value in enumerate(columns):
            source_df_result[value] = [row[index] for row in source_result]
            destination_df_result[value] = [row[index] for row in destination_result]

        return source_df_result, destination_df_result
    except Exception as e:
        raise e

def line_by_line_validation_table(source: Source, destination: Destination, source_table: str, destination_table: str):
    try:
        result = validation_table_util.line_by_line_validation(source_table, destination_table, source, destination)
        source_df_result = pd.DataFrame()
        destination_df_result = pd.DataFrame()
        source_result = result['source_result']
        destination_result = result['destination_result']
        columns = result['columns']
        for index, value in enumerate(columns):
            source_df_result[value] = [row[index] for row in source_result]
            destination_df_result[value] = [row[index] for row in destination_result]

        return source_df_result, destination_df_result
    except Exception as e:
        raise e

def line_by_line_without_ddl_validation(source: Source, destination: Destination, source_query: str, destination_query: str):
    try:
        result = validation_util.line_by_line_without_ddl_validation(source_query, destination_query, source, destination)
        source_df_result = pd.DataFrame()
        destination_df_result = pd.DataFrame()
        source_result = result['source_result']
        destination_result = result['destination_result']
        if len(source_result) == 0 and len(destination_result) == 0:
            return source_df_result, destination_df_result
        length = len(source_result[0]) if len(source_result[0]) > len(destination_result[0]) else len(destination_result[0])
        for i in range(length):
            source_df_result[f"col_{i}"] = [row[i] for row in source_result]
            destination_df_result[f"col_{i}"] = [row[i] for row in destination_result]

        return source_df_result, destination_df_result
    except Exception as e:
        raise e


def data_diff_table_validation(source: Source, destination: Destination, source_table: str, destination_table: str):
    try:
        diff_result = validation_table_util.data_diff_validation(source_table, destination_table, source, destination)
        return diff_result
    except Exception as e:
        raise e

def schema_table_validation(source: Source, destination: Destination, source_table: str, destination_table: str):
    try:
        diff_result = validation_table_util.schema_validation(source_table, destination_table, source, destination)
        return diff_result
    except Exception as e:
        raise e

def pk_id_table_validation(source: Source, destination: Destination, source_table: str, destination_table: str, pk_id: str):
    try:
        diff_result = validation_table_util.pk_id_column_validation(source_table, destination_table, source, destination, pk_id)
        return diff_result
    except Exception as e:
        raise e

def pk_id_partition_table_validation(source: Source, destination: Destination,
                                     source_table: str, destination_table: str, pk_id: str,
                                     is_source_filter: bool,
                                     is_dest_filter: bool, source_filter_columns: list,
                                     source_filter_values: list, dest_filter_columns: list, dest_filter_values: list):
    try:
        diff_result = validation_partition_table_util.pk_id_column_validation(source_table, destination_table, source, destination, pk_id, is_source_filter, is_dest_filter,source_filter_columns, source_filter_values,dest_filter_columns, dest_filter_values)
        return diff_result
    except Exception as e:
        raise e

def pk_id_validation(source: Source, destination: Destination, source_query: str, destination_query: str, pk_id: str):
    try:
        diff_result = validation_util.pk_id_validation(source_query, destination_query, source, destination, pk_id)
        return diff_result
    except Exception as e:
        raise e

def display_validation_result(source_df_result, destination_df_result):
    try:
        source_result, destination_result = st.columns(2)
        with source_result:
            st.text(st.session_state['src_connection'].name)
            st.table(source_df_result)
        with destination_result:
            st.text(st.session_state['destination_connection'].name)
            st.table(destination_df_result)
        if source_df_result.equals(destination_df_result):
            st.success(
                f'{st.session_state["src_connection"].name} result is equal with {st.session_state["destination_connection"].name} result')
        else:
            st.error(
                f'{st.session_state["src_connection"].name} result is not equal with {st.session_state["destination_connection"].name} result')
            diff_result = source_df_result.compare(destination_df_result, keep_shape=True, keep_equal=True,
                                                   result_names=(st.session_state['src_connection'].name,
                                                                 st.session_state[
                                                                     'destination_connection'].name))
            st.text('difference overview')
            st.table(diff_result)
            st.text('difference results')
            st.table(source_df_result.compare(destination_df_result,
                                              result_names=(st.session_state['src_connection'].name,
                                                            st.session_state[
                                                                'destination_connection'].name)))
    except Exception as e:
        raise e