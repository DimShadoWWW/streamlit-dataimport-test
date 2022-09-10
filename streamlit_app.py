import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

uploaded_file = st.file_uploader('Choose a file')

dest_columns=['id', 'nombre', 'tipo', 'valor']
columns_rename = {}

def new_field(name):
    # st.text_input(name)
    v = st.selectbox(name, key='dynamic_checkbox_{}'.format(name), options=[d for d in dest_columns if d not in columns_rename.keys()])
    if st.checkbox('custom'):
        v = st.text_input('custom name')
    return v

columns_rename = []
# if 'columns_data' not in st.session_state.keys():
#     st.session_state['columns_data'] = columns_data
# else:
#     columns_data = st.session_state['columns_data']

# def checkbox_container(data):
#     st.header('Add renaming of fields')

#     # cols = st.columns(10)
#     if st.button("New", help="Add new rename of columns"):
#         c = str(st.selectbox('Input field name', key='dynamic_checkbox_{}'.format(len(columns_rename.keys())), options=[d for d in df.columns.to_list() if d not in columns_rename.keys()]))
#         columns_rename[c]= new_field(c)

#     # if cols[1].button('Select All'):
#     #     for i in data:
#     #         st.session_state['dynamic_checkbox_' + i] = True
#     #     st.experimental_rerun()
#     # if cols[2].button('UnSelect All'):
#     #     for i in data:
#     #         st.session_state['dynamic_checkbox_' + i] = False
#     #     st.experimental_rerun()
#     # for i in data:
#     #     st.checkbox(i, key='dynamic_checkbox_' + i)

# # def get_selected_checkboxes():
# #     return [i.replace('dynamic_checkbox_','') for i in st.session_state.keys() if i.startswith('dynamic_checkbox_') and st.session_state[i]]


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
    i = st.selectbox('Input field name', key='dynamic_checkbox_{}'.format(len(columns_rename.keys())), options=[d for d in df.columns.to_list() if d not in columns_rename.keys()])
    o = new_field(i)
    # cols = st.columns(10)
    if st.button("New", help="Add new rename of columns"):
        columns_rename[str(i)] = str(o)

    st.write(columns_rename)
    
    # st.write(df.rename(columns=columns_rename))
    # #read csv
    # # df1=pd.read_csv(uploaded_file, type=['csv','xlsx'], accept_multiple_files=False)
    # while True:
    #     # c = st.selectbox('Rename field', options=[d for d in dest_columns if d not in columns_rename.keys()])
    #     if st.button("New", help="Add new rename of columns"):
    #         c = st.selectbox('Rename field', options=[d for d in dest_columns if d not in columns_rename.keys()])
    #         columns_rename[str(c)] = new_field(str(c))
        


# checkbox_container(columns_data)
# st.write('You selected:')
# st.write(get_selected_checkboxes())
