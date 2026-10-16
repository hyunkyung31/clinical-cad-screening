# 데이터 출처 및 이용 조건

이 프로젝트에서는 관상동맥질환(Coronary Artery Disease, CAD) 분류 모델을 개발하기 위해 **UCI Machine Learning Repository의 Extension of Z-Alizadeh Sani 데이터셋**을 사용했습니다.

임상정보와 검사 결과를 바탕으로 CAD 여부를 분류하는 데이터셋으로, 총 303명의 환자 기록을 포함하고 있습니다.

## 1. 사용 데이터셋

| 항목 | 내용 |
|---|---|
| 데이터셋 | Extension of Z-Alizadeh Sani |
| 제공 기관 | UCI Machine Learning Repository |
| 데이터 유형 | 임상정보 및 검사 결과 |
| 전체 데이터 | 303명 |
| 예측 대상 | CAD / Normal |
| Dataset ID | 411 |
| 라이선스 | CC BY 4.0 |

- [UCI 데이터셋 공식 페이지](https://archive.ics.uci.edu/dataset/411/extention+of+z+alizadeh+sani+dataset)
- [데이터셋 DOI: 10.24432/C5461K](https://doi.org/10.24432/C5461K)

### 데이터 구성

데이터셋에는 환자의 기본 정보와 증상, 검사 결과, 심전도 및 혈액검사 관련 변수 등이 포함되어 있습니다.

CAD 여부를 예측하기 위해 `Cath` 변수를 Target으로 사용했습니다.

- **Normal (0):** 관상동맥질환이 없는 경우
- **CAD (1):** 관상동맥질환이 있는 경우

전처리 과정에서는 예측 결과와 직접적인 관련이 있는 `LAD`, `LCX`, `RCA` 변수를 입력에서 제외했습니다.

이 변수들은 관상동맥의 협착 결과와 연결되어 있어, CAD 분류 모델의 입력에 그대로 사용하면 데이터 누수가 발생할 수 있다고 판단했기 때문입니다.

이후 범주형 변수 인코딩과 데이터 전처리를 거쳐 머신러닝 모델 학습에 활용했습니다.

자세한 전처리 과정은 [실험 과정 및 모델 검증](experiments.md)에 정리했습니다.

---

## 2. 데이터 이용 조건

해당 데이터셋은 **Creative Commons Attribution 4.0 International (CC BY 4.0)** 라이선스로 제공됩니다.

CC BY 4.0은 적절한 출처 표시와 변경 사항 안내 등의 조건을 지키는 경우, 상업적 목적을 포함한 데이터 공유와 수정·활용을 허용하는 라이선스입니다.

자세한 내용은 아래 공식 문서에서 확인할 수 있습니다.

- [CC BY 4.0 라이선스 안내](https://creativecommons.org/licenses/by/4.0/)
- [CC BY 4.0 전문](https://creativecommons.org/licenses/by/4.0/legalcode.en)

다만 데이터셋 라이선스가 개인정보 보호와 관련된 모든 권리까지 허용하는 것은 아닙니다.

이 프로젝트에서는 원본 임상 데이터 대신 실험 코드와 집계된 평가 결과를 중심으로 공개했습니다.

또한 데이터셋의 CC BY 4.0 라이선스가 프로젝트 코드나 사용한 외부 라이브러리의 라이선스를 자동으로 결정하는 것은 아닙니다.

---

## 3. 데이터 인용

본 프로젝트에서 사용한 데이터셋의 UCI 공식 권장 인용 정보는 다음과 같습니다.

**Alizadehsani, R., Roshanzamir, M., & Sani, Z. (2013).** *extention of Z-Alizadeh sani dataset* [Dataset]. UCI Machine Learning Repository.

DOI: https://doi.org/10.24432/C5461K

데이터셋을 제공한 원저작자의 기여를 명시하며, 프로젝트의 분석과 모델 개발 결과는 해당 데이터셋을 활용한 별도의 실험입니다.

---

## 4. 실험 데이터와 공개 범위

실험에서는 Extension of Z-Alizadeh Sani 데이터를 전처리한 뒤 여러 분류 모델을 학습하고 비교했습니다.

사용한 데이터와 공개 자료의 범위는 다음과 같습니다.

| 구분 | 공개 여부 |
|---|---|
| 데이터 전처리 및 모델 학습 코드 | 공개 |
| 모델별 집계 평가 결과 | 공개 |
| 성능 비교 그래프 | 공개 |
| 원본 임상 데이터 파일 | 미포함 |
| 환자별 예측 결과 | 미포함 |
| 학습된 모델 파일 | 미포함 |

실험 당시 사용한 Excel 파일과 UCI 공식 배포 파일의 바이트 단위 동일성은 별도로 확인하지 않았습니다. 따라서 정확한 파일 버전까지 일치한다고 단정하지는 않습니다.

공개된 집계 결과는 기존 실험 기록을 바탕으로 정리했으며, 전체 데이터와 학습 환경을 사용한 독립적인 모델 재현 검증은 수행하지 않았습니다.

---

### 관련 문서

- [프로젝트 소개](../README.md)
- [실험 과정 및 검증 방법](experiments.md)
- [모델 평가 결과](../results/README.md)
- [실험 환경](environment.md)
