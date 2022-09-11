import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import uuid
import redis
from furl import furl
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TagField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

# st.info('start')
# try:
#     st.info('started')
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
    df = df.rename(columns=columns_rename)
    st.write(df)
    #read csv
    # df1=pd.read_csv(uploaded_file, type=['csv','xlsx'], accept_multiple_files=False)

    if st.button('import'):
        redis_url = furl(st.secrets["redis_url"])

        redisCon = redis.Redis(
            host=redis_url.host,
            port=redis_url.port,
            password=redis_url.password if redis_url.password != '' else None,
            # host='redis',
            # port=6379,
            # host='aqueous-badlands-51618.herokuapp.com',
            # port=80,
            # password='af80e90f144cdd37ae539349ba0bc7a4',
            max_connections=10,
            decode_responses=True,
            retry_on_timeout=True)

        index_name = "idx:data"

        schema = (
            TextField("$.name", as_name="name", sortable=True),
            # TextField("$.middleName", as_name="middleName", sortable=True),
            # TextField("$.lastName", as_name="lastName", sortable=True),
            # TextField("$.shortName", as_name="shortName", sortable=True),
            # TextField("$.nickName", as_name="nickName", sortable=True),
            # TextField("$.side", as_name="side", sortable=True),
            # TextField("$.country", as_name="country", sortable=True),

            NumericField("$.id", as_name="id"),
            # NumericField("$.countryId", as_name="countryId"),
            # NumericField("$.teamId", as_name="teamId"),
            # NumericField("$.currentTeamId", as_name="currentTeamId"),
            # NumericField("$.gamesPlayed", as_name="gamesPlayed", sortable=True),

            # # TagField("$.user.city", as_name="city"),
            # TagField("$.channel", as_name="channel"),
        )

        try:
            ftindex_data = redisCon.ft(index_name)
            ftindex_data.create_index(schema,
                                        definition=IndexDefinition(
                                            prefix=["data:"],
                                            index_type=IndexType.JSON))
        except redis.exceptions.ResponseError:
            pass

        df['uuid'] = [uuid.uuid4().hex for x in range(df.shape[0])]
        df = df.fillna(np.nan).replace([np.nan], [None])
        for index, row in df.iterrows():
            values = row.to_dict()
            st.json(values)
            for k in values.keys():
                print(k, type(values[k]))
            print("data:{id}".format(id=values['uuid']))
            redisCon.json().set("data:{id}".format(id=values['uuid']), '.', values)

# except Exception as e:
#     st.error(e)