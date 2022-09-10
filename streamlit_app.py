import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

uploaded_file = st.file_uploader('Choose a file')

dest_columns=['id', 'nombre', 'tipo', 'valor']
columns_rename = {}

def new_field(name):
    # st.text_input(name)
    v = st.selectbox(name, key='dynamic_checkbox_{}'.format(name), options=[d for d in dest_columns if d not in columns_rename.values()])
    if st.checkbox('custom'):
        v1 = st.text_input('custom name')
        return v1
    return v

st.session_state['columns_rename'] = columns_rename
# if 'columns_rename' not in st.session_state.keys():
# else:
#     columns_rename = st.session_state['columns_rename']

if uploaded_file is not None:
    # st.write(dir(uploaded_file))
    # st.write(uploaded_file)
    lines = uploaded_file.readlines()[:3]
    df = pd.read_csv(StringIO('\n'.join([l.decode().replace('\n', '') for l in lines])))
    st.write(df)
    # st.write(df.columns)
    # columns_rename = {}
    # first_column = df.columns.tolist()
    # c: '' for c in df.columns.tolist()}
    # for c in columns_rename.keys():
    #     columns_rename[c] = st.selectbox(label=c, options=dest_columns)

    # checkbox_container(df.columns.tolist())
    
    st.header('Add renaming of fields')
    # cols = st.columns(10)
    if st.button("New", help="Add new rename of columns"):
        i = st.selectbox('Input field name', key='dynamic_checkbox_{}'.format(len(columns_rename.keys())), options=[d for d in df.columns.to_list() if d not in columns_rename.keys()])
        columns_rename[str(i)] = str(new_field(i))

    st.write(columns_rename)

    # st.write(df.rename(columns=columns_rename))
    # #read csv
    # # df1=pd.read_csv(uploaded_file, type=['csv','xlsx'], accept_multiple_files=False)
    # while True:
    #     # c = st.selectbox('Rename field', options=[d for d in dest_columns if d not in columns_rename.keys()])
    #     if st.button("New", help="Add new rename of columns"):
    #         c = st.selectbox('Rename field', options=[d for d in dest_columns if d not in columns_rename.keys()])
    #         columns_rename[str(c)] = new_field(str(c))
        


# checkbox_container(columns_rename)
# st.write('You selected:')
# st.write(get_selected_checkboxes())
