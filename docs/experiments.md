# Clinical 실험의 평가 단계

원본commit·셀은 `source_manifest.json`, 집계수치는 `../results/metrics.csv`에 연결했습니다. 공개 사본은 원본 셀 순서를 유지하되 저장 출력을 비웠습니다.

## 초기 탐색과 Nested CV

`preprocessing.ipynb` c14/c24–58은 누수 변수 제외 후80/20 split의 LR/DT와 DT GridSearch를 다룹니다. `preprocessing_keras_memory_safe.ipynb`의 앞부분에는 같은 탐색 단계가 반복됩니다. 이를두개의독립된전체실험으로세지않았습니다.

후반 c69–81의 XGBoost/RF는 outer10/inner5입니다. 후보마다inner OOF 확률을 만들고 민감도95% 조건을 만족하는threshold를 선택합니다. 그안에서 specificity·AP·AUROC 등을 비교해 고른후 outer held-out에 평가합니다(c75). Pooled결과의threshold가NaN인것은여러fold의결정값을합쳤기때문입니다.

ANN은6config,training내20% early-stop split,clear_session/gc와fold checkpoint를 사용합니다(c83–89). 저장출력은fold1–7을재사용하고8–10을실행한내용입니다. 환경차이가있어단일환경재현은남아있습니다.

LR/Linear SVM의Nested결과는첨부ClinicalPDF p4–5가근거입니다. 이개인폴더에해당Nested코드가없어다른팀원코드로채우지않았습니다. 초기80/20 LR결과를Nested성능으로대체하지않았습니다.

## RF 최종 구성과 보정

`RF/02_RF_최종검증_신규환자예측.ipynb` c4는원래NestedRF를읽습니다. c7은전체303명의별도5-fold OOF에서24후보를비교해Candidate19를고릅니다. 동일Sensitivity .9537이어도원래NestedRF specificity .6897과최종구성용Raw .6782는다른결과입니다.

c8의Sigmoid/Isotonic은각training fold안에서추가5-fold보정을수행합니다. validation을보정기fit에직접넣지는않지만,RF후보와pooled threshold·보정방법을개발OOF에서선택하므로새로운unbiased Nested평가또는외부검증이아닙니다.

Sigmoid는Brier/ECE를개선하고FN을10→9로줄였지만AUROC는소폭감소했습니다. Isotonic의낮은ECE만으로모든지표에서최고라고하지않습니다. 작은표본의과적합가능성은후속위험이지외부자료로입증한실패가아닙니다.

## 저장과 Mock의 경계

R02 c9–10은전체개발모델저장·재로딩후확률과threshold판정을비교했습니다. 이출력은artifact일관성검사이며신규환자성능이아닙니다. 모델파일과원시예측은이사본에없습니다.

`RF/03_RF_mock_검증.ipynb` c4/c6은저장파일·schema·빈template를확인합니다. c7제목뒤의c8–13은빈셀입니다. 실제정상/결측/잘못된범주Mock생성·추론과독립환자검증은미완료입니다. 새추론코드나성공예측을추가하지않았습니다.

## 완료 범위

| 작업 | 상태 |
|---|---|
| 초기LR/DT, NestedXGB/RF/ANN | 코드와저장출력근거있음 |
| NestedLR/SVM 비교 | PDF기록있음, 개인구현미확인 |
| RF후보선택·Raw/Sigmoid/Isotonic비교 | 최종구성용OOF출력있음 |
| 전체303명모델저장·재로딩 | 당시출력근거있음, 현재artifact재실행없음 |
| 입력schema·빈template확인 | 당시출력근거있음 |
| 실제Mock추론·오류입력처리 | 미완료 |
| 독립외부검증·SHAP·하위집단·DCA | 공개증빙없음/후속과제 |
