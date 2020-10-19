from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import countDistinct
from pyspark.sql.functions import col

spark = SparkSession \
    .builder \
    .appName("Spark_EnronEmail") \
    .getOrCreate()

# may need to set this environmetn variable as well
# _JAVA_OPTIONS: -Xms1024M -Xmx2048M
spark.conf.set("spark.executor.memory", "2g")

# load every CSV in the folder
df = spark.read.format("csv")  \
        .option("header", "true")   \
        .load("./export/*.csv")
#df.collect()

print( "cols are ", df.columns )
print("length of", df.count() ) 
# df1.filter(col("long_text").contains(col("number"))).show()
# some of the 'ids' are parsed wrong, so including jsut ones with a  pattern of 
# "<26124562.1075849737648.JavaMail.evans@thyme>"  
# 
dc = df.filter(col("id").contains("JavaMail")).groupBy( "id" ).agg( countDistinct("id" ))
dc.repartition(1).write.csv('email_ids')
#dc.collect()
print( dc.show() )
print( 'total unique email-ids ' , dc.count() )

to_emails_df = df.filter(
        col("to").contains("@"))  \
        .groupBy('to' )  \
        .agg( countDistinct("id") ) \
        .filter("to is NOT null AND to != ''")   \
        .sort(col("count(DISTINCT id)").desc() )
to_emails_df.collect() 
to_emails_df.repartition(1).write.csv('to_emails')
print( "cols are ", to_emails_df.columns )
print( to_emails_df.show() )

