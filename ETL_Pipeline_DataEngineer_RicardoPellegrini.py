#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine

from datetime import datetime


# ## Data Extraction

# In[2]:


# equipments file
df_equip = pd.read_json('Shape-Test/equipment.json')


# In[3]:


# Sample of the equipments table, which is already fine to be loaded into the database
df_equip.head()


# In[4]:


# equipment_sensors file
df_equip_sensors = pd.read_csv('Shape-Test/equipment_sensors.csv', sep=';')


# In[5]:


# Sample of the equipment_sensors table, which is already fine to be loaded into the database
df_equip_sensors.head()


# In[6]:


# equipment_failure_sensors file
df_equip_failure_sensors = pd.read_csv('Shape-Test/equipment_failure_sensors.log',sep='\t', engine='python',header=None)


# In[7]:


# Sample of the equipments table, which needs some transformations before loading it into the database
df_equip_failure_sensors.tail()


# ## Data Transformation

# In[8]:


# datetime_utc field
df_equip_failure_sensors['datetime_utc'] = df_equip_failure_sensors[0].apply(lambda x: x[x.find("[")+1:x.find("]")])
df_equip_failure_sensors['datetime_utc'] = df_equip_failure_sensors['datetime_utc'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))


# In[9]:


# sensor_id field
df_equip_failure_sensors['sensor_id'] = df_equip_failure_sensors[2].apply(lambda x: int(x[x.find("[")+1:x.find("]")]))


# In[10]:


# temperature field
df_equip_failure_sensors['temperature'] = df_equip_failure_sensors[4].apply(lambda x: float((x.split(',')[0]).strip()))


# In[11]:


# vibration field
df_equip_failure_sensors['vibration'] = df_equip_failure_sensors[5].apply(lambda x: float((x[:x.find(")")]).strip()))


# In[12]:


df_equip_failure_sensors.head()


# In[13]:


df_equip_failure_sensors.sort_values(by='datetime_utc', inplace=True)


# In[14]:


df_equip_failure_sensors = df_equip_failure_sensors.iloc[:,6:]


# In[15]:


# Sample of the equipment_failure_sensors table, which now is ready to be loaded into the database
df_equip_failure_sensors.head()


# In[16]:


# Checking if all the data types are correct
df_equip_failure_sensors.dtypes


# In[36]:


# Checking for any null values in the tables
dfs = [df_equip, df_equip_sensors, df_equip_failure_sensors]

is_there_null_values = [df.isnull().any().any() for df in dfs]
is_there_null_values


# ## Data Load (SQL Database - PostgreSQL)

# In[80]:


# Creating the connection to the sql database in PostgreSQL
try:
    conn_string = 'postgres://postgres:ricardo1992@localhost/db_shape'
    db = create_engine(conn_string)
    conn = db.connect()
except:
    print('Database connection not succeeded')


# In[81]:


# Converting the 03 databases into tables in PostgreSQL
try:
    df_equip.to_sql('tb_equipments', con=conn, if_exists='append', index=False)
except:
    print('Not possible to load the values into the table tb_equipments')

try:
    df_equip_sensors.to_sql('tb_equipment_sensors', con=conn, if_exists='append', index=False)
except:
    print('Not possible to load the values into the table tb_equipments')

try:
    df_equip_failure_sensors.to_sql('tb_equipment_failure_sensors', con=conn, if_exists='append', index=False)
except:
    print('Not possible to load the values into the table tb_equipments')


# In[ ]:


# Closing the connection to the database
conn.close()

