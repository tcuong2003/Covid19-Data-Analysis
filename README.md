<div align="center">

# BÁO CÁO ĐỒ ÁN CUỐI KÌ - PHÂN TÍCH DỮ LIỆU

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

Phân tích dữ liệu: COVID-19 Data.

</div>

---

## 📋 Giới thiệu

**Phân tích dữ liệu (Data Analysis)** à một lĩnh vực quan trọng trong khoa học dữ liệu, nhằm trích xuất thông tin giá trị từ dữ liệu thô để hỗ trợ ra quyết định. Trong bối cảnh thế giới trải qua đại dịch COVID-19, dữ liệu trở thành yếu tố then chốt giúp các tổ chức y tế, chính phủ và nhà nghiên cứu theo dõi diễn biến dịch, dự đoán xu hướng và đánh giá hiệu quả của các biện pháp phòng chống.

Chủ đề COVID-19 không chỉ mang giá trị học thuật mà còn có ý nghĩa thực tiễn, giúp sinh viên hiểu được tầm quan trọng của dữ liệu trong việc ứng phó với các vấn đề toàn cầu. Qua môn học, sinh viên có cơ hội phát triển tư duy logic, kỹ năng làm việc với dữ liệu, và năng lực đánh giá thông tin một cách khoa học.

**Dự án này được xây dựng cho môn học Phân tích dữ liệu.**

---

## ✨ Câu hỏi nghiên cứu (Research Questions)

Bộ dữ liệu COVID-19 do **Johns Hopkins University (JHU)** cung cấp là một tập dữ liệu chuỗi thời gian (time series) mang tính toàn cầu, ghi nhận liên tục số ca **nhiễm**, **tử vong** và **hồi phục** theo từng ngày. Đây là nguồn dữ liệu quan trọng giúp mô tả diễn biến của đại dịch và hỗ trợ quá trình phân tích định lượng.

Dựa trên bộ dữ liệu này, dự án tập trung trả lời các câu hỏi nghiên cứu chính sau:

### 🔍 1. Diễn biến dịch bệnh theo thời gian
- Số ca nhiễm/tử vong/hồi phục thay đổi như thế nào từ giai đoạn đầu dịch đến cuối năm?
- Những mốc thời gian nào ghi nhận sự bùng phát hoặc suy giảm mạnh?

### 🌍 2. So sánh mức độ ảnh hưởng giữa các khu vực/quốc gia
- Quốc gia nào chịu ảnh hưởng nặng nề nhất trong từng giai đoạn?
- Tốc độ lây lan khác nhau như thế nào giữa các khu vực địa lý?

### 📈 3. Xác định xu hướng và mô hình lan truyền
- Liệu có thể nhận diện các giai đoạn: bùng phát – đạt đỉnh – suy giảm?
- Các đường cong tăng trưởng có điểm tương đồng hoặc khác biệt nổi bật nào?

### ⚖️ 4. Đánh giá tỉ lệ tử vong và khả năng hồi phục
- Tỉ lệ tử vong (CFR) của từng quốc gia là bao nhiêu?
- Quốc gia nào có mức độ phục hồi tốt hơn và vì sao?


---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mục đích |
|-----------|---------|
| **jupyter Notebook** | Ngôn ngữ lập trình chính |

---

## 🚀 Cách chạy ứng dụng
Ứng dụng trực quan hóa dữ liệu được xây dựng bằng **Streamlit**. Để khởi chạy, làm theo các bước sau:

### 1️⃣ Mở terminal hoặc command prompt
Dẫn đường dẫn đến thư mục chứa ứng dụng Streamlit:
```
cd streamlit_app
```

### 2️⃣ Cài đặt thư viện cần thiết
Chạy lệnh:
```
pip install -r requirements.txt
```
*Hoặc thủ công:* 
```
pip install streamlit pandas plotly
```

### 3️⃣ Khởi chạy ứng dụng
Dùng câu lệnh:
```
streamlit run covid_dashboard.py
```

### 4️⃣ Mở trong trình duyệt
Streamlit sẽ tự mở trình duyệt hoặc bạn có thể truy cập:
```
http://localhost:8501
```

---
## 🗂️ Cấu trúc dự án

```text
Covid19-Data-Analysis/
├── data/                   # nơi lưu trữ dữ liệu thô và/hoặc đã xử lý  
│   ├── raw/                # dữ liệu gốc, chưa xử lý  
│   ├── processed/          # dữ liệu đã clean / transform / thống kê …  
│   ├── model/              # (tùy chọn) dữ liệu từ nguồn bên ngoài (có thể archive)  
│   └── README.md           # mô tả các file dữ liệu: nguồn, ý nghĩa, format, date cập nhật  
│
├── notebooks/              # notebooks dùng để phân tích, thử nghiệm, khám phá dữ liệu  
│   ├── 01_data_understanding.ipynb  
│   ├── 02_preprocessing.ipynb  
│   ├── 03_EDA.ipynb 
│   ├── 03a_featuring.ipynb 
│   ├── 04_clustering.ipynb 
│   └── 05_visualization.ipynb             
│
├── output/                 # kết quả sinh ra: hình ảnh, báo cáo, bản đồ, CSV Excel xuất ra …  
│   ├── chart/              # biểu đồ, hình ảnh   
│   └── model_results/      # nếu xuất dữ liệu (csv, json …) sau xử lý  
│
├── src/                    # mã nguồn chính — logic xử lý, phân tích, model, helper …  
│   ├── clustering.py      
│   ├── features.py          
│   ├── visualization.py    # mã hỗ trợ vẽ biểu đồ, bản đồ ...  
│   └── preprocessing.py            
│
├── streamlit_app/          # thư mục chứa chương trình chạy streamlit
│
│
├── .gitignore              # ignore file/folder không cần track (data lớn, output tạm …) 
├── README.md
├── requirements.txt        # thư viện / dependencies của dự án

```
---

## 📤 Output Format



---

## 📚 Tài liệu tham khảo

- [COVID-19 Data](https://github.com/CSSEGISandData/COVID-19) 

---

## ⚠️ Ghi chú

- Đồ án chỉ là sản phẩm tập thể không có giá trị thương mại
- Tổng hợp dữ liệu trên tập dữ liệu thô có sẵn, sẽ có thiếu sót so với một số tập dữ liệu khác
- Có thể cải thiện chất lượng và phát triển hơn trong tương lai

---

## 👥 Thông tin

Dự án này được hoàn thành cho bài Phân tích dữ liệu .

---

<div align="center">

Made with ❤️ for Vietnamese 

</div>

