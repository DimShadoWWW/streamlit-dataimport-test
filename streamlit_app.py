import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

uploaded_file = st.file_uploader('Choose a file')

dest_columns=['id', 'nombre', 'tipo', 'valor']
columns_rename = {}

def new_field(name):
    # st.text_input(name)
    v = st.selectbox(name, options=[d for d in dest_columns if d not in columns_rename.keys()])
    if st.checkbox('custom'):
        v = st.text_input('custom name')
    return v
    

if uploaded_file is not None:
    # st.write(dir(uploaded_file))
    # st.write(uploaded_file)
    lines = uploaded_file.readlines()[:3]
    df = pd.read_csv(StringIO('\n'.join([l.decode().replace('\n', '') for l in lines])))
    st.write(df)
    # st.write(df.columns)
    columns_rename = {}
    # first_column = df.columns.tolist()
    # c: '' for c in df.columns.tolist()}
    # for c in columns_rename.keys():
    #     columns_rename[c] = st.selectbox(label=c, options=dest_columns)

    st.json(columns_rename)
    
    st.write(df.rename(columns=columns_rename))
    #read csv
    # df1=pd.read_csv(uploaded_file, type=['csv','xlsx'], accept_multiple_files=False)
    while True:
        c = st.selectbox('Rename field', options=[d for d in dest_columns if d not in columns_rename.keys()])
        # c = st.selectbox('Rename field', options=[d for d in dest_columns if d not in columns_rename.keys()])
        if st.button("New", help="Add new rename of columns"):
            columns_rename[str(c)] = new_field(str(c))
        
