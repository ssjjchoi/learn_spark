# Spark 공식 소스 기반 최소 시작점

from pyspark.sql import SparkSession

# 1) SparkSession 생성
spark = SparkSession.builder \
    .appName("core-to-dataframe") \
    .master("local[*]") \
    .getOrCreate()

# 2) SparkSession 내부에 SparkContext가 있음
sc = spark.sparkContext

# 이 print는 공식 RDD 코드가 어떻게 나오는지 보여줌
print("SparkContext:", sc)

# 3) RDD 예제
# 이 부분은 core/src/main/scala/org/apache/spark/rdd/RDD.scala
rdd = sc.parallelize([10, 20, 30, 40])

# map/filter은 실행계획을 바로 만들고
# 아직 실행은 안 됨 (lazy)
mapped = rdd.map(lambda x: x * 10)
filtered = mapped.filter(lambda x: x > 200)

# collect()에서 실제 실행이 이루어짐
print("RDD result:", filtered.collect())

# 4) DataFrame 예제
# DataFrame은 sql/core 코드를 타게 됨
df = spark.createDataFrame([(1,), (2,), (3,), (4,)], ["num"])

# filter + select는 Logical → Optimizer → Physical로 넘어감
df2 = df.filter(df.num * 2 > 4).select(df.num * 2)

df2.show()

# 5) Spark 종료
spark.stop()
