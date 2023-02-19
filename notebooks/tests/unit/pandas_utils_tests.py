# Databricks notebook source
import unittest
#from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC Run the notebook containing the methods being tested

# COMMAND ----------

# MAGIC %run ../../common/_pandas_utils

# COMMAND ----------

# Define the Unit Test Class
class PandasUtilsTests(unittest.TestCase):
  
  def test_square(self):
   
    # Create a pandas-on-Spark DataFrame
    psdf = ps.DataFrame({'A': np.random.rand(5),
                     'B': np.random.rand(5)})
    
    #call the method to test
    psdf_test = psdf.apply(square)

    #now define the expected result
    psdf_expected = psdf.apply(lambda x: x ** 2)
           
    #check 
    #note we need to call .to_spark() because these are pandas-on-spark dataframes
    self.assertEqual(sorted(psdf_test.to_spark().collect()),sorted(psdf_expected.to_spark().collect()))

  def test_foo(self):
    self.assertEqual('foo', 'foo')
    self.assertNotEqual('foo2', 'foo')

# COMMAND ----------

suite = unittest.TestLoader().loadTestsFromTestCase(PandasUtilsTests)
runner = unittest.TextTestRunner(verbosity=2)
results = runner.run(suite)

# COMMAND ----------

results.printErrors()

if results.wasSuccessful():
  dbutils.notebook.exit(str(results.testsRun) + " successful tests run")
else:
  raise Exception(f"{len(results.failures)} of {results.testsRun} tests failed.")

# COMMAND ----------

