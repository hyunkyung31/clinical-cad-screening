# 소규모 임상 데이터의 CAD 선별 모델

Extension of Z-Alizadeh Sani 데이터로 CAD 선별 모델을 비교하고, Random Forest의 확률 보정까지 살펴본 개인 실험입니다. 작은 Test를 반복해서 보며 모델을 고르던 초기 탐색에서 출발해, 모델과 threshold 선택을 평가 데이터에서 분리하는 Nested Cross-Validation으로 검증 방식을 바꿨습니다.

팀 관상동맥 AI 프로젝트에서 제가 진행한 임상 전처리·XGBoost/RF/ANN 실험과 RF 최종 구성 작업을 정리했습니다. LR·Linear SVM의 Nested 비교 수치는 개인 정리PDF에 기록되어 있으나 이 개인 폴더에 해당 Nested 구현은 없어 별도로 표시했습니다. 결과는 당시 저장된 출력과PDF를 근거로 하며 새로 학습한 수치가 아닙니다.

![RF 내부 검증과 별도 최종 구성용 확률 보정](figures/portfolio_cover.png)

두 패널은 같은 개발 코호트의 **서로 다른 평가 단계**입니다. 최종 구성용 보정 결과를 원래10-fold Nested 결과나 독립 외부 검증과 합치지 않았습니다.

## 데이터 출처

