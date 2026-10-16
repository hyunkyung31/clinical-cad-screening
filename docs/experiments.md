# Clinical RF 실험 과정 및 모델 검증

임상정보를 활용한 관상동맥질환(CAD) 분류 모델을 개발하면서 진행한 데이터 전처리, 모델 비교, Random Forest 최종 구성 및 확률 보정 과정을 정리했습니다.

이번 실험에서는 모델의 분류 성능뿐 아니라 **소규모 데이터에서 검증 결과를 얼마나 신뢰할 수 있는지**, 그리고 **모델이 출력하는 예측 확률을 어떻게 평가할 것인지**에 중점을 두었습니다.

실험은 크게 초기 모델 탐색, Nested Cross-Validation을 이용한 모델 비교, Random Forest 구성 및 확률 보정, 모델 저장과 입력 구조 확인의 순서로 진행했습니다.

---

## 1. 초기 데이터 탐색과 모델 학습

### 1.1 데이터 전처리

Extension of Z-Alizadeh Sani 데이터셋의 임상정보 303건을 사용했습니다.

예측 대상은 `Cath` 변수이며, 정상(Normal)을 0, 관상동맥질환(CAD)을 1로 설정했습니다.

전처리 과정에서는 관상동맥질환 판정 결과와 직접적으로 연결되는 `LAD`, `LCX`, `RCA` 변수를 제외했습니다. 이러한 변수를 입력에 포함하면 실제 예측에 사용하기 어려운 정보로 인해 성능이 과대평가될 가능성이 있기 때문입니다.

이외에도 상수 변수인 `Exertional CP`를 제외하고, 범주형 변수의 특성에 맞춰 인코딩을 적용했습니다.

- BBB: One-Hot Encoding
- VHD: Ordinal Encoding
- 원본 54개 입력 변수 → 인코딩 후 모델 입력 55개 변수

### 1.2 초기 모델 비교

먼저 데이터를 Train 80%, Test 20%로 나누어 Logistic Regression과 Decision Tree를 학습했습니다.

Decision Tree는 GridSearch를 이용한 하이퍼파라미터 탐색도 진행했습니다.

초기 실험에서는 제한 없는 Decision Tree의 Train Accuracy가 1.0에 도달했지만, Test Accuracy는 0.7049로 차이가 크게 나타났습니다.

학습 데이터에서는 좋은 성능을 보이더라도 평가 데이터에서는 결과가 달라질 수 있다는 점을 확인했습니다.

또한 전체 데이터가 303건으로 많지 않기 때문에 하나의 Train/Test 분할 결과만으로 모델의 성능을 판단하기 어렵다고 생각했습니다.

특히 같은 Test 데이터를 반복적으로 확인하며 모델을 선택하면, 평가 데이터에 간접적으로 맞춰진 결과를 선택할 위험이 있었습니다.

이 문제를 줄이기 위해 이후 실험에서는 **모델 선택 과정과 성능 평가 과정을 분리하는 Nested Cross-Validation**을 적용했습니다.

관련 코드: [데이터 전처리 및 초기 탐색](../notebooks/preprocessing.ipynb)

---

## 2. Nested Cross-Validation을 이용한 모델 비교

### 2.1 검증 구조

Nested Cross-Validation은 다음과 같이 구성했습니다.

| 구분 | 설정 | 목적 |
|---|---|---|
| Outer CV | 10-fold | 모델 성능 평가 |
| Inner CV | 5-fold | 모델 및 Threshold 선택 |
| 주요 기준 | Sensitivity 95% 우선 | CAD 환자 누락 최소화 |
| 추가 지표 | Specificity, PR-AUC, ROC-AUC | 전반적인 분류 성능 비교 |

각 Outer Fold의 학습 데이터에서 Inner 5-fold OOF(Out-of-Fold) 예측 확률을 생성했습니다.

이후 Inner OOF에서 Sensitivity 95% 이상을 우선 만족하는 Threshold를 탐색하고, Specificity 및 다른 평가 지표를 함께 고려해 후보를 선택했습니다.

선택한 모델과 Threshold는 해당 Outer Fold에서 따로 남겨둔 평가 데이터에 적용했습니다.

이렇게 하면 모델을 선택하는 데 사용하지 않은 데이터에서 예측 성능을 확인할 수 있습니다.

### 2.2 Threshold 선택 시 주의한 점

이번 실험에서는 CAD 선별을 목적으로 했기 때문에, 질환이 있는 환자를 정상으로 잘못 분류하는 False Negative(FN)를 중요하게 살펴봤습니다.

단순히 Accuracy가 높은 모델보다는 Sensitivity를 우선 확보하면서 Specificity가 얼마나 유지되는지 비교했습니다.

