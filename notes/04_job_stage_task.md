# 04. Job → Stage → Task 분해 흐름

목표  
- Action 이후 Spark Job이 **어떻게 Stage와 Task로 분해되는지** 코드 기준으로 고정  
- Stage 경계가 생성되는 **유일한 기준**을 명확히 한다  
- 개념 설명 없이 **Apache Spark 공식 소스 흐름만 기록**한다  

---

## 핵심 질문

DAGScheduler는  
어떤 조건에서 Job을 여러 Stage로 분리하는가

---

## Job 생성 이후 진입 지점

### DAGScheduler.handleJobSubmitted

- 위치  
  core/src/main/scala/org/apache/spark/scheduler/DAGScheduler.scala  

- 역할  
  - Action 기준으로 Job 처리 시작  
  - ResultStage 생성  
  - Stage DAG 생성 로직 진입  

---

## ResultStage 생성

### createResultStage

- 위치  
  DAGScheduler.scala  

- 역할  
  - Action 결과를 수집하는 최종 Stage 생성  
  - 최종 RDD 기준으로 부모 Stage 탐색 시작  

---

## Stage 분리 기준

### ShuffleDependency

- 위치  
  core/src/main/scala/org/apache/spark/Dependency.scala  

- 의미  
  - RDD lineage 중 ShuffleDependency가 존재하면  
    → **Stage 경계 생성**  
  - NarrowDependency는 같은 Stage로 유지  

---

## 부모 Stage 생성 흐름

### getOrCreateParentStages

- 위치  
  DAGScheduler.scala  

- 역할  
  - ShuffleDependency 발견 시  
    → 새로운 ShuffleMapStage 생성  
  - 재귀적으로 Stage DAG 구성  

---

## Stage → Task 변환

### submitStage

- 위치  
  DAGScheduler.scala  

- 역할  
  - Stage를 TaskSet으로 변환  
  - RDD 파티션 수만큼 Task 생성  

---

## 실행 흐름 요약 (코드 기준)

RDD.collect
→ SparkContext.runJob  
→ DAGScheduler.submitJob  
→ handleJobSubmitted  
→ createResultStage  
→ getOrCreateParentStages  
→ ShuffleDependency 기준 Stage 분리  
→ submitStage  
→ TaskSet 생성  

---

## 실행 로그 확인 
Stage 분리

실행  
spark-submit 04_step_stage_trace.py

DAGScheduler 로그

INFO DAGScheduler: Final stage: ResultStage 1
INFO DAGScheduler: Parents of final stage: List(ShuffleMapStage 0)
INFO DAGScheduler: Submitting ShuffleMapStage 0
INFO DAGScheduler: Submitting ResultStage 1
  
- ShuffleDependency 존재  
- ShuffleMapStage → ResultStage 분리 확인  
- Stage 경계 생성 시점이 Action 이후임 로그 확인

## Spark UI (4040)

- ResultStage DAG에 ShuffledRDD 표시
- collect Action 위치가 Stage 시작점
- Task 수 = RDD 파티션 수 (4)


## 정리

- Stage는 Action 기준으로 생성된다  
- Stage 경계는 ShuffleDependency 기준이다  
- Task 개수 = RDD 파티션 수다  
- 이 단계는 전부 Driver 영역이다  
- Executor는 아직 관여하지 않는다  

---

## next time

- ShuffleDependency 내부 동작  
- Partition 개수 결정 시점  
- reduceByKey / groupByKey 성능 차이  

→ 05. Shuffle / Partition