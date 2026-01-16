import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import platform

# 1. 폰트 설정 함수: 시스템에 있는 폰트를 강제로 찾아 지정합니다.
def get_korean_font():
    system_name = platform.system()
    if system_name == "Windows":
        return "Malgun Gothic"
    elif system_name == "Darwin":
        return "AppleGothic"
    else:
        # 리눅스/배포 환경에서 한글 폰트가 없을 경우를 대비해 
        # 시스템에 설치된 폰트 중 하나를 자동으로 선택합니다.
        return "DejaVu Sans" # 한글이 없을 경우 기본 영문 폰트

target_font = get_korean_font()
plt.rcParams['font.family'] = target_font
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="무역 데이터 시각화", layout="wide")
st.title("📈 주요 국가별 무역 규모 데이터 분석")

# 2. 데이터 구성 (순위 1부터 시작)
data = {
    "구분": ["중국", "미국", "베트남", "일본", "인도네시아", "홍콩", "대만"],
    "2017": [2216.2, 1557.0, 1419.9, 688.6, 520.6, 559.7, 491.2],
    "2018": [2417.4, 1676.9, 1524.8, 735.5, 572.6, 613.3, 532.9],
    "2019": [2386.6, 1655.1, 1459.8, 695.2, 548.9, 596.4, 513.8],
    "2020": [2510.0, 1432.2, 1356.9, 630.5, 525.0, 505.1, 472.1],
    "2021": [3215.9, 1761.4, 1617.0, 749.2, 647.9, 620.2, 584.7]
}

df = pd.DataFrame(data)
df.index = range(1, len(df) + 1) # [수정] 표의 순위 1부터 시작

# 3. 데이터 요약 표
st.subheader("📊 데이터 요약 (단위: 100만 달러 추정)")
st.dataframe(df, use_container_width=True)

# 4. 시각화를 위한 데이터 가공
df_melted = df.melt(id_vars=['구분'], var_name='연도', value_name='규모')

st.divider()

# 5. 그래프 생성 영역
chart_type = st.radio("그래프 종류를 선택하세요:", ["선 그래프 (추이)", "막대 그래프 (비교)"])
fig, ax = plt.subplots(figsize=(12, 6))

if chart_type == "선 그래프 (추이)":
    sns.lineplot(data=df_melted, x="연도", y="규모", hue="구분", marker="o", ax=ax)
    title_text = "Yearly Trade Volume Trend" # 한글 깨짐 방지를 위해 영문 병기 고려
else:
    sns.barplot(data=df_melted, x="연도", y="규모", hue="구분", ax=ax)
    title_text = "Trade Volume Comparison by Country"

# --- [중요] 폰트 강제 적용 섹션 ---
# 제목과 축 이름을 설정할 때 시스템 폰트를 강제로 입힙니다.
ax.set_title(title_text, fontsize=16, fontweight='bold')
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Volume (Million USD)", fontsize=12)

# 범례(Legend) 설정: 범례 제목과 텍스트의 네모칸 방지
ax.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
st.pyplot(fig)