"""
COVID-19 Dashboard - Phân tích dữ liệu toàn cầu
Dùng Streamlit + Plotly để trực quan hóa dữ liệu COVID-19

Run: streamlit run covid_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CẤU HÌNH TRANG
# ============================================================================
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("📊 COVID-19 Global Dashboard")
st.markdown("Phân tích toàn cầu về dịch bệnh COVID-19")

# ============================================================================
# TẢI & XỬ LÝ DỮ LIỆU
# ============================================================================
@st.cache_data
def load_covid_data():
    """Tải file CSV dữ liệu COVID-19"""
    df = pd.read_csv("time_series_covid19_confirmed_global.csv")
    return df

try:
    covid_df = load_covid_data()
except FileNotFoundError:
    st.error("❌ Không tìm thấy file 'time_series_covid19_confirmed_global.csv'")
    st.stop()

# ============================================================================
# CHỦ ĐỘNG XỬ LÝ DỮ LIỆU
# ============================================================================
# Lấy các cột ngày (bỏ 4 cột đầu: Province/State, Country/Region, Lat, Long)
date_columns = covid_df.columns[4:]

# Chuyển đổi ngày từ chuỗi thành datetime
dates = pd.to_datetime(date_columns)

# Gộp tất cả các tỉnh/bang theo quốc gia
country_totals = covid_df.groupby("Country/Region")[date_columns].sum()

# Tổng toàn cầu
global_totals = country_totals.sum()

# ============================================================================
# TÌM CÁC CHỈ SỐ CHÍNH
# ============================================================================
# Tổng ca mắc toàn cầu (ngày cuối cùng)
total_global_cases = int(global_totals.iloc[-1])

# Ngày có nhiều ca mắc nhất (tính theo số ca mới trong ngày)
daily_new_cases = global_totals.diff().fillna(0)
peak_day_idx = daily_new_cases.idxmax()
peak_day = pd.to_datetime(peak_day_idx)
peak_cases = int(daily_new_cases.max())

# Quốc gia có nhiều ca mắc nhất
top_country = country_totals.iloc[:, -1].idxmax()
top_country_cases = int(country_totals.loc[top_country, date_columns[-1]])

# ============================================================================
# PHẦN TỔNG QUAN (OVERVIEW)
# ============================================================================
st.header("📈 Tổng Quan Dịch Bệnh")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌍 Tổng ca mắc toàn cầu",
        value=f"{total_global_cases:,}",
        delta=None
    )

with col2:
    st.metric(
        label="📅 Ngày có ca mắc nhiều nhất",
        value=peak_day.strftime("%d/%m/%Y"),
        delta=f"+{peak_cases:,} ca"
    )

with col3:
    st.metric(
        label="🏆 Quốc gia có ca mắc nhiều nhất",
        value=top_country,
        delta=None
    )

with col4:
    st.metric(
        label="🔴 Ca mắc của quốc gia hàng đầu",
        value=f"{top_country_cases:,}",
        delta=f"{(top_country_cases/total_global_cases)*100:.1f}% toàn cầu"
    )

st.markdown("---")

# ============================================================================
# PHẦN BIỂU ĐỒ (CHARTS)
# ============================================================================
st.header("📊 Biểu Đồ Phân Tích")

# ---------- BIỂU ĐỒ 1: CỘT - SO SÁNH QUỐC GIA ----------
st.subheader("1️⃣ Biểu Đồ Cột - So Sánh Ca Mắc: Thế Giới vs 3 Quốc Gia Hàng Đầu")

# Lấy 3 quốc gia có ca mắc nhiều nhất
top_3_countries = country_totals.iloc[:, -1].nlargest(3).index.tolist()

# Chuẩn bị dữ liệu
chart1_data = {
    "Thực thể": ["🌍 Toàn Cầu"] + [f"#{i+1} {country}" for i, country in enumerate(top_3_countries)],
    "Tổng Ca Mắc": [
        total_global_cases,
        *[int(country_totals.loc[country, date_columns[-1]]) for country in top_3_countries]
    ]
}

chart1_df = pd.DataFrame(chart1_data)

fig1 = px.bar(
    chart1_df,
    x="Thực thể",
    y="Tổng Ca Mắc",
    title="Tổng Số Ca Mắc: Thế Giới vs 3 Quốc Gia Hàng Đầu",
    labels={"Tổng Ca Mắc": "Số Ca Mắc", "Thực thể": ""},
    color="Thực thể",
    text="Tổng Ca Mắc"
)
fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# ---------- BIỂU ĐỒ 2: TRÒN - TỈ LỆ CÁC QUỐC GIA ----------
st.subheader("2️⃣ Biểu Đồ Tròn - Tỉ Lệ % Ca Mắc Các Quốc Gia Hàng Đầu")

# Lấy top 10 quốc gia
top_10_countries = country_totals.iloc[:, -1].nlargest(10)
other_cases = total_global_cases - top_10_countries.sum()

# Chuẩn bị dữ liệu
chart2_data = pd.DataFrame({
    "Country": list(top_10_countries.index) + ["Các quốc gia khác"],
    "Cases": list(top_10_countries.values) + [other_cases]
})

fig2 = px.pie(
    chart2_data,
    names="Country",
    values="Cases",
    title="Tỉ Lệ % Ca Mắc Bệnh Các Quốc Gia Hàng Đầu",
)
fig2.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig2, use_container_width=True)

# ---------- BIỂU ĐỒ 3: ĐƯỜNG - TRENDLINE THEO THỜI GIAN ----------
st.subheader("3️⃣ Biểu Đồ Đường - Số Ca Mắc Toàn Cầu Theo Thời Gian")

# Chuẩn bị dữ liệu time series
chart3_data = pd.DataFrame({
    "Ngày": dates,
    "Tổng Ca Mắc": global_totals.values
})

fig3 = px.line(
    chart3_data,
    x="Ngày",
    y="Tổng Ca Mắc",
    title="Tổng Số Ca Mắc COVID-19 Toàn Cầu Theo Thời Gian",
    labels={"Tổng Ca Mắc": "Số Ca Mắc", "Ngày": "Ngày"},
    markers=False
)
fig3.update_traces(line=dict(color="#1f77b4", width=2))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================================================
# PHẦN GHI CHÚ
# ============================================================================
st.markdown("### 📌 Ghi Chú")
st.markdown("""
- 📊 Dữ liệu từ Johns Hopkins University COVID-19 Global Cases
- 🔄 Dữ liệu được cập nhật hàng ngày
- 📍 Bao gồm tất cả các quốc gia và vùng lãnh thổ
- 🏥 Con số là số ca mắc được xác nhận
""")

st.caption("Tạo bằng Streamlit + Plotly | Dashboard COVID-19 Global Analysis")
