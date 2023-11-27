from __future__ import absolute_import, unicode_literals
import os
import sys
import io
import json
import streamlit as st
import sqlglot
from pathlib import Path
from PIL import Image
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from travel.util import connect_util, validation_util

TEXT_INPUT_KEY = 0

icon = None
try:
    icon = Image.open('icon.png')
except:
    pass

st.set_page_config(
    page_title="ClickZetta Batch Validation Tool",
    layout="wide",
    page_icon=icon,
    initial_sidebar_state="collapsed",
    menu_items={
        'About': 'https://github.com/clickzetta/clickzetta-travel'
    }
)

DEFAULT_SRC = 'doris'
dialects = [e.value for e in sqlglot.Dialects if e.value]
input_table_type = ['csv', 'text_input']

if 'VOLUME' in os.environ: # for docker
    vol = os.environ['VOLUME']
    for path in ['conf']:
        src = f'{vol}/{path}'
        if not os.path.exists(src):
            os.mkdir(src)
        if not os.path.exists(path):
            os.symlink(src, path)
else:
    for path in ['conf']:
        if not os.path.exists(path):
            os.mkdir(path)

def save_file(file, folder) -> str:
    if file:
        dest = Path(f"{folder}/{file.name}")
        dest.write_bytes(file.read())
        return f'{folder}/{dest.name}'
    return None

def list_files(folder, filter=None):
    ret = ['']
    files = os.listdir(folder)
    if files:
        files.sort(key=lambda x: os.path.getmtime(f'{folder}/{x}'), reverse=True)
        for f in files:
            if not filter or (filter and f.endswith(filter)):
                ret.append(f'{folder}/{f}')
    return ret

st.title('ClickZetta Batch Validation Tool')
st.subheader('1. Batch Validation Task Name')
validation_task_col = st.columns(2)
validation_task_name = validation_task_col[0].text_input('Validation Task Name', value='', max_chars=50)

st.subheader('2. Select Source and Destination Database')
cols = st.columns(2)
src_db = cols[0].selectbox('source db', dialects, index=dialects.index(DEFAULT_SRC), label_visibility='collapsed')
dest_db = cols[1].selectbox('destination db', ['clickzetta'], index=0, label_visibility='collapsed')

config_col1, config_col2 = st.columns(2)
with config_col1:
    st.write(f'Config {src_db} connection')
    config = None
    if src_db == "mysql" or src_db == "doris" or src_db == "postgres":
        cols = st.columns(2)
        with cols[0].form('source_db', clear_on_submit=True):
            config = st.file_uploader('Upload source config file', type=['json'])
            submitted = st.form_submit_button('Upload')
            if submitted and config is not None:
                uploaded = save_file(config, 'conf')
                st.session_state['source_conf'] = uploaded
        with cols[1]:
            all_confs = list_files('conf')
            idx = 0
            if 'source_conf' in st.session_state:
                idx = all_confs.index(st.session_state['source_conf'])
            st.selectbox('Select existing config file:', all_confs, idx, key='source_conf')
            with st.expander('Config template for MySQL/Doris/Postgres'):
                with open('conf_mysql.template') as f:
                    tmpl = f.read()
                st.code(tmpl, 'json')
        if 'source_conf' in st.session_state and st.session_state['source_conf']:
            with open(st.session_state['source_conf'], 'r') as f:
                config = json.load(f)
            host = config['host']
            port = config['port']
            username = config['username']
            password = config['password']
            database = config['database']
            if src_db == 'mysql' or src_db == 'postgres':
                config = {'host': host, 'port': port, 'user': username,
                          'password': password, 'db_type': src_db, 'database': database}
            elif src_db == 'doris':
                config = {'fe_servers': [host + ':' + port], 'user': username,
                          'password': password, 'db_type': src_db}
            connect_util.source_connection_test(config)
    else:
        # url = st.text_input('URL', value='', key=TEXT_INPUT_KEY + 14)
        st.error('Not supported yet')

with config_col2:
    st.write(f'Config {dest_db} connection')
    cols = st.columns(2)
    with cols[0].form('dest_db', clear_on_submit=True):
        config = st.file_uploader('Upload dest config file', type=['json'])
        submitted = st.form_submit_button('Upload')
        if submitted and config is not None:
            uploaded = save_file(config, 'conf')
            st.session_state['dest_conf'] = uploaded
    with cols[1]:
        all_confs = list_files('conf')
        idx = 0
        if 'dest_conf' in st.session_state:
            idx = all_confs.index(st.session_state['dest_conf'])
        st.selectbox('Select existing config file:', all_confs, idx, key='dest_conf')
        with st.expander('Config template for ClickZetta Lakehouse'):
            with open('conf_cz.template') as f:
                tmpl = f.read()
            st.code(tmpl, 'json')
    if 'dest_conf' in st.session_state and st.session_state['dest_conf']:
        with open(st.session_state['dest_conf'], 'r') as f:
            config = json.load(f)
        service = config['service']
        workspace = config['workspace']
        instance = config['instance']
        vcluster = config['vcluster']
        username = config['username']
        password = config['password']
        schema = config['schema']
        # instance_id = config['instanceId']
        instance_id = None
        if instance_id is None or len(instance_id) == 0:
            # st.text("instanceId is empty, will use the first instanceId")
            instance_id = 0
        config = {'service': service, 'workspace': workspace, 'instance': instance,
                  'vcluster': vcluster, 'username': username, 'password': password, 'schema': schema,
                  'db_type': dest_db, 'instanceId': 300}
        connect_util.destination_connection_test(config)

