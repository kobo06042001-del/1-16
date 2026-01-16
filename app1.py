import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import chardet

# 1. 한글 폰트 및 마이너스 기호 설정 (Windows 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="국세청 데이터 분석기", layout="wide")
st.title("🪙 국세청 근로소득 데이터 분석기")

file_path = "income.csv"

def load_data(path):
    # 파일 인코딩 감지
    with open(path, 'rb') as f:
        raw_data = f.read(20000)
        result = chardet.detect(raw_data)
        detected_enc = result['encoding']
    
    # 한글 깨짐 방지를 위한 인코딩 순차 시도
    encodings = ['utf-8-sig', 'cp949', 'euc-kr', detected_enc]
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            return df, enc
        except:
            continue
    return None, None

try:
    df, used_enc = load_data(file_path)

    if df is not None:
        # 2. 데이터 정제 (열 이름 및 내용 깨짐/특수문자 방지)
        df.columns = [str(col).strip() for col in df.columns] # 컬럼명 공백 제거

        for col in df.columns:
            if df[col].dtype == 'object':
                # 문자열 내 공백, 쉼표, 퍼센트 제거
                df[col] = df[col].astype(str).str.replace(r'[%, ]', '', regex=True)
                # 숫자로 변환 (변환 불가능한 '0.1' 같은 값들을 위해 errors='coerce' 사용 가능하나 여기선 유지)
                df[col] = pd.to_numeric(df[col], errors='ignore')

        st.success(f"✅ 데이터를 불러왔습니다. (적용 인코딩: {used_enc})")

        # 데이터 미리보기
        st.subheader("📊 데이터 확인하기")
        st.dataframe(df.head(10))

        # 3. 항목별 분석 그래프
        st.divider()
        st.subheader("📈 항목별 분포 그래프")
        
        column_names = df.columns.tolist()
        selected_col = st.selectbox("분석할 항목을 선택하세요:", column_names)

        # 그래프 영역 생성
        fig, ax = plt.subplots(figsize=(10, 5))

        # 선택한 데이터가 숫자인지 문자인지에 따라 그래프 종류 자동 변경
        if np.issubdtype(df[selected_col].dtype, np.number):
            sns.histplot(df[selected_col], ax=ax, color="#cc00ff", kde=True)
            ax.set_title(f"[{selected_col}] 수치 분포 분석", fontsize=15)
        else:
            # 텍스트 데이터인 경우 상위 15개 빈도 출력
            df[selected_col].value_counts().head(15).plot(kind='bar', ax=ax, color="#cc00ff")
            ax.set_title(f"[{selected_col}] 항목별 빈도 (상위 15개)", fontsize=15)

        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        st.pyplot(fig)

    else:
        st.error("❌ 파일 인코딩을 판별할 수 없습니다. 파일을 다시 확인해 주세요.")

except FileNotFoundError:
    st.error(f"🚨 '{file_path}' 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
except Exception as e:
    st.error(f"❌ 분석 중 오류가 발생했습니다: {e}")