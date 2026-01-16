import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. 페이지 설정
st.set_page_config(page_title="국가별 무역지표 분석", layout="wide")

# 2. 폰트 설정 (에러 방지 강화)
def setup_korean_font():
    font_name = "sans-serif" # 기본값
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "NanumGothic.ttf")
    
    # 파일이 존재하고 정상적인지 확인
    if os.path.exists(font_path):
        try:
            # 폰트 등록 시도
            fe = fm.FontEntry(fname=font_path, name='NanumGothic')
            fm.fontManager.ttflist.insert(0, fe)
            plt.rc('font', family='NanumGothic')
            font_name = 'NanumGothic'
        except Exception as e:
            # 폰트 로드 실패 시 시스템 기본 폰트 사용 (에러 방지)
            st.warning(f"나눔고딕 로드 실패: {e}. 시스템 기본 폰트를 사용합니다.")
            plt.rc('font', family='sans-serif')
    else:
        st.info("NanumGothic.ttf 파일이 없어 기본 폰트를 사용합니다.")
        plt.rc('font', family='sans-serif')
        
    plt.rcParams['axes.unicode_minus'] = False
    return font_name

target_font = setup_korean_font()

# 3. 데이터 로드 (캐싱)
@st.cache_data
def load_data():
    file_path = '한국무역보험공사_국가별 무역지표.csv'
    if not os.path.exists(file_path):
        return None
    
    try:
        return pd.read_csv(file_path, encoding='cp949')
    except:
        return pd.read_csv(file_path, encoding='utf-8')

df = load_data()

# 4. 화면 구성
st.title("📈 국가별 무역지표 분석")

if df is not None:
    # 사이드바 설정
    st.sidebar.header("설정")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    selected_metrics = st.sidebar.multiselect("확인할 지표", numeric_cols, default=numeric_cols[:1])
    
    # 데이터 표
    st.subheader("데이터 미리보기")
    st.dataframe(df.head(20), use_container_width=True)

    # 시각화
    if selected_metrics:
        st.subheader("지표 비교 그래프")
        
        # 국가명 컬럼 찾기
        country_col = '국가명' if '국가명' in df.columns else df.columns[0]
        chart_data = df.head(10).set_index(country_col)

        fig, ax = plt.subplots(figsize=(10, 5))
        chart_data[selected_metrics].plot(kind='bar', ax=ax)
        
        # 폰트가 지정된 경우만 타이틀 한글 적용
        ax.set_title("국가별 무역 지표 비교", fontsize=15)
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.error("파일을 찾을 수 없습니다. '한국무역보험공사_국가별 무역지표.csv' 파일이 같은 폴더에 있는지 확인해주세요.")