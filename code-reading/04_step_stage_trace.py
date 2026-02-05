"""
04. Job → Stage → Task Trace

목표:
- Spark Job이 Stage로 분해되는 지점 코드 기준 추적
- ShuffleDependency가 Stage 경계가 되는 지점 확인

Scala source flow (Apache Spark GitHub):
RDD.collect
→ SparkContext.runJob
→ DAGScheduler.handleJobSubmitted
→ createResultStage
→ getOrCreateParentStages
→ ShuffleDependency 기준 Stage 분리
→ submitStage → TaskSet 생성
"""

from pyspark.sql import SparkSession


# SparkSession 생성
# sql/core/src/main/scala/org/apache/spark/sql/SparkSession.scala
spark = SparkSession.builder \
    .appName("step04-stage-trace") \
    .master("local[*]") \
    .getOrCreate()


# SparkContext
# core/src/main/scala/org/apache/spark/SparkContext.scala
sc = spark.sparkContext


# RDD 생성
# core/src/main/scala/org/apache/spark/rdd/RDD.scala
rdd = sc.parallelize(range(1, 11), 4)


# Narrow Dependency (같은 Stage)
# RDD.scala: def map
mapped = rdd.map(lambda x: x * 2)


# Shuffle 발생
# PairRDD → reduceByKey 내부에서 ShuffleDependency 생성
# core/src/main/scala/org/apache/spark/rdd/PairRDDFunctions.scala
paired = mapped.map(lambda x: (x % 2, x))
reduced = paired.reduceByKey(lambda a, b: a + b)


# Action
# 이 시점에서 Job 생성
# → ResultStage + ShuffleMapStage 생성
result = reduced.collect()
print("Final Result:", result)

# Spark UI 확인용 대기
import time
print("UI 확인 60초 대기...")
time.sleep(60)

spark.stop()
