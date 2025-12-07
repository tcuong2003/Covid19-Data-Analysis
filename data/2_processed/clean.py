import pandas as pd
from pathlib import Path

# Thư mục raw (nơi chứa file gốc)
RAW_DIR = Path(__file__).resolve().parent.parent / '1_raw'
OUTPUT_DIR = Path(__file__).resolve().parent

# Danh sách các file cần làm sạch
file_names = [
    'time_series_covid19_confirmed_global.csv',
    'time_series_covid19_deaths_global.csv',
    'time_series_covid19_recovered_global.csv'
]

# Định nghĩa hàm làm sạch
def clean_covid_data_no_coords_v2(file_name):
    """
    Hàm làm sạch, chuyển đổi dữ liệu COVID-19 từ Wide sang Long, 
    và đảm bảo loại bỏ các cột Lat/Long.
    """
    # Xây dựng đường dẫn tuyệt đối đến file raw
    file_path = RAW_DIR / file_name
    
    if not file_path.exists():
        print(f"❌ Lỗi: Không tìm thấy file tại đường dẫn: {file_path}")
        return None
    
    case_type = file_name.split('_')[-2].replace('.csv', '')

    try:
        # Đọc file
        df = pd.read_csv(file_path) 
        print(f"\n--- Bắt đầu làm sạch file: **{file_name}** ({case_type.upper()}) ---")
    except Exception as e:
        print(f"❌ Lỗi khi đọc file {file_name}: {e}")
        return None

    # 1. Đổi tên cột
    df.rename(columns={
        'Province/State': 'Province_State',
        'Country/Region': 'Country_Region'
    }, inplace=True)

    # 2. Xử lý giá trị thiếu (Điền NaN bằng chuỗi rỗng cho Province_State)
    df['Province_State'].fillna('', inplace=True) 
    
    # 3. LOẠI BỎ TRIỆT ĐỂ CỘT LAT VÀ LONG TRƯỚC KHI MELT
    cols_to_remove = ['Lat', 'Long']
    
    # Tạo DataFrame tạm thời đã được loại bỏ Lat và Long
    # Sử dụng errors='ignore' để tránh lỗi nếu cột đã bị xóa
    df_temp = df.drop(columns=cols_to_remove, errors='ignore')
    print(f"    - ✅ Đã xóa cột 'Lat' (Vĩ độ) và 'Long' (Kinh độ) khỏi DataFrame tạm thời.")

    # 4. Chuyển đổi từ định dạng Wide sang Long (Unpivot/Melt)
    # Chỉ dùng Province_State và Country_Region làm biến định danh
    id_vars = ['Province_State', 'Country_Region'] 
    
    # Xác định các cột ngày còn lại
    date_cols = df_temp.columns.difference(id_vars)
    value_name = f'{case_type.capitalize()}_Cases'

    df_long = df_temp.melt(
        id_vars=id_vars,
        value_vars=date_cols,
        var_name='Date',
        value_name=value_name
    )
    
    # 5. LOẠI BỎ CÁC TRƯỜNG HỢP CÓ DỮ LIỆU RỖNG
    rows_before = len(df_long)
    df_long.dropna(subset=['Country_Region', value_name], inplace=True)
    rows_after = len(df_long)
    print(f"    - Loại bỏ: {rows_before - rows_after} hàng có giá trị rỗng trong Country_Region hoặc cột số ca.")
    
    # 6. Chuyển đổi cột 'Date' sang kiểu datetime
    df_long['Date'] = pd.to_datetime(df_long['Date'], format='%m/%d/%y')

    # 7. Chuyển đổi cột giá trị sang kiểu số nguyên (Integer)
    df_long[value_name] = df_long[value_name].astype(int) 

    # 8. Sắp xếp dữ liệu
    df_cleaned = df_long.sort_values(by=['Country_Region', 'Province_State', 'Date']).reset_index(drop=True)

    # 9. Xuất dữ liệu đã clean
    # Đổi tên file để xác nhận sự thay đổi
    output_file_path = OUTPUT_DIR / f'time_series_covid19_{case_type}_global_cleaned_no_lat_long.csv'
    df_cleaned.to_csv(output_file_path, index=False)
    print(f"✅ Đã hoàn thành. File làm sạch đã lưu vào: **{output_file_path}**")
    
    return df_cleaned

# --- Chạy hàm làm sạch cho từng file ---
cleaned_dataframes = {}
for file_name in file_names:
    cleaned_df = clean_covid_data_no_coords_v2(file_name)
    if cleaned_df is not None:
        case_type = file_name.split('_')[-2]
        cleaned_dataframes[case_type] = cleaned_df