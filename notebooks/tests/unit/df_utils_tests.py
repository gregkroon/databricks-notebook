# Databricks notebook source
import unittest
from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC Run the notebook containing the methods being tested

# COMMAND ----------

# MAGIC %run ../../common/_df_utils

# COMMAND ----------

# Define the Unit Test Class
class DfUtilsTests(unittest.TestCase):
  
  def test_timestamp_to_zulu(self):
   
    #define a test dataframe
    test_df = spark.createDataFrame(
      [
        (1, "2022-01-01T19:18:16.000+0000"),
        (2, "2022-02-01T19:18:16.000+0000"),
        (3, "2022-03-01T21:18:16.000+0000"),
        (4, "2022-01-02T05:18:16.000+0000"),
        (5, "2022-01-03T19:18:57.000+0000")
      ], 
      ["@id", "date_string"]
    )
    
    test_df = test_df.withColumn("date_timestamp", F.to_timestamp("date_string"))

    #call the timestamp_to_zulu() transformation method
    actual_df = test_df.select("@id", timestamp_to_zulu("date_timestamp").alias("zulu_string"))
    
    #now define the expected result
    expected_df = spark.createDataFrame(
      [
        (1, "2022-01-01T19:18:16.000Z"),
        (2, "2022-02-01T19:18:16.000Z"),
        (3, "2022-03-01T21:18:16.000Z"),
        (4, "2022-01-02T05:18:16.000Z"),
        (5, "2022-01-03T19:18:57.000Z")
      ], 
      ["@id", "zulu_string"]
    )
                          
    self.assertEqual(sorted(expected_df.collect()),sorted(actual_df.collect()))

  def test_foo(self):
    self.assertEqual('foo', 'foo')
    self.assertNotEqual('foo2', 'foo')



# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Run the Test Suite

# COMMAND ----------

suite = unittest.TestLoader().loadTestsFromTestCase(DfUtilsTests)
runner = unittest.TextTestRunner(verbosity=2)
results = runner.run(suite)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Check results, throw Exception to fail Job if there were errors

# COMMAND ----------

results.printErrors()

if results.wasSuccessful():
  dbutils.notebook.exit(str(results.testsRun) + " successful tests run")
else:
  raise Exception(f"{len(results.failures)} of {results.testsRun} tests failed.")
  

# COMMAND ----------

