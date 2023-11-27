from __future__ import absolute_import, unicode_literals
import os
import sys
import io
import json
import streamlit as st
import sqlglot
from pathlib import Path
from PIL import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from travel.util import connect_util, validation_util

TEXT_INPUT_KEY = 0

icon = None
try:
    icon = Image.open('icon.png')
except:
    pass

st.set_page_config(
    page_title="ClickZetta Low Touch Tool",
    layout="wide",
    page_icon=icon,
    initial_sidebar_state="collapsed",
    menu_items={
        'About': 'https://github.com/clickzetta/clickzetta-travel'
    }
)

DEFAULT_SRC = 'doris'
dialects = [e.value for e in sqlglot.Dialects if e.value]

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

st.title('ClickZetta Travel Unified Page')

st.subheader('Transpile SQL')
cols = st.columns(2)
src_db = cols[0].selectbox('source db', dialects, index=dialects.index(DEFAULT_SRC), label_visibility='collapsed')
dest_db = cols[1].selectbox('destination db', ['clickzetta'], index=0, label_visibility='collapsed')

cols = st.columns(2)
input_sql = cols[0].text_area(f'Input {src_db} sql here')
transpile_col1, transpile_col2 = st.columns(2)
src_sql = None
dest_sql = None

if input_sql:
    with transpile_col1:
        st.write(src_db)
        try:
            src_sql = sqlglot.transpile(input_sql, read=src_db, write=src_db, pretty=True)[0]
            st.code(src_sql, 'sql', True)
        except Exception as ex:
            st.error(f'failed to format input sql: {ex}')

    with transpile_col2:
        st.write(dest_db)
        try:
            dest_sql = sqlglot.transpile(input_sql, read=src_db, write=dest_db, pretty=True)[0]
            st.code(dest_sql, 'sql', True)
        except Exception as ex:
            st.error(f'failed to transpile input sql: {ex}')

st.subheader("Run SQLs and Validate results")

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