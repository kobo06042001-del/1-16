import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# [핵심] 윈도우 절대 경로 설정 (r을 붙여 역슬래시 인식 오류 방지)
font_path = r"C:\python_prep\1-16\fonts\NanumGothic.ttf"

@st.cache_resource
def setup_korean_font(path):
    if os.path.exists(path):
        fm.fontManager.addfont(path)
        prop = fm.FontProperties(fname=path)
        plt.rcParams['font.family'] = prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        return prop
    return None

font_prop = setup_korean_font(font_path)

st.set_page_config(page_title="무역 데이터 시각화", layout="wide")
st.title("📈 주요 국가별 무역 규모 데이터 분석")

# 데이터 생성 및 순위 1번부터 시작 설정
data = {
    "구분": ["중국", "미국", "베트남", "일본", "인도네시아", "홍콩", "대만"],
    "2017": [2216.2, 1557.0, 1419.9, 688.6, 520.6, 559.7, 491.2],
    "2018": [2417.4, 1676.9, 1524.8, 735.5, 572.6, 613.3, 532.9],
    "2019": [2386.6, 1655.1, 1459.8, 695.2, 548.9, 596.4, 513.8],
    "2020": [2510.0, 1432.2, 1356.9, 630.5, 525.0, 505.1, 472.1],
    "2021": [3215.9, 1761.4, 1617.0, 749.2, 647.9, 620.2, 584.7]
}
df = pd.DataFrame(data)
df.index = range(1, len(df) + 1) # 인덱스 1부터 시작

st.subheader("📊 데이터 요약 (단위: 100만 달러 추정)")
st.dataframe(df, use_container_width=True)

df_melted = df.melt(id_vars=['구분'], var_name='연도', value_name='규모')
st.divider()

col1, col2 = st.columns([1, 3])
with col1:
    chart_type = st.radio("그래프 종류:", ["선 그래프 (추이)", "막대 그래프 (비교)"])
    selected = st.multiselect("국가 선택:", df["구분"].tolist(), default=df["구분"].tolist())

filtered_df = df_melted[df_melted["구분"].isin(selected)]

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "선 그래프 (추이)":
        sns.lineplot(data=filtered_df, x="연도", y="규모", hue="구분", marker="o", ax=ax)
        ax.set_title("연도별 무역 규모 변화 추이", fontsize=16, pad=20)
    else:
        sns.barplot(data=filtered_df, x="연도", y="규모", hue="구분", ax=ax)
        ax.set_title("연도별/국가별 무역 규모 비교", fontsize=16, pad=20)

    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("규모 (100만 달러)", fontsize=12)
    ax.legend(title="국가명", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    if not font_prop:
        st.error(f"🚨 폰트 파일을 찾을 수 없습니다: {font_path}") # 경로 오류 발생 시 경고
    
    plt.tight_layout()
    st.pyplot(fig)