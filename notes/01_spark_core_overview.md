# Spark 공식 GitHub 구조 정리

문서는 공식 (https://github.com/apache/spark)의
디렉터리 및 주요 소스 파일 기준

---

## 1. 핵심 모듈 개요

공식 저장소에서 핵심 모듈은 두 디렉터리로 구분
Spark의 실행 구조와 API 흐름은 아래 모듈 중심으로 구성

- core/
- sql/


---

## 2. core/ 모듈

core 모듈에는 Spark의 기본 실행 엔진과 RDD 관련 코드가 위치

### 주요 파일

- core/src/main/scala/org/apache/spark/SparkContext.scala  
  https://github.com/apache/spark/blob/master/core/src/main/scala/org/apache/spark/SparkContext.scala  
  - SparkContext 클래스 정의 (약 L70~)  
  - RDD 생성 API(`parallelize`, `textFile`) 포함 (약 L500~600)

- core/src/main/scala/org/apache/spark/rdd/RDD.scala  
  https://github.com/apache/spark/blob/master/core/src/main/scala/org/apache/spark/rdd/RDD.scala  
  - RDD 클래스 정의 (파일 전반)  
  - 변환 연산(`map`, `filter`) 정의 (중반부)  
  - 액션(`collect`) 정의 (후반부)

### 정리

- RDD는 core 모듈에 정의되어 있다.
- 파티션, 의존성, 실행 단위 관리 로직이 이 레벨에 위치.

---

## 3. sql/ 모듈

sql 모듈에는 DataFrame, Dataset, SQL 처리 관련 코드 위치.

### 주요 파일

- sql/core/src/main/scala/org/apache/spark/sql/SparkSession.scala  
  https://github.com/apache/spark/blob/master/sql/core/src/main/scala/org/apache/spark/sql/SparkSession.scala  
  - SparkSession 클래스 정의 (약 L60~)  
  - 내부 필드로 SparkContext 참조

- sql/core/src/main/scala/org/apache/spark/sql/DataFrame.scala  
  https://github.com/apache/spark/blob/master/sql/core/src/main/scala/org/apache/spark/sql/DataFrame.scala  
  - DataFrame API 정의  
  - Dataset 기반 인터페이스 구조

- sql/catalyst/  
  https://github.com/apache/spark/tree/master/sql/catalyst  
  - Logical Plan, Optimizer 관련 코드 위치

### 정리

- DataFrame API는 sql 모듈에 정의되어 있다.
- 실행 이전 단계의 계획 수립 로직이 이 영역에 위치.

---

## 4. 공식 코드 기준 주요 객체 관계
DataFrame은 SparkSession을 통해 생성되며,
실행 단계에서는 RDD 기반 구조로 연결.

SparkSession  
 → SparkContext  
   → RDD  

---

## 5. 코드 탐색 기준 우선순위
순서는 공식 저장소 구조에 따른 코드 흐름을 기준.

1. SparkContext.scala  
2. RDD.scala  
3. SparkSession.scala  
4. DataFrame.scala  


