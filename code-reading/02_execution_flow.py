from pyspark.sql import SparkSession

"""
Spark 공식 소스(core → scheduler → sql) 흐름 보기 최소버전
"""

# SparkSession 생성
# - sql/core/src/main/scala/org/apache/spark/sql/SparkSession.scala
spark = SparkSession.builder \
    .appName("step02-execution-flow") \
    .master("local[*]") \
    .getOrCreate()

sc = spark.sparkContext
print("SparkContext:", sc)


# 2) RDD 실행 흐름 명확히 보기
# - core/src/main/scala/org/apache/spark/rdd/RDD.scala
# - collect() → SparkContext.runJob → DAGScheduler
rdd = sc.parallelize([1, 2, 3, 4, 5], numSlices=2)

mapped = rdd.map(lambda x: x * 2)
filtered = mapped.filter(lambda x: x > 5)

# Action 지점
result = filtered.collect()
print("RDD result:", result)

"""
여기서 확인할 것:
- collect() 호출 시 Job 생성
- Shuffle 없음 → Stage 1개
- SparkContext.runJob → DAGScheduler.runJob 흐름
"""


# 3) Shuffle 발생시키기 (Stage 분리 관찰용)
pairs = sc.parallelize(
    [("a", 1), ("b", 1), ("a", 1), ("b", 1)],
    numSlices=2
)

# reduceByKey는 ShuffleDependency 생성
reduced = pairs.reduceByKey(lambda a, b: a + b)

print("Shuffle result:", reduced.collect())

"""
여기서 확인할 것:
- Stage 2개로 분리됨
- ShuffleMapStage / ResultStage
- DAGScheduler가 Stage DAG를 나눔
"""


# 4) DataFrame → Logical / Physical Plan 확인
# - sql/core + sql/catalyst
df = spark.createDataFrame(
    [(1,), (2,), (3,), (4,)],
    ["num"]
)

df2 = df.filter(df.num * 2 > 4).select(df.num * 2)

# 실행 전 계획 확인
print("=== Logical / Physical Plan ===")
df2.explain(True)

# Action
df2.show()

"""
여기서 확인할 것:
- Logical Plan
- Optimized Logical Plan
- Physical Plan
- 마지막엔 다시 RDD 실행으로 내려감
"""

spark.stop()