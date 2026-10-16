# 포트폴리오 카드

**프로젝트명:** 소규모 임상 데이터의 CAD 선별 모델

**한 줄 설명:** 누수 변수 제외와 Nested CV로 RF를 비교·선정하고, 확률 보정과 모델 저장·복원의 일관성을 살펴본 개인 실험.

**핵심 성과**

1. 개발 303명의 outer10/inner5 Nested RF pooled OOF에서 sensitivity 0.9537, specificity 0.6897, AUROC 0.9278을 기록했습니다. 독립 외부 검증과 구분한 내부 평가입니다.
2. 별도 최종 구성용 5-fold OOF에서 Sigmoid 보정으로 Brier 0.1245→0.1015, ECE 0.1567→0.0501을 개선했습니다. 최종 모델의 저장 전후 threshold 판정은 일치했으며 Mock 추론은 미완료로 남겼습니다.

**기술 스택:** Python, pandas, NumPy, scikit-learn, XGBoost, TensorFlow/Keras, joblib, Matplotlib, Nested Cross-Validation, Probability Calibration.

**대표 이미지:** `figures/portfolio_cover.png`

**대안:** `figures/calibration_comparison.png` — 확률 보정의 판단 과정을 강조할 때 사용합니다.

Nested와 최종 구성용 OOF를 하나의 성능으로 합치지 않습니다. LR/SVM Nested 비교는 PDF 근거만이며 실제 개인 구현은 별도로 확보하지 않았습니다.
