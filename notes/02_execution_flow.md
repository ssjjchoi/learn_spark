# 02. Spark Execution Flow
공식 (https://github.com/apache/spark)
디렉터리 및 주요 소스 파일 기준
- Spark 실행 흐름에서 **어디 코드로 내려가는지만 표시**  
- 설명 최소, 공식 소스 기준 위치만

---

## SparkSession / SparkContext

SparkSession  
- sql/core/src/main/scala/org/apache/spark/sql/SparkSession.scala

SparkContext  
- core/src/main/scala/org/apache/spark/SparkContext.scala


```
Composition: 
SparkSession → SparkContext
┌───────────────────┐
│   SparkSession    │
│  (wrapper / API)  │
│                   │
│  ┌─────────────┐  │
│  │ SparkContext│  │
│  │  (engine)   │  │
│  └─────────────┘  │
└───────────────────┘
structural ⭕  execution flow ❌  
```

---

## RDD (lazy)

RDD 정의  
- core/src/main/scala/org/apache/spark/rdd/RDD.scala

Transformation  
- map / filter  
- 실행 안 됨

---

## Action

collect  
- RDD.scala  
- 내부에서 SparkContext.runJob 호출

Action (collect / show / count)  
→ SparkContext.runJob()  
→ DAGScheduler.submitJob()  

---

## Scheduler

SparkContext.runJob  
- SparkContext.scala

DAGScheduler  
- core/src/main/scala/org/apache/spark/scheduler/DAGScheduler.scala

역할  
- Job → Stage 분리  
- Shuffle 기준 Stage 나눔

---

## Shuffle

reduceByKey  
- ShuffleDependency 생성  
- Stage 최소 2개

---

## DataFrame / SQL

DataFrame API  
- sql/core/src/main/scala/org/apache/spark/sql/DataFrame.scala

QueryExecution  
- sql/core/src/main/scala/org/apache/spark/sql/execution/QueryExecution.scala

흐름  
Logical Plan  
→ Optimized Logical Plan  
→ Physical Plan  
→ RDD 실행

```
=== Logical / Physical Plan ===
== Parsed Logical Plan ==
'Project [unresolvedalias((num#0L * 2), Some(org.apache.spark.sql.Column$$Lambda$2366/0x0000000800f9c840@60064c67))]
+- Filter ((num#0L * cast(2 as bigint)) > cast(4 as bigint))
   +- LogicalRDD [num#0L], false

== Analyzed Logical Plan ==
(num * 2): bigint
Project [(num#0L * cast(2 as bigint)) AS (num * 2)#2L]
+- Filter ((num#0L * cast(2 as bigint)) > cast(4 as bigint))
   +- LogicalRDD [num#0L], false

== Optimized Logical Plan ==
Project [(num#0L * 2) AS (num * 2)#2L]
+- Filter (isnotnull(num#0L) AND ((num#0L * 2) > 4))
   +- LogicalRDD [num#0L], false

== Physical Plan ==
*(1) Project [(num#0L * 2) AS (num * 2)#2L]
+- *(1) Filter (isnotnull(num#0L) AND ((num#0L * 2) > 4))
   +- *(1) Scan ExistingRDD[num#0L]
```

```
INFO CodeGenerator: Code generated in 5.74625 ms
== Action Result (df2.show()) ==
+---------+
|(num * 2)|
+---------+
|        6|
|        8|
+---------+
```

---

## 요약 흐름

SparkSession  
→ SparkContext  
→ RDD  
→ Action  
→ DAGScheduler  
→ Stage / Task  

DataFrame
→ Catalyst (Plan)
→ RDD