import pandas as pd
from pathlib import Path

# Thư mục raw (nơi chứa file gốc). Tính đường dẫn dựa trên vị trí file này
RAW_DIR = Path(__file__).resolve().parent.parent / '1_raw'

# Danh sách các file cần làm sạch (chỉ tên file, sẽ tìm trong `data/1_raw/`)
file_names = [
    'time_series_covid19_confirmed_global.csv',
    'time_series_covid19_deaths_global.csv',
    'time_series_covid19_recovered_global.csv'
]

def clean_covid_data(file_path):
    """
    Hàm làm sạch và chuyển đổi dữ liệu COVID-19 từ Wide sang Long.
    """
    # đảm bảo file_path là Path và tìm trong RAW_DIR nếu cần
    file_path = Path(file_path)
    if not file_path.exists():
        alt = RAW_DIR / file_path.name
        if alt.exists():
            file_path = alt
        else:
            print(f"❌ Lỗi: Không tìm thấy file tại đường dẫn: {file_path}")
            return None
    case_type = file_path.stem.split('_')[-2]  # Lấy loại case (confirmed, deaths, recovered)
    try:
        df = pd.read_csv(file_path)
        print(f"\n--- Bắt đầu làm sạch file: **{file_path}** ({case_type.upper()}) ---")
    except Exception as e:
        print(f"❌ Lỗi khi đọc file {file_path}: {e}")
        return None

    # 1. Đổi tên cột
    df.rename(columns={
        'Province/State': 'Province_State',
        'Country/Region': 'Country_Region'
    }, inplace=True)
    # 2. Xử lý giá trị thiếu (Điền NaN bằng chuỗi rỗng)
    df['Province_State'].fillna('', inplace=True)

    # 3. Chuyển đổi từ định dạng Wide sang Long (Unpivot/Melt)
    id_vars = ['Province_State', 'Country_Region', 'Lat', 'Long']
    date_cols = df.columns.difference(id_vars)
    value_name = f'{case_type.capitalize()}_Cases' # Tạo tên cột giá trị động (Confirmed_Cases, Deaths_Cases, ...)

    df_long = df.melt(
        id_vars=id_vars,
        value_vars=date_cols,
        var_name='Date',
        value_name=value_name
    )
    
    # 4. Chuyển đổi cột 'Date' sang kiểu datetime
    df_long['Date'] = pd.to_datetime(df_long['Date'], format='%m/%d/%y')
    # 5. Chuyển đổi cột giá trị sang kiểu số nguyên (Integer)
    df_long[value_name] = df_long[value_name].astype(int)

    # 6. Sắp xếp dữ liệu
    df_cleaned = df_long.sort_values(by=['Country_Region', 'Province_State', 'Date']).reset_index(drop=True)
    # Loại bỏ các trường hợp có dữ liệu rỗng
    df_cleaned = df_cleaned.dropna(subset=[value_name])
    # 7. Xuất dữ liệu đã clean vào thư mục `data/2_processed`
    output_dir = Path(__file__).resolve().parent
    output_file_path = output_dir / f'time_series_covid19_{case_type}_global_cleaned.csv'
    df_cleaned.to_csv(output_file_path, index=False)
    print(f"✅ Đã hoàn thành. File làm sạch đã lưu vào: **{output_file_path}**")
    
    return df_cleaned

# --- Chạy hàm làm sạch cho từng file ---
cleaned_dataframes = {}
for file_name in file_names:
    cleaned_df = clean_covid_data(file_name)
    if cleaned_df is not None:
        case_type = Path(file_name).stem.split('_')[-2]
        cleaned_dataframes[case_type] = cleaned_df