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
Understanding Data – COVID-19 Time Series
Mục lục
1.Định nghĩa vấn đề
1.1 Bối cảnh dữ liệu

Bộ dữ liệu COVID-19 mà Johns Hopkins University cung cấp là một hệ thống ghi nhận số ca bệnh theo chuỗi thời gian (time series), được tổng hợp từ các cơ quan y tế quốc gia trên toàn thế giới. Đây là một trong những nguồn dữ liệu được sử dụng rộng rãi nhất trong suốt thời kỳ đại dịch, hỗ trợ báo chí, cơ quan quản lý, các tổ chức nghiên cứu và cộng đồng theo dõi tình hình dịch bệnh theo từng ngày.

Dữ liệu bao gồm 3 nhóm chính:

Confirmed – Tổng số ca nhiễm được xác nhận
Deaths – Tổng số ca tử vong
Recovered – Tổng số ca hồi phục
Mỗi bảng đều được lưu theo dạng "wide format": mỗi dòng là một quốc gia/vùng lãnh thổ, và mỗi cột tương ứng với một ngày ghi nhận kể từ tháng 1/2020.

Dữ liệu giúp mô tả:

Diễn biến dịch bệnh qua thời gian
Sự khác nhau về tốc độ lây lan giữa các khu vực
Các giai đoạn bùng phát, đạt đỉnh và suy giảm
Tác động của chính sách phòng chống dịch
Tỉ lệ tử vong và khả năng phục hồi theo từng quốc gia


---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mục đích |
|-----------|---------|
| **jupyter Notebook** | Ngôn ngữ lập trình chính |

---

## 📦 Cài đặt


---

## 🚀 Cách chạy ứng dụng



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
│   ├── 01_data_cleaning.ipynb  
│   ├── 02_preprocessing.ipynb  
│   ├── 03_clustering.ipynb 
│   └── 04_visualization.ipynb             
│
├── output/                 # kết quả sinh ra: hình ảnh, báo cáo, bản đồ, CSV/Excel xuất ra …  
│   ├── chart/              # biểu đồ, hình ảnh   
│   └── model_results/      # nếu xuất dữ liệu (csv, json …) sau xử lý  
│
├── src/                    # mã nguồn chính — logic xử lý, phân tích, model, helper …  
│   ├── clustering.py      
│   ├── features.py          
│   ├── visualization.py    # mã hỗ trợ vẽ biểu đồ, bản đồ ...  
│   └── preprocessing.py            
│
├── streamlit_app/          # (theo repo hiện tại có thư mục streamlit_app)
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
- 
- 
- 

---

## ⚠️ Ghi chú

- 
- 
- 

---

## 👥 Thông tin

Dự án này được hoàn thành cho bài Phân tích dữ liệu .

---

<div align="center">

Made with ❤️ for Vietnamese 

</div>

