import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import glob

# 1. 페이지 설정
st.set_page_config(page_title="국가별 무역지표 분석", layout="wide")

# 2. 폰트 설정 (에러 방지 최적화)
@st.cache_resource
def setup_korean_font():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "NanumGothic.ttf")
    
    if os.path.exists(font_path):
        try:
            fe = fm.FontEntry(fname=font_path, name='NanumGothic')
            fm.fontManager.ttflist.insert(0, fe)
            plt.rc('font', family='NanumGothic')
        except Exception:
            plt.rc('font', family='sans-serif')
    else:
        plt.rc('font', family='sans-serif')
    plt.rcParams['axes.unicode_minus'] = False

setup_korean_font()

# 3. 데이터 로드 (여러 연도 파일 통합)
@st.cache_data
def load_all_data():
    # '한국무역보험공사'로 시작하는 모든 csv 파일을 찾습니다.
    file_list = glob.glob('*.csv')
    all_df = []
    
    for file in file_list:
        try:
            # 파일명에서 연도 추출 (예: '2024_무역지표.csv' 등 파일명에 연도가 있다면 좋음)
            temp_df = pd.read_csv(file, encoding='cp949')
            # 파일명을 연도 구분용 컬럼으로 추가 (선택 사항)
            temp_df['출처파일명'] = file
            all_df.append(temp_df)
        except:
            try:
                temp_df = pd.read_csv(file, encoding='utf-8')
                temp_df['출처파일명'] = file
                all_df.append(temp_df)
            except:
                continue
    
    if not all_df:
        return None
    
    return pd.concat(all_df, ignore_index=True)

df = load_all_data()

# 4. 화면 구성
st.title("📈 국가별 무역지표 분석 (다년도 통합)")

if df is not None:
    # --- 순위 1부터 시작하도록 인덱스 조정 ---
    df.index = df.index + 1 
    
    # 사이드바 설정
    st.sidebar.header("설정")
    
    # 연도별/파일명별 필터 (파일이 여러 개일 경우)
    if '출처파일명' in df.columns:
        files = df['출처파일명'].unique()
        selected_file = st.sidebar.selectbox("데이터 파일 선택", files)
        filtered_df = df[df['출처파일명'] == selected_file]
    else:
        filtered_df = df

    numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
    selected_metrics = st.sidebar.multiselect("확인할 지표", numeric_cols, default=numeric_cols[:1])
    
    # 데이터 표 출력
    st.subheader(f"📊 {selected_file if '출처파일명' in df.columns else '무역'} 데이터 (순위 1부터 표시)")
    st.dataframe(filtered_df, use_container_width=True)

    # 시각화
    if selected_metrics:
        st.subheader("📉 지표 비교 그래프 (상위 10개)")
        
        country_col = '국가명' if '국가명' in filtered_df.columns else filtered_df.columns[0]
        # 시각화용 데이터 (상위 10개)
        chart_data = filtered_df.head(10).copy()
        chart_data = chart_data.set_index(country_col)

        fig, ax = plt.subplots(figsize=(10, 5))
        chart_data[selected_metrics].plot(kind='bar', ax=ax)
        
        ax.set_title("국가별 주요 무역 지표", fontsize=15)
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.error("CSV 파일을 찾을 수 없습니다. 프로젝트 폴더에 CSV 파일을 넣어주세요.")