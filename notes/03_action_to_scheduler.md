# 03. Action → Scheduler 진입 지점

목표  
- Spark에서 **실제 실행이 시작되는 코드 위치**를 고정한다  
- 개념 설명 없이 **공식 소스 기준 흐름만 기록한다**

---

## 핵심 질문

RDD에서 `collect()`를 호출하면  
**어디 코드부터 실제 Job 실행이 시작되는가**

---

## Action 진입 지점

### RDD.collect

- 위치  
  core/src/main/scala/org/apache/spark/rdd/RDD.scala

- 특징  
  - Transformation이 아님  
  - 내부에서 SparkContext.runJob 호출  
  - 이 시점부터 lazy 해제

---

## SparkContext

### runJob

- 위치  
  core/src/main/scala/org/apache/spark/SparkContext.scala

- 역할  
  - Job 실행 요청을 Scheduler로 전달  
  - RDD, 함수, 파티션 정보 전달

---

## DAGScheduler

### submitJob

- 위치  
  core/src/main/scala/org/apache/spark/scheduler/DAGScheduler.scala

- 역할  
  - Job을 Stage 단위로 분해  
  - Action 기준으로 Job 생성

### handleJobSubmitted

- 위치  
  DAGScheduler.scala

- 역할  
  - ResultStage 생성  
  - ShuffleDependency 기준으로 Stage 분리  
  - Stage 실행 준비

---

## 실행 흐름 요약 (코드 기준)

