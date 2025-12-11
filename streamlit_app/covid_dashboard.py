"""
COVID-19 Dashboard - Phân tích dữ liệu toàn cầu
Dùng Streamlit + Plotly để trực quan hóa dữ liệu COVID-19

Run: streamlit run covid_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

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
def load_covid_data(data_type):
    """Tải file CSV dữ liệu COVID-19 theo loại"""
    file_map = {
        "Confirmed": "time_series_covid19_confirmed_global.csv",
        "Deaths": "time_series_covid19_deaths_global.csv",
        "Recovered": "time_series_covid19_recovered_global.csv"
    }
    df = pd.read_csv(file_map[data_type])
    return df

data_type = st.sidebar.radio(
    "📊 Chọn loại dữ liệu:",
    options=["Confirmed", "Deaths", "Recovered"],
    index=0,
    help="Chọn loại dữ liệu để hiển thị"
)

# Mapping cho tiêu đề và icon
data_labels = {
    "Confirmed": {"title": "Ca Mắc", "icon": "🔴", "unit": "ca mắc"},
    "Deaths": {"title": "Ca Tử Vong", "icon": "⚫", "unit": "ca tử vong"},
    "Recovered": {"title": "Ca Hồi Phục", "icon": "🟢", "unit": "ca hồi phục"}
}

current_label = data_labels[data_type]

try:
    covid_df = load_covid_data(data_type)
except FileNotFoundError:
    st.error(f"❌ Không tìm thấy file dữ liệu cho '{data_type}'")
    st.stop()

# ============================================================================
# CHỦ ĐỘNG XỬ LÝ DỮ LIỆU
# ============================================================================
# Lấy các cột ngày (bỏ 4 cột đầu: Province/State, Country/Region, Lat, Long)
date_columns = covid_df.columns[4:]

# Chuyển đổi ngày từ chuỗi thành datetime
dates = pd.to_datetime(date_columns)

# Điền NaN values với 0
covid_df_filled = covid_df.fillna(0)

# Gộp tất cả các tỉnh/bang theo quốc gia
country_totals = covid_df_filled.groupby("Country/Region")[date_columns].sum()

# Tổng toàn cầu
global_totals = country_totals.sum()

# ============================================================================
# TÌM CÁC CHỈ SỐ CHÍNH
# ============================================================================
# Tổng toàn cầu (ngày cuối cùng với dữ liệu)
# Với Recovered data, dữ liệu dừng vào 8/4/21, nên tìm giá trị cuối cùng khác 0
last_valid_idx = -1
for i in range(len(global_totals) - 1, -1, -1):
    if global_totals.iloc[i] > 0:
        last_valid_idx = i
        break

if last_valid_idx >= 0:
    total_global_cases = int(global_totals.iloc[last_valid_idx])
else:
    total_global_cases = int(global_totals.iloc[-1])

# Ngày có nhiều ca nhất (tính theo số ca mới trong ngày)
daily_new_cases = global_totals.diff().fillna(0)
peak_day_idx = daily_new_cases.idxmax()
peak_day = pd.to_datetime(peak_day_idx)
peak_cases = int(daily_new_cases.max())

# Quốc gia có nhiều ca nhất
# Sử dụng cột cuối cùng với giá trị khác 0
if last_valid_idx >= 0:
    top_country = country_totals.iloc[:, last_valid_idx].idxmax()
    top_country_cases = int(country_totals.iloc[:, last_valid_idx].max())
else:
    top_country = country_totals.iloc[:, -1].idxmax()
    top_country_cases = int(country_totals.iloc[:, -1].max())

# ============================================================================
# PHẦN TỔNG QUAN (OVERVIEW)
# ============================================================================
st.header(f"📈 Tổng Quan {current_label['title']}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=f"🌍 Tổng {current_label['unit']} toàn cầu",
        value=f"{total_global_cases:,}",
        delta=None
    )

with col2:
    st.metric(
        label=f"📅 Ngày có {current_label['unit']} nhiều nhất",
        value=peak_day.strftime("%d/%m/%Y"),
        delta=f"+{peak_cases:,} {current_label['unit']}"
    )

with col3:
    st.metric(
        label=f"🏆 Quốc gia có {current_label['unit']} nhiều nhất",
        value=top_country,
        delta=None
    )

with col4:
    percentage = (top_country_cases / total_global_cases * 100) if total_global_cases > 0 else 0
    st.metric(
        label=f"{current_label['icon']} {current_label['unit']} của quốc gia hàng đầu",
        value=f"{top_country_cases:,}",
        delta=f"{percentage:.1f}% toàn cầu"
    )

st.markdown("---")

# ============================================================================
# PHẦN BIỂU ĐỒ (CHARTS)
# ============================================================================
st.header("📊 Biểu Đồ Phân Tích")

# ---------- BIỂU ĐỒ 1: CỘT - SO SÁNH QUỐC GIA ----------
st.subheader(f"1️⃣ Biểu Đồ Cột - So Sánh {current_label['unit']}: Thế Giới vs 3 Quốc Gia Hàng Đầu")

# Lấy 3 quốc gia có ca nhất (sử dụng cột cuối cùng với dữ liệu hợp lệ)
if last_valid_idx >= 0:
    top_3_countries = country_totals.iloc[:, last_valid_idx].nlargest(3).index.tolist()
    chart1_values = [int(country_totals.loc[country, date_columns[last_valid_idx]]) for country in top_3_countries]
else:
    top_3_countries = country_totals.iloc[:, -1].nlargest(3).index.tolist()
    chart1_values = [int(country_totals.loc[country, date_columns[-1]]) for country in top_3_countries]

# Chuẩn bị dữ liệu
chart1_data = {
    "Thực thể": ["🌍 Toàn Cầu"] + [f"#{i+1} {country}" for i, country in enumerate(top_3_countries)],
    f"Tổng {current_label['unit']}": [total_global_cases] + chart1_values
}

chart1_df = pd.DataFrame(chart1_data)

fig1 = px.bar(
    chart1_df,
    x="Thực thể",
    y=f"Tổng {current_label['unit']}",
    title=f"Tổng Số {current_label['unit']}: Thế Giới vs 3 Quốc Gia Hàng Đầu",
    labels={f"Tổng {current_label['unit']}": current_label['unit'].capitalize(), "Thực thể": ""},
    color="Thực thể",
    text=f"Tổng {current_label['unit']}"
)
fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# ---------- BIỂU ĐỒ 2: TRÒN - TỈ LỆ CÁC QUỐC GIA ----------
st.subheader(f"2️⃣ Biểu Đồ Tròn - Tỉ Lệ % {current_label['unit']} Các Quốc Gia Hàng Đầu")

# Lấy top 10 quốc gia (sử dụng cột cuối cùng với dữ liệu hợp lệ)
if last_valid_idx >= 0:
    top_10_countries = country_totals.iloc[:, last_valid_idx].nlargest(10)
else:
    top_10_countries = country_totals.iloc[:, -1].nlargest(10)

other_cases = max(0, total_global_cases - int(top_10_countries.sum()))

# Chuẩn bị dữ liệu
chart2_data = pd.DataFrame({
    "Country": list(top_10_countries.index) + ["Các quốc gia khác"],
    current_label['unit']: list(top_10_countries.values) + [other_cases]
})

fig2 = px.pie(
    chart2_data,
    names="Country",
    values=current_label['unit'],
    title=f"Tỉ Lệ % {current_label['unit']} Các Quốc Gia Hàng Đầu",
)
fig2.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig2, use_container_width=True)

# ---------- BIỂU ĐỒ 3: ĐƯỜNG - TRENDLINE THEO THỜI GIAN ----------
st.subheader(f"3️⃣ Biểu Đồ Đường - Số {current_label['unit']} Toàn Cầu Theo Thời Gian")

# Chuẩn bị dữ liệu time series
chart3_data = pd.DataFrame({
    "Ngày": dates,
    f"Tổng {current_label['unit']}": global_totals.values
})

fig3 = px.line(
    chart3_data,
    x="Ngày",
    y=f"Tổng {current_label['unit']}",
    title=f"Tổng Số {current_label['unit']} COVID-19 Toàn Cầu Theo Thời Gian",
    labels={f"Tổng {current_label['unit']}": current_label['unit'].capitalize(), "Ngày": "Ngày"},
    markers=False
)
fig3.update_traces(line=dict(color="#1f77b4", width=2))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================================================
# PHẦN GHI CHÚ
# ============================================================================
st.markdown("### 📌 Ghi Chú")
st.markdown(f"""
- 📊 Dữ liệu từ Johns Hopkins University COVID-19 Global Cases
- 🔄 Dữ liệu được cập nhật hàng ngày
- 📍 Bao gồm tất cả các quốc gia và vùng lãnh thổ
- 🏥 Loại dữ liệu hiện tại: **{data_type}** ({current_label['unit'].lower()})
""")


