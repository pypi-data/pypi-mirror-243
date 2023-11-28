# Databricks notebook source
from sdutilities.acsclient import ACSClient
import os

# COMMAND ----------

api_key = dbutils.secrets.get(scope="acs", key="api_key")

# COMMAND ----------

os.chdir('/Workspace/Users/c-etucker@sdoh.private')

# COMMAND ----------

acs = ACSClient(2021, api_key=api_key)

# COMMAND ----------

acs_cols = ['B01001_001E']

# COMMAND ----------

acs.get_zips(acs_cols, sd_cols=True)
