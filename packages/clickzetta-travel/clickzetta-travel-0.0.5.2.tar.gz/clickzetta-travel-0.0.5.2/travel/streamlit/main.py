import streamlit as st
from PIL import Image

icon = None
try:
    icon = Image.open('icon.png')
except:
    pass

st.set_page_config(
    page_title="ClickZetta Travel Web UI",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items = {
        'About': 'https://github.com/clickzetta/clickzetta-travel'
    }
)

st.write("# Welcome to ClickZetta Travel Toolkit")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    ClickZetta Travel is a toolkit including Transpile, Run, And Validate queries, for Evaluating clickzetta with Love.


    - Unify Page: transpile SQL, run SQLs and validate results in one page.
    - AST Viewer: transpile SQL and show ASTs for debug

    **👈 Select a page from the sidebar** to reach your desired purpose.

"""
)