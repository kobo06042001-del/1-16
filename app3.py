import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# 1. 나눔고딕 폰트 로드 및 설정 (피드백 반영)
font_path = "NanumGothic.ttf"

@st.cache_resource
def configure_font(path):
    if os.path.exists(path):
        # 폰트 등록
        fm.fontManager.addfont(path)
        prop = fm.FontProperties(fname=path)
        # Matplotlib 전역 설정에 나눔고딕 적용
        plt.rcParams['font.family'] = prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        return prop
    else:
        return None

font_prop = configure_font(font_path)

st.set_page_config(page_title="무역 데이터 시각화", layout="wide")
st.title("📈 주요 국가별 무역 규모 데이터 분석")

# 2. 데이터 구성
data = {
    "구분": ["중국", "미국", "베트남", "일본", "인도네시아", "홍콩", "대만"],
    "2017": [2216.2, 1557.0, 1419.9, 688.6, 520.6, 559.7, 491.2],
    "2018": [2417.4, 1676.9, 1524.8, 735.5, 572.6, 613.3, 532.9],
    "2019": [2386.6, 1655.1, 1459.8, 695.2, 548.9, 596.4, 513.8],
    "2020": [2510.0, 1432.2, 1356.9, 630.5, 525.0, 505.1, 472.1],
    "2021": [3215.9, 1761.4, 1617.0, 749.2, 647.9, 620.2, 584.7]
}

df = pd.DataFrame(data)

# [수정] 이미지에서 0부터 시작하던 순위를 1부터 시작하도록 변경
df.index = range(1, len(df) + 1)

# 3. 데이터 요약 표 출력
st.subheader("📊 데이터 요약 (단위: 100만 달러 추정)")
st.dataframe(df, use_container_width=True)

# 4. 시각화 데이터 가공
df_melted = df.melt(id_vars=['구분'], var_name='연도', value_name='규모')

st.divider()

# 5. 시각화 영역
col1, col2 = st.columns([1, 3])

with col1:
    chart_type = st.radio("그래프 종류를 선택하세요:", ["선 그래프 (추이)", "막대 그래프 (비교)"])
    selected_countries = st.multiselect("분석할 국가를 선택하세요:", 
                                        df["구분"].unique(), 
                                        default=df["구분"].unique())

filtered_df = df_melted[df_melted["구분"].isin(selected_countries)]

with col2:
    if font_prop:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if chart_type == "선 그래프 (추이)":
            sns.lineplot(data=filtered_df, x="연도", y="규모", hue="구분", marker="o", ax=ax)
            ax.set_title("연도별 무역 규모 변화 추이", fontsize=18, pad=20)
        else:
            sns.barplot(data=filtered_df, x="연도", y="규모", hue="구분", ax=ax)
            ax.set_title("연도별/국가별 무역 규모 비교", fontsize=18, pad=20)

        # 개별 요소에 폰트 재차 확인 적용
        ax.set_xlabel("연도", fontsize=12)
        ax.set_ylabel("규모 (100만 달러)", fontsize=12)
        
        # 범례 설정
        legend = ax.legend(title="국가", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        st.pyplot(fig)
    else:
        # 폰트 파일이 없을 경우 경고 메시지 출력
        st.error(f"🚨 '{font_path}' 파일을 찾을 수 없습니다. 파일을 파이썬 코드와 같은 폴더에 넣어주세요.")
        st.info("파일이 준비되기 전까지는 그래프의 한글이 네모칸으로 보일 수 있습니다.")

st.info("💡 폰트 파일을 직접 로드하여 모든 환경에서 네모칸 현상을 방지하고, 순위는 1번부터 표시됩니다.")