다만 Sensitivity를 높이기 위해 Threshold를 낮추면 False Positive(FP)가 증가할 수 있습니다.

따라서 Sensitivity만 높다고 좋은 모델로 판단하지 않고 다른 지표도 함께 비교했습니다.

또한 Nested CV에서는 Outer Fold마다 학습 데이터와 선택된 Threshold가 달라질 수 있습니다.

이 때문에 전체 Outer OOF 결과를 합친 경우 하나의 공통 Threshold가 존재하지 않으며, 집계 결과에서 Threshold가 `NaN`으로 표시되더라도 예측 자체가 누락됐다는 뜻은 아닙니다.

### 2.3 모델별 결과

이번 Nested CV에서 비교한 주요 모델은 XGBoost, Random Forest, Keras ANN입니다.

| 모델 | Sensitivity | Specificity | PR-AUC(AP) | ROC-AUC |
|---|---:|---:|---:|---:|
| XGBoost | 0.9444 | 0.5977 | 0.9513 | 0.9012 |
| **Random Forest** | **0.9537** | **0.6897** | **0.9709** | **0.9278** |
| Keras ANN | 0.9352 | 0.5632 | 0.9609 | 0.9050 |

이 결과에서 Random Forest는 비교 모델 가운데 Sensitivity와 Specificity가 가장 높았고, PR-AUC 및 ROC-AUC에서도 좋은 결과를 보였습니다.

특히 Sensitivity 0.9537은 CAD 환자 216명 중 206명을 양성으로 분류하고 10명을 놓친 결과입니다.

이를 바탕으로 이후 실험에서는 Random Forest를 중심으로 최종 모델 구성을 진행했습니다.

단, 위 성능은 **Nested CV 기반 내부 검증 결과**이며 독립적인 외부 데이터에 대한 성능은 아닙니다.

[모델별 성능 비교 그래프](../figures/nested_model_comparison.png)

---

## 3. ANN 학습 과정과 실행 환경

ANN 모델도 Nested CV 비교 대상으로 실험했습니다.

주요 구성은 다음과 같습니다.

- 6개 모델 설정 비교
- 학습 Fold 내부에서 20%를 Early Stopping 용도로 분리
- Fold별 모델 Checkpoint 저장
- `clear_session()` 및 가비지 컬렉션을 통한 메모리 관리

ANN은 실행 시간이 길고 학습 환경의 영향을 받는 부분이 있어, 저장한 Checkpoint를 이용해 일부 Fold를 이어서 진행했습니다.

기존에 완료된 Fold 1~7의 결과를 활용하고 Fold 8~10을 추가 실행한 기록이 있습니다.

따라서 ANN의 집계 결과는 확인할 수 있지만, 모든 Fold를 동일한 환경에서 처음부터 다시 학습한 재현 결과는 아직 확보하지 못했습니다.

이 과정에서 단순히 모델 구조를 구성하는 것뿐 아니라 **실험 환경과 Checkpoint 관리도 결과를 재현하는 데 중요한 요소**라는 점을 확인했습니다.

관련 코드: [추가 모델 비교 및 ANN 실험](../notebooks/preprocessing_keras_memory_safe.ipynb)

---

## 4. Random Forest 최종 모델 구성

### 4.1 추가 하이퍼파라미터 탐색

Nested CV에서 Random Forest를 선택한 이후에는 별도의 5-fold OOF 실험으로 최종 모델 구성을 검토했습니다.

전체 개발 데이터 303명을 대상으로 Random Forest 후보 24개를 비교했고, Candidate 19를 선택했습니다.

선택한 하이퍼파라미터는 다음과 같습니다.

| Hyperparameter | Value |
|---|---|
| n_estimators | 400 |
| max_depth | 12 |
| min_samples_split | 10 |
| min_samples_leaf | 8 |
| max_features | sqrt |
| criterion | entropy |
| class_weight | balanced_subsample |

여기서 주의할 점은 **앞선 Nested CV와 최종 모델 구성을 위한 5-fold OOF는 서로 다른 평가 단계**라는 것입니다.

Nested CV에서 Random Forest의 Specificity는 0.6897이었지만, 별도 5-fold OOF의 Raw RF에서는 0.6782였습니다.

두 결과는 사용한 코호트가 같더라도 모델 설정과 검증 과정이 다르므로 동일한 성능으로 취급하지 않았습니다.

### 4.2 확률 보정 실험

Random Forest의 분류 성능을 확인한 뒤에는 예측 확률이 얼마나 잘 보정되어 있는지도 살펴봤습니다.

AUROC는 양성과 음성을 구분하는 능력을 평가하지만, 모델이 출력한 확률 자체의 정확성을 직접 보여주지는 않습니다.

따라서 Sigmoid Calibration과 Isotonic Calibration을 추가로 비교했습니다.

