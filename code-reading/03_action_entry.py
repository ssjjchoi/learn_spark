"""
03. Spark Action Entry Point Trace

목표:
- Spark에서 lazy evaluation이 언제 해제되는지 코드 기준으로 확인
- collect() 호출 시 Driver 측에서 실행이 시작되는 지점 고정

Scala source flow (Apache Spark GitHub):
RDD.collect
→ SparkContext.runJob
→ DAGScheduler.submitJob
→ DAGScheduler.handleJobSubmitted
"""

from pyspark.sql import SparkSession


# SparkSession 생성
# sql/core/src/main/scala/org/apache/spark/sql/SparkSession.scala
spark = SparkSession.builder \
    .appName("step03-action-entry") \
    .master("local[*]") \
    .getOrCreate()


# SparkContext
# core/src/main/scala/org/apache/spark/SparkContext.scala
sc = spark.sparkContext


# RDD 생성
# core/src/main/scala/org/apache/spark/rdd/RDD.scala
rdd = sc.parallelize([1, 2, 3, 4, 5])


# Transformation 1: map (lazy)
# RDD.scala: def map
mapped = rdd.map(lambda x: x * 2)


# Transformation 2: filter (lazy)
# RDD.scala: def filter
filtered = mapped.filter(lambda x: x > 5)


# Action
# RDD.scala: def collect
# 이 시점부터 실제 Job 생성
# → SparkContext.runJob
# → DAGScheduler.submitJob
# → DAGScheduler.handleJobSubmitted
result = filtered.collect()


print("Final Result:", result)


spark.stop()