[UCI Extension of Z-Alizadeh Sani](https://archive.ics.uci.edu/dataset/411/extention+of+z+alizadeh+sani+dataset)를 사용했습니다([DOI](https://doi.org/10.24432/C5461K)). 공식 페이지의 배포 조건은 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)입니다.

실험 자료는303명(CAD216명, Normal87명)의 임상표이며, AngioCAD Clinical-only/Fusion에 등장하는 개발303명과는 다른 코호트입니다. 원본Excel과 환자별 행·OOF 예측은 포함하지 않았습니다. 실제 사용Excel과 공식 배포 파일의 버전 대응은 추가 확인이 필요합니다. [출처·이용 조건](docs/data_sources.md)

## 1. 전처리와 누수 변수 제외

Target은 `Cath`이며 Normal0/CAD1로 변환했습니다. CAD 결과를 직접 담는 `LAD`, `LCX`, `RCA`는 입력에서 제외했고, 상수 변수인 `Exertional CP`도 제거했습니다. BBB는 one-hot, VHD는 ordinal로 처리해 원본54개 입력을55개 모델 입력으로 변환했습니다.

초기80/20 탐색에서는 LR과 Decision Tree를 비교했습니다. 제한 없는 트리는 Train accuracy1.0에 비해 Test accuracy0.7049로 차이가 컸습니다. 작은 Test를 여러 번 확인하며 모델을 고르는 한계를 줄이기 위해 이후 검증 설계를 바꿨습니다.

## 2. Nested CV에서 RF를 고른 이유

Outer10-fold에서 평가하고, 각 outer training 내부의 inner5-fold OOF로 후보와 threshold를 골랐습니다. Inner OOF sensitivity95% 이상을 우선 만족하는 threshold를 찾은 뒤 specificity와 PR-AUC 등을 비교했습니다. 따라서 pooled outer OOF에는 하나의 공통 threshold가 없습니다.

| 모델 | Sensitivity | Specificity | PR-AUC(AP) | ROC-AUC | 근거 |
|---|---:|---:|---:|---:|---|
| Logistic Regression | 0.9444 | 0.5747 | 0.9647 | 0.9170 | PDF기록만 |
| Linear SVM | 0.9398 | 0.5977 | 0.9640 | 0.9157 | PDF기록만 |
| XGBoost | 0.9444 | 0.5977 | 0.9513 | 0.9012 | 노트북·PDF |
| Random Forest | 0.9537 | 0.6897 | 0.9709 | 0.9278 | 노트북·PDF |
| Keras ANN | 0.9352 | 0.5632 | 0.9609 | 0.9050 | 노트북·PDF |

[비교 그래프](figures/nested_model_comparison.png) · [근거 셀·평가 조건](results/README.md)

이 내부 평가에서 RF는 CAD216명 중206명을 찾고10명을 놓쳤습니다. 다만 Brier0.1233, ECE0.1590으로 확률 자체의 보정은 더 살펴볼 필요가 있었습니다. ANN은 fold checkpoint로 재개한 결과이며 실행 환경이 섞여 있어 단일 환경 재현도 남아 있습니다.

## 3. 최종 RF 구성과 확률 보정

다음 단계에서는 전체 개발303명의 **별도5-fold OOF**로 RF24개 후보 중 Candidate19를 골랐습니다. 400trees, max depth12, min split10, min leaf8, `sqrt`, `entropy`, `balanced_subsample` 구성입니다.

각 training fold 내부에서 보정기를 학습해 Sigmoid와 Isotonic을 비교했습니다.

| 방법 | Threshold | Sensitivity | Specificity | ROC-AUC | Brier | ECE |
|---|---:|---:|---:|---:|---:|---:|
| Raw RF | 0.419485 | 0.9537 | 0.6782 | 0.9177 | 0.1245 | 0.1567 |
| RF + Sigmoid | 0.3558017639 | 0.9583 | 0.6782 | 0.9127 | 0.1015 | 0.0501 |
| RF + Isotonic | 약0.3333 | 0.9537 | 0.6667 | 0.9170 | 0.1033 | 0.0426 |

![최종 구성용 OOF의 Brier와 ECE](figures/calibration_comparison.png)

Sigmoid는 특이도를 유지하면서 FN을10명에서9명으로 줄였고 Brier와 ECE를 개선했습니다. AUROC는0.9177에서0.9127로 낮아졌습니다. Isotonic의 ECE가 더 낮았지만 특이도와 다른 지표도 함께 보고 Sigmoid를 선택했습니다.

RF후보·보정 방법·pooled threshold를 같은 개발 OOF를 보고 선택했으므로, 이 표를 새로운 독립 검증 결과로 해석할 수 없습니다. 확률 보정기를 fit할 때 validation을 직접 사용하지 않은 것과, 최종 구성을 선택한 뒤 편향 없는 평가를 마쳤다는 것은 다른 문제입니다.

## 4. 모델 저장·재로딩과 입력 schema

선택한 RF+Sigmoid를 전체303명으로 학습하고 모델·metadata·threshold·입력schema를 저장했습니다. 저장 전후 최대 확률 차이는 약5.55×10⁻¹⁶, threshold 판정 변경은0건이었습니다. 이는 저장·복원 과정의 일관성 확인이며 신규 환자에서의 정확도를 평가한 결과는 아닙니다.

`RF/03_RF_mock_검증.ipynb`에는 최종 artifact·모델hash·입력schema·빈54열 template 확인까지 있습니다. 뒤의 실제 Mock 생성·추론 셀은 비어 있어 **Mock 추론과 잘못된 입력 처리 검증은 미완료**로 남겼습니다. 공개용 사본에 실행하지 않은 예측 결과를 추가하지 않았습니다.

## 배운 점과 남은 과제

판별 성능과 출력 확률의 품질을 따로 평가해야 했습니다. 높은 AUROC만으로 환자에게 제시할 확률을 신뢰할 수 있는 것은 아니었고, 보정 후에도 민감도·특이도가 유지되는지 확인해야 했습니다.

다음 과제는 모델과 threshold를 고정한 독립 코호트 평가, 실제 Mock·범주 오류·결측 입력에 대한 기능 검증, 하위집단 분석과 DCA입니다. 현재 결과를 임상 적용 성능이나 외부 검증 완료로 소개하지 않습니다. [실험 설계와 한계](docs/experiments.md)

## 파일과 실행

- `notebooks/`: 전처리2개와 RF작업2개를 정리한 개인 노트북 사본
- `results/`: Nested 결과와 최종 구성용OOF를 구분한 집계 CSV
- `figures/`: 환자별 자료가 없는 집계 그래프
- `scripts/`: 그래프 재생성과 공개 파일 정적 검사

```bash
python -m pip install -r requirements.txt
python scripts/plot_results.py
python scripts/review_public_files.py
```

위 명령은 집계 자료를 다루며 RF를 새로 학습하거나 실제 환자를 추론하지 않습니다. 과거 학습 환경, 원본 자료와 저장 artifact 준비 사항은 [실행 환경](docs/environment.md)에 있습니다. [원본 대비 변경](docs/source_changes.md) · [공개 범위](docs/publication_review.md) · [포트폴리오 카드](docs/portfolio_card.md)
