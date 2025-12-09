import pandas as pd
from pathlib import Path

# --- 1. THIẾT LẬP ĐƯỜNG DẪN DỰA TRÊN CẤU TRÚC THƯ MỤC ---

# Giả sử file code này nằm trong thư mục '3_model'
MODEL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MODEL_DIR.parent
PROCESSED_DIR = PROJECT_ROOT / '2_processed'
OUTPUT_DIR = MODEL_DIR # Dữ liệu đầu ra sẽ nằm trong thư mục 3_model

# Danh sách file đã clean để xử lý (Giả định chúng có tên theo phiên bản cuối cùng)
CLEANED_FILES = {
    'Confirmed': PROCESSED_DIR / 'time_series_covid19_confirmed_global_cleaned_no_lat_long.csv',
    'Deaths': PROCESSED_DIR / 'time_series_covid19_deaths_global_cleaned_no_lat_long.csv',
    'Recovered': PROCESSED_DIR / 'time_series_covid19_recovered_global_cleaned_no_lat_long.csv'
}

# --- 2. HÀM TRÍCH XUẤT ĐẶC TRƯNG CHUỖI THỜI GIAN (FEATURE ENGINEERING) ---

def feature_engineer_time_series(df, case_type):
    """
    Trích xuất các đặc trưng chuỗi thời gian quan trọng (Daily Cases, Rolling Mean, Time Features).
    """
    value_col = f'{case_type}_Cases'
    print(f"    -> Tính toán các đặc trưng cho cột: {value_col}")
    
    # Đảm bảo dữ liệu được sắp xếp theo khu vực và ngày để tính toán diff/rolling
    df = df.sort_values(by=['Country_Region', 'Province_State', 'Date']).copy()

    # Tính toán số ca hàng ngày (Daily Cases: C_t - C_{t-1})
    # Phải sử dụng groupby để tính toán diff riêng biệt cho mỗi khu vực
    df[f'Daily_{case_type}'] = df.groupby(['Country_Region', 'Province_State'])[value_col].diff().fillna(0)
    # Đảm bảo số ca hàng ngày không âm (do sai sót dữ liệu)
    df[f'Daily_{case_type}'] = df[f'Daily_{case_type}'].clip(lower=0).astype(int)

    # Tính toán Trung bình trượt 7 ngày (7-Day Rolling Mean)
    # Giúp làm mượt dữ liệu và thấy rõ xu hướng
    df[f'MA_7_Day_{case_type}'] = df.groupby(['Country_Region', 'Province_State'])[f'Daily_{case_type}'].rolling(window=7, min_periods=1).mean().reset_index(level=[0, 1], drop=True)
    
    # Trích xuất các đặc trưng thời gian
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day_of_Week'] = df['Date'].dt.dayofweek # 0=Thứ Hai, 6=Chủ Nhật

    return df

# --- 3. HÀM TẠO MA TRẬN ĐẶC TRƯNG CHO PHÂN CỤM (CLUSTERING) ---

def create_clustering_features(df, case_type):
    """
    Tổng hợp dữ liệu chuỗi thời gian thành các đặc trưng cho mỗi khu vực địa lý 
    (Country_Region và Province_State).
    """
    daily_col = f'Daily_{case_type}'
    value_col = f'{case_type}_Cases'
    print(f"    -> Tổng hợp các đặc trưng cho phân cụm...")

    # Tạo Feature Matrix bằng cách tính toán các chỉ số thống kê trên Daily Cases
    feature_matrix = df.groupby(['Country_Region', 'Province_State']).agg(
        # Đặc trưng về Kích thước
        Total_Cases=(value_col, 'max'), # Tổng số ca tích lũy tối đa
        
        # Đặc trưng về Tốc độ (Trend)
        Mean_Daily_Cases=(daily_col, 'mean'), 
        Max_Daily_Cases=(daily_col, 'max'), # Ngày có số ca tăng cao nhất
        
        # Đặc trưng về Độ biến động (Volatility)
        Std_Daily_Cases=(daily_col, 'std'), # Độ lệch chuẩn
        
        # Đặc trưng về Thời gian
        Days_Reported=('Date', 'count') # Tổng số ngày báo cáo
    ).reset_index()
    
    # Xử lý các giá trị NaN có thể xuất hiện do std hoặc mean nếu dữ liệu không đủ
    feature_matrix['Std_Daily_Cases'].fillna(0, inplace=True) 

    return feature_matrix

# --- 4. THỰC THI CHÍNH ---

if __name__ == "__main__":
    
    all_feature_dfs = {}
    all_clustering_dfs = {}
    
    # Lặp qua từng loại Case (Confirmed, Deaths, Recovered)
    for case_type, file_path in CLEANED_FILES.items():
        print(f"\n======== XỬ LÝ {case_type.upper()} DATA ========")
        
        if not file_path.exists():
            print(f"❌ BỎ QUA: Không tìm thấy file đã clean tại: {file_path}")
            continue

        # Đọc dữ liệu đã clean
        df_clean = pd.read_csv(file_path, parse_dates=['Date'])

        # Bước 1: Trích xuất Đặc trưng Chuỗi thời gian
        df_features = feature_engineer_time_series(df_clean, case_type)
        all_feature_dfs[case_type] = df_features
        
        # Bước 2: Tạo Ma trận Đặc trưng cho Phân cụm
        df_clustering_features = create_clustering_features(df_features, case_type)
        all_clustering_dfs[case_type] = df_clustering_features
        
        # Bước 3: Lưu các file kết quả vào thư mục 3_model
        
        # Lưu file chuỗi thời gian có đặc trưng
        output_feature_path = OUTPUT_DIR / f'TS_{case_type}_Feature_Engineered.csv'
        df_features.to_csv(output_feature_path, index=False)
        print(f"✅ Lưu file Feature Engineered (TS) thành công tại: {output_feature_path}")

        # Lưu file ma trận phân cụm
        output_cluster_path = OUTPUT_DIR / f'CL_{case_type}_Feature_Matrix.csv'
        df_clustering_features.to_csv(output_cluster_path, index=False)
        print(f"✅ Lưu file Clustering Feature Matrix thành công tại: {output_cluster_path}")

    print("\n======== HOÀN THÀNH ======== ")
    print("Dữ liệu đã sẵn sàng trong thư mục 3_model để tiến hành chuẩn hóa và phân cụm.")