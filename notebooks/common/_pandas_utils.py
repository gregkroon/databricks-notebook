# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC ### Pandas on Spark Utility Functions
# MAGIC 
# MAGIC Requires Spark >= 3.2

# COMMAND ----------

import numpy as np
import pyspark.pandas as ps  #requires Spark >= 3.2

# COMMAND ----------

def square(x) -> ps.Series[np.float64]:
    return x ** 2

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC And this comment is on demo_branch_3