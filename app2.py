import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# [핵심] 우선순위: (1) 프로젝트 내부 폰트(상대경로) → (2) 기존 절대경로 → (3) 시스템 폰트 fallback
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ 1) 프로젝트에 NanumGothic.ttf가 app2.py 옆에 있으면 이게 제일 안정적
local_font_1 = os.path.join(BASE_DIR, "NanumGothic.ttf")

# ✅ 2) 프로젝트에 fonts 폴더가 있으면 여기에 둘 수도 있음
local_font_2 = os.path.join(BASE_DIR, "fonts", "NanumGothic.ttf")

# ✅ 3) 네가 쓰던 절대경로(틀 유지)
abs_font = r"C:\python_prep\1-16\fonts\NanumGothic.ttf"

# 실제 사용할 폰트 경로 선택
font_path = next((p for p in [local_font_1, local_font_2, abs_font] if os.path.exists(p)), None)

@st.cache_resource
def setup_korean_font(path):
    """
    path가 있으면 해당 ttf를 matplotlib에 등록해서 사용.
    없으면 시스템 fallback 폰트(맑은 고딕 등)로라도 한글이 안 깨지게 설정.
    """
    if path and os.path.exists(path):
        fm.fontManager.addfont(path)
        prop = fm.FontProperties(fname=path)

        # ✅ 여기서 확실히 rcParams에 박아주기
        plt.rcParams["font.family"] = prop.get_name()
        plt.rcParams["axes.unicode_minus"] = False

        # seaborn도 결국 matplotlib 기반이라 이걸로 충분
        return prop, path

    # ✅ 폰트 파일이 없을 때도 한글 안 깨지게 "시스템 폰트 fallback"
    # (Windows: Malgun Gothic, Mac: AppleGothic)
    plt.rcParams["font.family"] = ["NanumGothic", "Malgun Gothic", "AppleGothic", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    return None, None

font_prop, used_font_path = setup_korean_font(font_path)

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
df.index = range(1, len(df) + 1)  # 인덱스 1부터 시작

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

    # ✅ 경고 메시지는 "사용한 폰트 경로" 기준으로 보여주기
    if not used_font_path:
        st.warning("⚠️ NanumGothic.ttf를 못 찾아서 시스템 폰트로 표시 중입니다. (한글은 깨지지 않아야 정상)")
    else:
        st.caption(f"✅ 적용된 폰트: {used_font_path}")

    plt.tight_layout()
    st.pyplot(fig)
