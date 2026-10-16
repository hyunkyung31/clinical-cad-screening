# 실행 환경과 재현 범위

## 집계 그래프와 정적 검사

`requirements.txt`는Python3.12에서집계CSV를그리거나노트북형식·셀구문을검사하는환경입니다. 모델학습환경과분리했습니다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/plot_results.py
python scripts/review_public_files.py
```

그림재생성은환자자료나학습모델을읽지않습니다. 정적검사는모델을실행하지않으므로과거성능재현·의료적유효성검증과다릅니다.

## 과거 RF 환경

R02저장출력은Python3.13.15,NumPy2.1.3,pandas2.2.3,scikit-learn1.6.1,joblib1.5.3을기록합니다. 이는원본실험의버전기록이며위그래프환경과같지않습니다. XGBoost·TensorFlow/Keras·openpyxl·koreanize-matplotlib도해당노트북의기능에필요합니다. 모든패키지버전을고정한원본lockfile은없습니다. ANN은여러세션의checkpoint를이어썼으므로하나의검증된학습환경이라고묶지않았습니다.

다시학습하려면별도환경에서원본Excel을준비하고전처리→Nested CV→RF구성·보정순으로진행해야합니다. pandas/sklearn버전차이와joblib호환성도확인해야합니다. 현재사본에서새학습·모델재로딩·Mock추론은실행하지않았습니다.

## 입력·산출물

공개사본의예제경로는일반적인Colab Drive구조입니다. `preprocessing.ipynb`의개인Linux경로는 `/content/drive/MyDrive/research-data/Clinical`로바꿨고,다른노트북은경로설정셀에서해당자료위치를맞춰야합니다. Colab mount코드는유지했습니다.

RF최종구성은원본Excel뿐아니라P02에서저장한Nested결과·signature·config를읽습니다. R03은최종모델·metadata·threshold·input_schema·빈template를읽습니다. 이artifact들은공개사본에없습니다. 기존timestamp폴더는과거실험의참조이므로실제보유artifact위치에맞춰야합니다.

원본자료·모델·환자별OOF는권한이있는비공개장소에두고,필요하면 `data/`, `private/`, `artifacts/`를사용합니다. `.gitignore`는기록에이미들어간민감자료를제거하거나접근을차단하지않습니다.

R03의빈Mock셀은그대로두었습니다. 정상·결측·잘못된범주·극단입력을처리하는코드와예측결과가추가로필요하지만이공개사본에서새성공사례를만들지는않았습니다.
