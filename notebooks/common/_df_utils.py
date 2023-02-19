# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC #### Date Utility Functions

# COMMAND ----------

def timestamp_to_zulu(timestampColumn):
  '''
  This method takes a databricks column of type 'timestamp' and converts it into the desired Zulu string format
  
  input format:  2022-01-01T19:18:16.000+0000  (timestamp)
  return format:  2022-01-01T19:18:16.000Z (string)
  
  Example Use:
  df.select(timestamp_to_zulu("date_created").alias("date_created"))
  '''
  return (F.regexp_replace(F.date_format(timestampColumn, "yyyy-MM-dd'T'HH:mm:ss.SSSZ"), "\+0000", "Z"))