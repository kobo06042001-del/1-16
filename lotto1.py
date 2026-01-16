import streamlit as st  
import random
import datetime


st.title("로또 번호 생성기")


def generate_lotto():
    lotto = set()
    while len(lotto) < 6:
        number= random.randint(1, 45)
        lotto.add(number)


    return lotto


button = st.button("로또 번호 생성하기")


if button:
    for i in range(1,6) :
        st. subheader(f"{i}번째 추천 로또 번호:{generate_lotto()}")
    st.write(f"생성된 시각 : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")