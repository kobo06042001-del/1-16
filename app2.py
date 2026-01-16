import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 1. 시스템별 한글 폰트 설정 (그래프 네모칸 방지)
def set_korean_font():
    system_name = platform.system()
    if system_name == "Windows":
        # 윈도우: 맑은 고딕
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system_name == "Darwin":
        # 맥: 애플 고딕
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        # 리눅스/배포환경: 나눔 고딕 시도
        plt.rcParams['font.family'] = 'NanumGothic'
    
    # 그래프에서 마이너스 기호가 깨지는 현상 방지
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.set_page_config(page_title="무역 데이터 시각화", layout="wide")
st.title("📈 주요 국가별 무역 규모 데이터 분석")

# 2. 데이터 생성 (보내주신 이미지의 데이터 기반)
data = {
    "구분": ["중국", "미국", "베트남", "일본", "인도네시아", "홍콩", "대만"],
    "2017": [2216.2, 1557.0, 1419.9, 688.6, 520.6, 559.7, 491.2],
    "2018": [2417.4, 1676.9, 1524.8, 735.5, 572.6, 613.3, 532.9],
    "2019": [2386.6, 1655.1, 1459.8, 695.2, 548.9, 596.4, 513.8],
    "2020": [2510.0, 1432.2, 1356.9, 630.5, 525.0, 505.1, 472.1],
    "2021": [3215.9, 1761.4, 1617.0, 749.2, 647.9, 620.2, 584.7]
}

df = pd.DataFrame(data)

# [해결 1] 첫 번째 사진의 인덱스 0을 1부터 시작하도록 수정
df.index = range(1, len(df) + 1)

# 3. 데이터 요약 출력
st.subheader("📊 데이터 요약 (단위: 100만 달러 추정)")
st.dataframe(df, use_container_width=True)

# 4. 시각화 준비 (데이터 변환)
df_melted = df.melt(id_vars=['구분'], var_name='연도', value_name='규모')

st.divider()

# 5. 시각화 영역
col1, col2 = st.columns([1, 3])

with col1:
    chart_type = st.radio("그래프 종류를 선택하세요:", ["선 그래프 (추이)", "막대 그래프 (비교)"])
    selected_countries = st.multiselect("분석할 국가를 선택하세요:", 
                                        df["구분"].tolist(), 
                                        default=df["구분"].tolist())

# 선택한 국가만 필터링
filtered_df = df_melted[df_melted["구분"].isin(selected_countries)]

with col2:
    # [해결 2] 그래프 내부의 한글(네모칸) 해결을 위해 폰트 설정 재확인
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if chart_type == "선 그래프 (추이)":
        sns.lineplot(data=filtered_df, x="연도", y="규모", hue="구분", marker="o", linewidth=2, ax=ax)
        ax.set_title("연도별 무역 규모 변화 추이", fontsize=16, pad=20)
    else:
        sns.barplot(data=filtered_df, x="연도", y="규모", hue="구분", ax=ax)
        ax.set_title("연도별/국가별 무역 규모 비교", fontsize=16, pad=20)

    # 축 이름 한글 설정
    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("무역 규모 (100만 달러)", fontsize=12)
    
    # [해결 3] 범례(Legend) 국가명 한글 깨짐 해결
    ax.legend(title="국가명", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

st.info("💡 이제 왼쪽 표는 1번부터 시작하며, 그래프의 제목과 국가명도 한글로 정상 표시됩니다.")