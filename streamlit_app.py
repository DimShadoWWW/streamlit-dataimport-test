import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

uploaded_file = st.file_uploader('Choose a file')

dest_columns=['', 'id', 'nombre', 'tipo']
columns_rename = {}

cols = {}
cols[0], cols[1], cols[2] = st.columns(3)

if uploaded_file is not None:
    # st.write(dir(uploaded_file))
    # st.write(uploaded_file)
    lines = uploaded_file.readlines()[:3]
    df = pd.read_csv(StringIO('\n'.join([l.decode().replace('\n', '') for l in lines])))
    st.text('datos originales')
    st.write(df)
    # st.write(df.columns)
    columns_rename = {c: c for c in dict.fromkeys(df.columns.tolist()).keys()}
    v = {}
    cl = 0
    for c in columns_rename.keys():
        if cl > 2:
            cl = 0
        with cols[cl]:
            v[c] = st.selectbox(label=c, options=[d for d in dest_columns if d in dict.fromkeys(df.columns.tolist()).keys() or d not in columns_rename.values()])
            if v[c] is not None and v[c] != '':
                columns_rename[c] = v[c]
        cl = cl + 1

    st.text('renombrado de columns')
    st.json(columns_rename)
    
    st.text('datos renombrados')
    st.write(df.rename(columns=columns_rename))
    #read csv
    # df1=pd.read_csv(uploaded_file, type=['csv','xlsx'], accept_multiple_files=False)
    
