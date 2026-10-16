# 집계 결과의 범위와 출처

`metrics.csv`는당시노트북의저장출력과개인ClinicalPDF에서확인한수치입니다. 새학습·새모델추론결과가아닙니다. `source_id`, `source_file`, `source_cells`, `evidence_level`, `pdf_pages`를통해근거를연결했습니다. 원본cell번호는Markdown·빈셀을포함한1-based번호이며공개사본에서도유지했습니다.

빈칸은미기록/해당없음입니다. 서로다른dataset·phase·evaluation_unit·gt_canvas·threshold를합쳐하나의성능으로보면안됩니다. PR-AUC는확인한코드에서average precision입니다. 소수자리수는저장출력/기존집계의정밀도를유지했습니다. LR/SVM의PDF수치를가짜노트북결과로채우지않았습니다.

| 모델 | 데이터 | 평가 단계·단위 | 근거 |
|---|---|---|---|
| LR | Z-Alizadeh Sani Extension | 10-outer/5-inner Nested CV pooled outer OOF / patient | PDF p4-5 |
| Linear SVM | Z-Alizadeh Sani Extension | 10-outer/5-inner Nested CV pooled outer OOF / patient | PDF p4-5 |
| XGBoost | Z-Alizadeh Sani Extension | 10-outer/5-inner Nested CV pooled outer OOF / patient | [P02](../notebooks/preprocessing_keras_memory_safe.ipynb) c78 |
| RF | Z-Alizadeh Sani Extension | 10-outer/5-inner Nested CV pooled outer OOF / patient | [P02](../notebooks/preprocessing_keras_memory_safe.ipynb) c80 |
| Keras ANN | Z-Alizadeh Sani Extension | 10-outer/5-inner Nested CV pooled outer OOF / patient | [P02](../notebooks/preprocessing_keras_memory_safe.ipynb) c89 |
| Candidate19 RF Raw | Z-Alizadeh Sani Extension | final-configuration selection 5-fold OOF / patient | [R02](../notebooks/RF/02_RF_최종검증_신규환자예측.ipynb) c7-9 |
| Candidate19 RF Sigmoid | Z-Alizadeh Sani Extension | final-configuration selection 5-fold OOF / patient | [R02](../notebooks/RF/02_RF_최종검증_신규환자예측.ipynb) c7-9 |
| Candidate19 RF Isotonic | Z-Alizadeh Sani Extension | final-configuration selection 5-fold OOF / patient | [R02](../notebooks/RF/02_RF_최종검증_신규환자예측.ipynb) c7-9 |

## 그림 재생성

`python scripts/plot_results.py`는이CSV만읽습니다. 환자별자료·원본이미지·GT·모델가중치를읽지않습니다. [그림manifest](../figures/manifest.json)는입력CSV와생성script의hash,각PNG의hash·설명을담습니다. 그래프는비교조건을분리했으며계산하지않은ROC곡선·calibration곡선·신뢰구간을임의생성하지않았습니다.

Nested표는outer10/inner5의pooled결과입니다. 최종Candidate19보정표는전체개발303명의별도5-fold구성선택용OOF입니다. 두단계의RawRF값이다릅니다. Mock환자별예측·환자별OOF·학습모델을포함하지않았습니다.