보정기는 각 학습 Fold 내부에서 추가 5-fold 절차를 이용해 학습했으며, 해당 평가 Fold를 보정기 학습에 직접 사용하지 않도록 구성했습니다.

비교 지표로는 Sensitivity, Specificity, ROC-AUC와 함께 Brier Score, Expected Calibration Error(ECE)를 사용했습니다.

### 4.3 확률 보정 결과

| 방법 | Sensitivity | Specificity | ROC-AUC | Brier | ECE |
|---|---:|---:|---:|---:|---:|
| Raw RF | 0.9537 | 0.6782 | 0.9177 | 0.1245 | 0.1567 |
| **RF + Sigmoid** | **0.9583** | **0.6782** | 0.9127 | **0.1015** | 0.0501 |
| RF + Isotonic | 0.9537 | 0.6667 | 0.9170 | 0.1033 | **0.0426** |

[확률 보정 비교 그래프](../figures/calibration_comparison.png)

Sigmoid Calibration을 적용한 결과 Brier Score는 0.1245에서 0.1015로, ECE는 0.1567에서 0.0501로 감소했습니다.

Specificity는 0.6782로 유지됐고, Sensitivity는 0.9537에서 0.9583으로 증가했습니다.

이에 따라 CAD 환자의 False Negative는 10명에서 9명으로 줄었습니다.

반면 ROC-AUC는 0.9177에서 0.9127로 소폭 낮아졌습니다.

Isotonic Calibration은 ECE가 가장 낮았지만, Specificity는 Raw RF와 Sigmoid보다 낮았습니다.

이러한 결과를 함께 고려해 **Sigmoid Calibration을 최종 보정 방법으로 선택했습니다.**

### 4.4 최종 구성 결과를 해석할 때의 한계

확률 보정기를 학습할 때 평가 Fold를 직접 사용하지 않도록 구성한 점과, 최종 모델의 성능이 편향 없이 평가됐다는 점은 구분해야 합니다.

이번에는 RF 후보, 보정 방법, Threshold를 동일한 개발 데이터의 OOF 결과를 참고해 선택했습니다.

따라서 최종 구성용 5-fold OOF 결과는 모델 선택에 활용한 내부 실험 결과이며, 새로운 독립 검증 결과로 해석할 수 없습니다.

추후에는 모델과 Threshold를 고정한 뒤 별도 데이터로 평가할 필요가 있습니다.

관련 코드: [Random Forest 최종 구성 및 확률 보정](../notebooks/RF/02_RF_최종검증_신규환자예측.ipynb)

---

## 5. 모델 저장 및 입력 구조 확인

### 5.1 모델 저장과 재로딩

선택한 Random Forest + Sigmoid 모델을 전체 개발 데이터 303명으로 학습한 뒤, 모델과 함께 Threshold 및 입력 Schema 등의 정보를 저장했습니다.

이후 동일한 입력을 사용해 저장 전후의 예측 결과가 일치하는지 확인했습니다.

- 최대 확률 차이: 약 5.55 × 10⁻¹⁶
- Threshold 기준 분류 판정 변경: 0건

이는 모델 저장과 복원 과정에서 출력이 일관되게 유지됐는지 확인한 결과입니다.

신규 환자에 대한 분류 성능을 검증한 결과와는 구분했습니다.

### 5.2 Mock 입력 검증 준비

저장된 모델과 입력 구조를 확인하기 위해 다음 항목을 점검했습니다.

- 저장된 모델 파일과 관련 정보
- 모델 Hash 및 Metadata
- 입력 변수 Schema
- 원본 54개 변수 기준의 빈 입력 Template

다만 실제 Mock 환자 데이터를 생성해 예측을 실행하는 단계까지는 진행하지 못했습니다.

특히 정상 입력, 결측값, 잘못된 범주형 값이 들어오는 경우의 처리 및 예측 결과 검증은 후속 작업으로 남아 있습니다.

입력 구조를 확인한 것과 실제 신규 입력에 대한 추론을 검증한 것은 별개이므로 완료 범위를 구분했습니다.

관련 코드: [RF Mock 입력 검토](../notebooks/RF/03_RF_mock_검증.ipynb)

---

## 6. 주요 문제와 개선 과정

### 6.1 단일 Train/Test 분할의 한계

초기 Decision Tree 실험에서는 학습 정확도가 매우 높았지만 테스트 성능은 그에 미치지 못했습니다.

이후 작은 데이터셋에서 특정 분할 결과에 의존하지 않도록 검증 방법을 Nested Cross-Validation으로 변경했습니다.

### 6.2 분류 성능과 예측 확률의 차이

Random Forest는 내부 검증에서 비교적 높은 Sensitivity와 AUROC를 보였지만, 예측 확률의 보정 정도는 별도로 살펴볼 필요가 있었습니다.

