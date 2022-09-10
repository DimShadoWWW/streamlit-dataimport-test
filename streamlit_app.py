import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

uploaded_file = st.file_uploader('Choose a file')

dest_columns=['id', 'nombre', 'tipo']
columns_rename = {}

if uploaded_file is not None:
    st.write(dir(uploaded_file))
    st.write(uploaded_file)
    lines = uploaded_file.readlines()[:3]
    df = pd.read_csv(StringIO('\n'.join([l.decode().replace('\n', '') for l in lines])))
    st.write(df)
    st.write(df.columns)
    columns_rename = {c: '' for c in df.columns.tolist()}
    for c in columns_rename.keys():
        columns_rename[c] = st.selectbox(label=c, options=dest_columns)

    st.write(columns_rename)
    
    st.write(df.rename(columns=columns_rename))
    #read csv
    # df1=pd.read_csv(uploaded_file, type=['csv','xlsx'], accept_multiple_files=False)
    
