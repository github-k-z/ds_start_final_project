import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_data():
    data = pd.read_csv("data/tab3-zpl_2000-2023.csv")
    data.columns = pd.Index(['type']).append(data.columns[1:])
    inflation_data = pd.read_csv("data/inflation.csv")
    vvp = pd.read_csv("data/VVP.csv")
    return data, inflation_data, vvp


st.set_page_config(layout="wide")

data, inflation_data, vvp = load_data()

selected_types = ["Образование", "Обрабатывающие производства", "Здравоохранение и предоставление социальных услуг"]

years = [str(i) for i in range(2000, 2024)]
selected_with_inflation = [[], [], []]
for i in range(1, len(years)):
    for j in range(3):
        nzpg = data.loc[data["type"] == selected_types[j], years[i - 1]].values[0]
        nztg = data.loc[data["type"] == selected_types[j], years[i]].values[0]
        inf = inflation_data.loc[inflation_data["Год"] == int(years[i - 1]), "Всего"].values[0]
        selected_with_inflation[j].append(nzpg * (nztg / nzpg * 100) / (100 + inf))



st.title("Анализ номинальной и реальной зарплат в России")
st.write("Под реальной зарплатой имеется в виду зарплата с учетом инфляции, полученная по специальной формуле")

cols = st.columns(3)

for i in range(3):
    with cols[i]:
        st.subheader(f"{selected_types[i]} (в руб.)")
        chart_data = pd.DataFrame({
            "Year": range(2001, 2024),
            "Номинальная зарплата": data.loc[data["type"] == selected_types[i]].values[:, 2:].flatten(),
            "Реальная зарплата": selected_with_inflation[i]
        })
        st.line_chart(chart_data.set_index("Year"))

        chart_data = pd.DataFrame({
            "Year": range(2002, 2024),
            "Изменение номинальной зарплаты": np.diff(data.loc[data["type"] == selected_types[0]].values[:, 2:].flatten()),
            "Изменение реальной зарплаты": np.diff(np.array(selected_with_inflation[i]), axis=0).flatten()
        })
        st.line_chart(chart_data.set_index("Year"))

st.subheader("ВВП (в млрд. руб.)")
chart_data = pd.DataFrame({
    "Year": range(2000, 2024),
    "ВВП": vvp.iloc[0].values.flatten(),
})
st.line_chart(chart_data.set_index("Year"))