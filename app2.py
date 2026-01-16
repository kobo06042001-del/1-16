import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import platform
import os

# 1. 한글 폰트 설정 함수 (기존 틀 유지하되 로직 개선)
def setup_korean_font():
    if platform.system() == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif platform.system() == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        plt.rcParams['font.family'] = 'NanumGothic'
    
    plt.rcParams['axes.unicode_minus'] = False

setup_korean_font()

# 앱 설정 및 제목
st.set_page_config(page_title="무역 데이터 시각화", layout="wide")
st.title("📈 주요 국가별 무역 규모 데이터 분석")

# 2. 데이터 생성 (인덱스 1번부터 시작 설정 유지)
data = {
    "구분": ["중국", "미국", "베트남", "일본", "인도네시아", "홍콩", "대만"],
    "2017": [2216.2, 1557.0, 1419.9, 688.6, 520.6, 559.7, 491.2],
    "2018": [2417.4, 1676.9, 1524.8, 735.5, 572.6, 613.3, 532.9],
    "2019": [2386.6, 1655.1, 1459.8, 695.2, 548.9, 596.4, 513.8],
    "2020": [2510.0, 1432.2, 1356.9, 630.5, 525.0, 505.1, 472.1],
    "2021": [3215.9, 1761.4, 1617.0, 749.2, 647.9, 620.2, 584.7]
}
df = pd.DataFrame(data)
df.index = range(1, len(df) + 1)

st.subheader("📊 데이터 요약 (단위: 100만 달러 추정)")
st.dataframe(df, use_container_width=True)

# 데이터 재구조화 (시각화용)
df_melted = df.melt(id_vars=['구분'], var_name='연도', value_name='규모')
st.divider()

# 3. 레이아웃 설정 (사이드바 형태의 컬럼 구조 유지)
col1, col2 = st.columns([1, 3])
with col1:
    chart_type = st.radio("그래프 종류:", ["선 그래프 (추이)", "막대 그래프 (비교)"])
    selected = st.multiselect("국가 선택:", df["구분"].tolist(), default=df["구분"].tolist())

filtered_df = df_melted[df_melted["구분"].isin(selected)]

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 그래프 타입 분기
    if chart_type == "선 그래프 (추이)":
        sns.lineplot(data=filtered_df, x="연도", y="규모", hue="구분", marker="o", ax=ax)
        ax.set_title("연도별 무역 규모 변화 추이", fontsize=16, pad=20)
    else:
        sns.barplot(data=filtered_df, x="연도", y="규모", hue="구분", ax=ax)
        ax.set_title("연도별/국가별 무역 규모 비교", fontsize=16, pad=20)

    # 축 레이블 한글 설정 확인
    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("규모 (100만 달러)", fontsize=12)
    ax.legend(title="국가명", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    st.pyplot(fig)