import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import chardet
import platform

# 1. OS별 한글 폰트 설정 (Windows/Mac/Linux 대응)
def set_korean_font():
    system_name = platform.system()
    if system_name == "Windows":
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system_name == "Darwin":  # Mac
        plt.rcParams['font.family'] = 'AppleGothic'
    else:  # Linux (Streamlit Cloud 등)
        # 리눅스의 경우 별도의 폰트 설치가 필요할 수 있으나, 기본적으로 Nanum 등을 시도합니다.
        plt.rcParams['font.family'] = 'NanumGothic'
    
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.set_page_config(page_title="국세청 데이터 분석기", layout="wide")
st.title("🪙 국세청 근로소득 데이터 분석기")

file_path = "income.csv"

# 2. 데이터 로드 함수 개선
@st.cache_data # 성능 최적화: 매번 파일을 다시 읽지 않음
def load_data(path):
    try:
        with open(path, 'rb') as f:
            raw_data = f.read(100000) # 샘플링 크기 상향
            result = chardet.detect(raw_data)
            detected_enc = result['encoding']
        
        # 'utf-8-sig'는 엑셀 저장 시 발생하는 BOM 문제를 해결해줍니다.
        encodings = ['utf-8-sig', 'cp949', 'euc-kr', detected_enc, 'utf-8']
        
        for enc in encodings:
            if enc is None: continue
            try:
                df = pd.read_csv(path, encoding=enc, thousands=',')
                return df, enc
            except:
                continue
    except Exception as e:
        st.error(f"파일 로드 오류: {e}")
    return None, None

try:
    df, used_enc = load_data(file_path)

    if df is not None:
        # --- [컬럼 정제 로직 개선] ---
        df = df.dropna(axis=1, how='all')

        new_cols = []
        counts = {}
        
        for col in df.columns:
            # 1. 문자열 변환 및 공백 제거
            clean_name = str(col).strip()
            # 2. 정규표현식: 한글, 영어, 숫자만 남기고 특수문자 제거
            # [^a-zA-Z0-9가-힣] -> 해당 문자가 아닌 것들은 제거
            import re
            clean_name = re.sub(r'[^a-zA-Z0-9가-힣\s]', '', clean_name)
            
            if not clean_name:
                clean_name = "미정의항목"
            
            # 중복 이름 처리
            if clean_name in counts:
                counts[clean_name] += 1
                new_cols.append(f"{clean_name}_{counts[clean_name]}")
            else:
                counts[clean_name] = 0
                new_cols.append(clean_name)
        
        df.columns = new_cols

        # 3. 데이터 내용 정제 (숫자 변환 및 결측치 처리)
        for col in df.columns:
            if df[col].dtype == 'object':
                # %와 콤마 제거 후 숫자 변환 시도
                cleaned_series = df[col].astype(str).str.replace(r'[%,]', '', regex=True).str.strip()
                # 빈 문자열을 NaN으로 변경
                cleaned_series = cleaned_series.replace('', np.nan)
                converted = pd.to_numeric(cleaned_series, errors='coerce')
                
                # 변환 성공률이 50% 이상이면 숫자 컬럼으로 확정
                if converted.notna().sum() > (len(df) * 0.5):
                    df[col] = converted

        st.success(f"✅ 데이터를 성공적으로 분석했습니다. (인코딩: {used_enc})")

        # 4. 데이터 확인 및 시각화
        st.subheader("📊 데이터 확인하기")
        st.dataframe(df.head(10))

        st.divider()
        st.subheader("📈 항목별 분포 그래프")
        
        # 사용자 선택
        selected_col = st.selectbox("분석할 항목을 선택하세요:", df.columns.tolist())
        final_series = df[selected_col].dropna() # 결측치 제외 후 시각화
        
        fig, ax = plt.subplots(figsize=(10, 6))

        if pd.api.types.is_numeric_dtype(final_series):
            sns.histplot(final_series, ax=ax, color="#cc00ff", kde=True)
            ax.set_title(f"<{selected_col}> 수치 분포 분석", fontsize=15, pad=20)
        else:
            top_values = final_series.value_counts().head(20)
            if not top_values.empty:
                sns.barplot(x=top_values.index, y=top_values.values, ax=ax, palette="viridis")
                ax.set_title(f"<{selected_col}> 빈도 분석 (상위 20개)", fontsize=15, pad=20)
            else:
                st.warning("표시할 데이터가 없습니다.")

        plt.xticks(rotation=45)
        plt.ylabel("빈도/수치")
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        
        # 여백 자동 조정 (라벨 잘림 방지)
        plt.tight_layout()
        st.pyplot(fig)

    else:
        st.error("❌ 'income.csv' 파일을 찾을 수 없거나 읽을 수 없습니다. 파일명을 확인해주세요.")

except Exception as e:
    st.error(f"❌ 분석 중 오류 발생: {e}")
    # 상세 오류 디버깅용
    st.exception(e)