import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 1. 그래프 한글 및 스타일 설정
def set_korean_font():
    system_name = platform.system()
    if system_name == "Windows":
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system_name == "Darwin":  # Mac
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_theme(style="whitegrid", font=plt.rcParams['font.family'])

set_korean_font()

st.set_page_config(page_title="MLB 유격수 종합 분석", layout="wide")
st.title("⚾ MLB 역대 유격수 주요 기록 종합 분석")
st.markdown("홈런, 타점, 안타, 도루, 2루타 데이터를 통해 전설적인 유격수들을 비교합니다.")

# 2. 확장된 데이터 구성 (StatMuse 기반 데이터)
data = {
    "선수명": ["Cal Ripken Jr.", "Alex Rodriguez", "Ernie Banks", "Miguel Tejada", "Francisco Lindor", "Derek Jeter", "Jimmy Rollins", "Hanley Ramirez", "Vern Stephens", "Trevor Story"],
    "홈런(HR)": [353, 345, 298, 285, 279, 260, 245, 230, 213, 174],
    "타점(RBI)": [1369, 990, 858, 1185, 856, 1073, 936, 755, 829, 534],
    "안타(H)": [2631, 1435, 1378, 2035, 1502, 3034, 2195, 1332, 1104, 895],
    "도루(SB)": [32, 218, 50, 68, 176, 358, 470, 262, 10, 118],
    "2루타(2B)": [521, 235, 218, 407, 290, 487, 447, 268, 176, 175]
}

df = pd.DataFrame(data)

# [수정] 순위 1부터 시작하게 설정
df.index = range(1, len(df) + 1)

# 3. 데이터 요약 표
st.subheader("📊 역대 유격수 주요 기록표 (Top 10)")
st.dataframe(df, use_container_width=True)

st.divider()

# 4. 시각화 분석 컨트롤러
col1, col2 = st.columns([1, 3])

with col1:
    st.write("### 🛠 그래프 컨트롤러")
    
    # 1. 그래프 형태 선택
    chart_type = st.radio(
        "그래프 형태를 고르세요:",
        ["꺾은선 그래프 (추이)", "누적 막대 그래프 (전체 합계)", "개별 막대 그래프 (비교)"]
    )
    
    # 2. 데이터 지표 선택 (개별 막대/꺾은선용)
    metrics = ["홈런(HR)", "타점(RBI)", "안타(H)", "도루(SB)", "2루타(2B)"]
    selected_metric = st.selectbox("분석할 지표 선택:", metrics)
    
    # 3. 선수 필터링
    num_players = st.slider("표시할 선수 인원:", 5, 10, 10)
    chart_data = df.head(num_players)

with col2:
    fig, ax = plt.subplots(figsize=(12, 7))
    
    if chart_type == "꺾은선 그래프 (추이)":
        # 꺾은선 그래프: 기록의 고저차를 한눈에 확인
        sns.lineplot(data=chart_data, x="선수명", y=selected_metric, marker="D", 
                     markersize=12, color="#1f77b4", linewidth=3, ax=ax)
        ax.set_title(f"선수별 {selected_metric} 기록 변화", fontsize=18, pad=20)
        
    elif chart_type == "누적 막대 그래프 (전체 합계)":
        # 모든 지표를 쌓아서 선수의 '종합적인 생산성' 확인
        chart_data.plot(kind='bar', x='선수명', stacked=True, ax=ax, colormap='viridis')
        ax.set_title("전체 지표 누적 비교 (종합 생산성)", fontsize=18, pad=20)
        ax.legend(title="기록 항목", bbox_to_anchor=(1.05, 1), loc='upper left')
        
    elif chart_type == "개별 막대 그래프 (비교)":
        sns.barplot(data=chart_data, x="선수명", y=selected_metric, palette="coolwarm", ax=ax)
        ax.set_title(f"선수별 {selected_metric} 단순 비교", fontsize=18, pad=20)

    # 공통 레이아웃 보정
    plt.xticks(rotation=45)
    plt.ylabel(selected_metric if chart_type != "누적 막대 그래프 (전체 합계)" else "기록 합계")
    plt.tight_layout()
    st.pyplot(fig)

# 5. 하단 인사이트 레이블
max_val = df[selected_metric].max()
top_player = df.loc[df[selected_metric].idxmax(), '선수명']

st.success(f"💡 **{selected_metric}** 부문 최고 기록은 **{top_player}** 선수의 **{max_val}**개 입니다.")