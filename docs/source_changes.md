# 원본 대비 변경

원본은 `hyunkyung31/coronary-ai-ml-dl`의 개인 `hyunkyung/`이며 기준commit은 `28bf910207229e834893f9c92a1d4bc034855c64`입니다. 팀 저장소와 기존 YOLO 저장소는 수정하지 않았습니다. 이 저장소는 원본 Git 기록을 가져오지 않고 공개용 파일만 선별한 독립 저장소입니다.

## 공통 정리

- 개인노트북 4개를복사하고원본셀순서·개수를유지했습니다. 각셀metadata의 `original_cell_1based`와 `source_manifest.json`에서근거위치를찾을수있습니다.
- 저장출력 146개를모두제거했습니다. 이중image MIME을포함한출력은 9개입니다. 원본은그대로보존되어있습니다.
- 실행카운터,widget/Colabmetadata,cell첨부를비우고최소kernel정보만남겼습니다. 출력이없는것은실험미실행을새로판정한것이아니라공개용정리정책입니다.
- 개인계정·팀프로젝트경로를일반예제이름으로바꾸고Unicode를NFC로정규화했습니다. 정규화도셀hash변경내역에포함합니다.
- 원래저장된성능은출력에서복제한안전한집계CSV로분리했습니다. 새학습·평가결과를만들지않았습니다. 환자별표·OOF·이미지·모델은복사하지않았습니다.
- `scripts/plot_results.py`와 `scripts/review_public_files.py`는공개자료정리를위해추가한보조도구입니다. 과거실험코드로소개하지않습니다.

## 소스 변경 위치

| 파일 | 변경한 원본 셀 |
|---|---|
| `notebooks/RF/02_RF_최종검증_신규환자예측.ipynb` | 소스 변경 없음 |
| `notebooks/RF/03_RF_mock_검증.ipynb` | 소스 변경 없음 |
| `notebooks/preprocessing.ipynb` | 4 |
| `notebooks/preprocessing_keras_memory_safe.ipynb` | 11 |

실험 로직은 개인 경로와문자정규화외에는바꾸지않았습니다. LR/SVM Nested구현을다른팀원폴더에서가져오지않았고,새Mock추론코드나예측값도만들지않았습니다. RF의threshold·모델선택·calibration방법을변경하지않았습니다.

파일별·셀별원본/사본SHA-256은 [source_manifest.json](source_manifest.json), 출력제거건수는 [source_changes.csv](source_changes.csv)에있습니다. 원본코드의개인값이노출될수있어전체raw diff를공개폴더에넣지않았습니다. 사본의모든셀을정적구문검사했지만의존자료와GPU를포함한전체실행은검증하지않았습니다.

## 최종 공개 전 정리

추가 산출물이 실수로 포함되지 않도록 `.gitignore`에서 CSV·JSON·이미지는 이 저장소의 집계 파일·manifest·생성 그래프만 예외로 두었습니다. PDF·키 파일·백업·캐시도 제외합니다. 공개 검사 스크립트의 경로 탐지 규칙에는 실제 개인 계정명이나 팀 폴더명을 남기지 않았습니다. 이 정리로 실험 수치·조건이나 노트북의 학습 로직을 변경하지 않았습니다.
