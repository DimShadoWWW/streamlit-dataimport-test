import streamlit as st
import pandas as pd
import numpy as np

uploaded_file = st.file_uploader('Choose a file')

if uploaded_file is not None:
    st.write(dir(uploaded_file))
    st.write(uploaded_file)
    #read csv
    # df1=pd.read_csv(uploaded_file, type=['csv','xlsx'], accept_multiple_files=False)
    