확률 보정을 추가한 결과 Brier Score와 ECE가 개선되는 경우에도 AUROC는 감소할 수 있음을 확인했습니다.

이를 통해 하나의 지표만으로 모델을 선택하기보다 사용 목적에 맞춰 여러 지표를 함께 확인해야 한다는 점을 배웠습니다.

### 6.3 모델 선택 이후의 검증

최종 RF 후보와 확률 보정 방법을 선택하는 과정에서 개발 데이터의 OOF 결과를 활용했습니다.

이러한 결과는 모델을 구성하고 비교하는 데 도움이 되지만, 선택이 끝난 모델의 일반화 성능을 평가하는 독립적인 근거가 되지는 않습니다.

따라서 최종 모델과 Threshold를 고정한 뒤 별도의 데이터로 검증하는 과정이 필요합니다.

### 6.4 실험 실행 환경 관리

ANN 학습에서는 Checkpoint를 활용해 일부 Fold를 재개했으며, 학습 환경이 여러 실행에 걸쳐 달라졌습니다.

또한 전체 실험 과정에서 사용한 데이터, 모델 설정, Threshold, 평가 단계를 구분해 관리해야 결과를 정확하게 비교할 수 있었습니다.

이후에는 실험 조건과 실행 환경을 함께 기록하고, 평가 결과가 어떤 단계에서 나온 것인지 명확하게 남기는 것이 중요하다고 생각했습니다.

---

## 7. 실험 완료 범위와 향후 과제

| 작업 | 현재 상태 |
|---|---|
| 데이터 전처리 및 누수 가능 변수 제외 | 완료 |
| 초기 LR / Decision Tree 탐색 | 완료 |
| Nested CV 기반 XGBoost / RF / ANN 비교 | 내부 평가 완료 |
| Random Forest 후보 및 Threshold 선택 | 개발 데이터 기반 비교 완료 |
| Sigmoid / Isotonic 확률 보정 | 내부 비교 완료 |
| 모델 저장 및 재로딩 일관성 확인 | 완료 |
| 입력 Schema 및 빈 Template 확인 | 완료 |
| 실제 Mock 데이터 추론 및 오류 입력 처리 | 미완료 |
| 독립 외부 검증 | 미완료 |
| SHAP, 하위집단 분석, DCA | 후속 과제 |

이번 실험에서는 Random Forest의 분류 성능을 비교하고 확률 보정까지 진행했지만, 아직 독립적인 외부 검증이나 임상적 활용 가능성을 확인한 것은 아닙니다.

추후에는 최종 모델을 고정한 상태에서 외부 데이터 평가를 진행하고, 실제 서비스 입력을 가정한 기능 검증과 하위집단 분석을 추가할 필요가 있습니다.

또한 모델의 예측 결과를 설명할 수 있는 SHAP 분석과 Decision Curve Analysis(DCA)를 통해 예측 결과를 더 다양한 관점에서 검토하고 싶습니다.

---

## 8. 실험을 통해 배운 점

이번 프로젝트를 진행하면서 모델을 학습하고 성능을 높이는 것만큼 **평가 과정이 적절하게 설계되어 있는지 확인하는 일**도 중요하다는 것을 느꼈습니다.

특히 소규모 임상 데이터에서는 데이터 분할과 Threshold 선택에 따라 결과가 달라질 수 있기 때문에, 평가 데이터가 모델 선택에 어떻게 사용되는지 주의해야 했습니다.

또한 CAD 선별에서는 높은 Accuracy보다 환자를 놓치지 않는 Sensitivity와 False Negative를 중요하게 고려해야 했습니다.

확률 보정 실험을 통해서는 모델의 분류 성능과 출력 확률의 신뢰성을 별도로 평가해야 한다는 점을 배웠습니다.

앞으로는 하나의 성능 수치보다 **데이터 구성, 검증 방식, Threshold, 확률 보정, 실제 활용 목적을 함께 고려하는 모델 개발**을 지향하고자 합니다.

---

### 관련 자료

- [데이터 전처리 및 초기 탐색](../notebooks/preprocessing.ipynb)
- [추가 모델 비교 및 ANN 실험](../notebooks/preprocessing_keras_memory_safe.ipynb)
- [Random Forest 최종 구성](../notebooks/RF/02_RF_최종검증_신규환자예측.ipynb)
- [Mock 입력 검토](../notebooks/RF/03_RF_mock_검증.ipynb)
- [평가 결과와 실험 조건](../results/README.md)
- [실험 환경](environment.md)

이 문서의 성능 수치는 기존 실험 기록을 기준으로 정리했습니다. 최종 모델의 외부 검증 및 실제 Mock 추론은 아직 수행하지 않았습니다.
