import sqlglot
import streamlit as st
from PIL import Image

icon = None
try:
    icon = Image.open('icon.png')
except:
    pass

st.set_page_config(
    page_title="SQLGlot AST Viewer",
    layout="wide",
    page_icon=icon,
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'https://github.com/clickzetta/clickzetta-travel'
    }
)

DEFAULT_SRC = 'doris'
dialects = [e.value for e in sqlglot.Dialects if e.value]

l_input, r_input = st.columns(2)
with l_input:
    st.subheader('Source')
    src_dialect = st.selectbox('dialect', dialects, dialects.index(DEFAULT_SRC))
    input_sql = st.text_area('sql')
with r_input:
    st.subheader('ClickZetta')
    hint = st.empty()

st.divider()
l_sql, r_sql = st.columns(2)

if src_dialect and input_sql:
    try:
        src_sql = sqlglot.transpile(input_sql, read=src_dialect, write=src_dialect, pretty=True)[0]
        l_sql.code(src_sql + ';', 'sql', True)
    except:
        pass

    try:
        cz_sql = sqlglot.transpile(input_sql, read=src_dialect, write='clickzetta', pretty=True)[0]
        r_sql.code(cz_sql + ';', 'sql', True)
        hint.info('transpiled successfully')

        st.divider()
        src_ast = sqlglot.parse_one(input_sql, read=src_dialect)
        cz_ast = sqlglot.parse_one(cz_sql, read='clickzetta')

        # ast_diff = sqlglot.diff(src_ast, cz_ast)
        # st.code(ast_diff, 'lisp')

        l_ast, r_ast = st.columns(2)
        l_ast.code(repr(src_ast), 'lisp', True)
        if cz_sql:
            r_ast.code(repr(cz_ast), 'lisp', True)
    except Exception as ex:
        # a rough impl to turn sqlglot output w/ ansi escaped underline to html red bold
        s = str(ex).replace('\033[4m', '<b style="color:red">')
        s = str(s).replace('\033[0m', '</b>')
        hint.write(f'<pre><span style="font-family: monospace;">{s}</span></pre>', unsafe_allow_html=True)