st.subheader("3. Input Source and Destination Tables")
input_tables_types = st.columns(2)
input_tables_types[0].text('* Please select input table type [1.csv file 2. text input]')
input_table_type_select = input_tables_types[0].selectbox('input table type', input_table_type, index=0, label_visibility='collapsed')
if input_table_type_select == 'csv':
    st.text("*Note: 1. Please align the tables orders of the source table and the destination table in csv files.")

    input_sqls = st.columns(2)
    with input_sqls[0]:
        st.write(f'config {src_db} tables')
        source_sql_col = st.columns(2)
        with source_sql_col[0].form('source_db_tables', clear_on_submit=True):
            src_sql_csv = st.file_uploader('Upload source table csv file', type=['csv'])
            submitted = st.form_submit_button('Upload')
            if submitted and src_sql_csv is not None:
                uploaded = save_file(config, 'table_csv')
                st.session_state['source_table_csv'] = uploaded
        with source_sql_col[1]:
            all_confs = list_files('table_csv')
            idx = 0
            if 'source_table_csv' in st.session_state:
                idx = all_confs.index(st.session_state['source_table_csv'])
            st.selectbox('Select existing table csv:', all_confs, idx, key='source_table_csv')
        if 'source_table_csv' in st.session_state and st.session_state['source_table_csv']:
            with open(st.session_state['source_table_csv'], 'r') as f:
                src_sql_file = csv.reader(f)
                src_tables = []
                for row in src_sql_file:
                    src_tables.append(row[0])
                st.session_state['src_tables'] = src_tables
    with input_sqls[1]:
        st.write(f'config {dest_db} tables')
        dest_sql_col = st.columns(2)
        with dest_sql_col[0].form('dest_db_tables', clear_on_submit=True):
            dest_sql_csv = st.file_uploader('Upload destination table csv file', type=['csv'])
            submitted = st.form_submit_button('Upload')
            if submitted and dest_sql_csv is not None:
                uploaded = save_file(config, 'table_csv')
                st.session_state['dest_table_csv'] = uploaded
        with dest_sql_col[1]:
            all_confs = list_files('table_csv')
            idx = 0
            if 'dest_table_csv' in st.session_state:
                idx = all_confs.index(st.session_state['dest_table_csv'])
            st.selectbox('Select existing table csv:', all_confs, idx, key='dest_table_csv')
        if 'dest_table_csv' in st.session_state and st.session_state['dest_table_csv']:
            with open(st.session_state['dest_table_csv'], 'r') as f:
                dest_sql_file = csv.reader(f)
                dest_tables = []
                for row in dest_sql_file:
                    dest_tables.append(row[0])
                st.session_state['dest_tables'] = dest_tables

elif input_table_type_select == 'text_input':
    st.text("*Note: 1. Please input the full table name, including database name and table name. e.g. db1.table1. \n"
            "      2. Split multiple tables with comma. \n"
            "       3. Please align the tables orders of the source table and the destination table.")
    input_sqls = st.columns(2)
    src_sql = input_sqls[0].text_area('Input source table sql', value='', height=200)
    dest_sql = input_sqls[1].text_area('Input destination table sql', value='', height=200)
    source_tables = []
    destination_tables = []
    for src_table in src_sql.split(','):
        source_tables.append(src_table.strip())
    for dest_table in dest_sql.split(','):
        destination_tables.append(dest_table.strip())
    st.session_state['src_tables'] = source_tables
    st.session_state['dest_tables'] = destination_tables




validation_col1, validation_col2 = st.columns(2)

cols = st.columns(2)
validate_level = ['Basic verification', 'Multidimensional verification', 'Line by line verification']
level = cols[0].selectbox('validation level', validate_level, index=0, label_visibility='collapsed')

validation_enabled = src_sql and dest_sql and 'src_connection' in st.session_state and 'destination_connection' in st.session_state
exe_validation = cols[1].button('Validate', key=TEXT_INPUT_KEY + 16, disabled=not validation_enabled)
if not validation_enabled:
    cols[1].info('finish database configuration to enable validation')

if exe_validation:
    st.subheader("Validation Result")
    if level == 'Basic verification':
        try:
            source_df_result, destination_df_result = validation_util.gen_basic_validation_result(
                st.session_state['src_connection'],
                st.session_state['destination_connection'],
                src_sql, dest_sql)
            validation_util.display_validation_result(source_df_result, destination_df_result)

        except Exception as e:
            st.error(e)

    elif level == 'Multidimensional verification':
        try:
            source_df_result, destination_df_result = validation_util.multidimensional_validation(
                st.session_state['src_connection'],
                st.session_state['destination_connection'],
                src_sql, dest_sql)
            validation_util.display_validation_result(source_df_result, destination_df_result)

        except Exception as e:
            st.error(e)
    elif level == 'Line by line verification':
        try:
            source_df_result, destination_df_result = validation_util.line_by_line_validation(
                st.session_state['src_connection'],
                st.session_state['destination_connection'],
                src_sql, dest_sql)
            validation_util.display_validation_result(source_df_result, destination_df_result)

        except Exception as e:
            st.error(e)
    else:
        st.error('Not supported yet')