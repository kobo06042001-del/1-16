import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# [1] 절대 경로 재설정 (r을 반드시 붙여주세요)
font_path = r"C:\python_prep\1-16\fonts\NanumGothic.ttf"

@st.cache_resource
def setup_font(path):
    if os.path.exists(path):
        # 시스템 폰트 매니저에 등록
        fm.fontManager.addfont(path)
        # 폰트 속성 객체 생성
        prop = fm.FontProperties(fname=path)
        # 전역 설정 (영향을 주지 못할 경우를 대비해 하단에서 개별 적용)
        plt.rcParams['font.family'] = prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        return prop
    return None

font_prop = setup_font(font_path)

st.title("📈 무역 규모 데이터 분석 (폰트 수정본)")

# 데이터 준비 및 인덱스 1부터 시작
data = {
    "구분": ["중국", "미국", "베트남", "일본", "인도네시아", "홍콩", "대만"],
    "2017": [2216.2, 1557.0, 1419.9, 688.6, 520.6, 559.7, 491.2],
    "2018": [2417.4, 1676.9, 1524.8, 735.5, 572.6, 613.3, 532.9],
    "2019": [2386.6, 1655.1, 1459.8, 695.2, 548.9, 596.4, 513.8],
    "2020": [2510.0, 1432.2, 1356.9, 630.5, 525.0, 505.1, 472.1],
    "2021": [3215.9, 1761.4, 1617.0, 749.2, 647.9, 620.2, 584.7]
}
df = pd.DataFrame(data)
df.index = range(1, len(df) + 1) #

st.dataframe(df, use_container_width=True)

# 시각화 로직
df_melted = df.melt(id_vars=['구분'], var_name='연도', value_name='규모')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_melted, x="연도", y="규모", hue="구분", marker="o", ax=ax)

# [2] 네모칸 해결의 핵심: 모든 텍스트 요소에 직접 fontproperties 적용
if font_prop:
    ax.set_title("연도별 무역 규모 변화 추이", fontproperties=font_prop, fontsize=16)
    ax.set_xlabel("연도", fontproperties=font_prop, fontsize=12)
    ax.set_ylabel("규모 (100만 달러)", fontproperties=font_prop, fontsize=12)
    
    # 범례(Legend) 한글 깨짐 방지
    legend = ax.legend(prop=font_prop, title="국가명")
    plt.setp(legend.get_title(), fontproperties=font_prop)
else:
    st.error(f"🚨 파일을 찾을 수 없습니다: {font_path}")

st.pyplot(fig)