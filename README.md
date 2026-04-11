# 🚀 B-Tree Student Manager (Index bậc 3)

Dự án quản lý sinh viên sử dụng cấu trúc dữ liệu **B-Tree (cây 2-3)** để tối ưu hóa hiệu suất tìm kiếm. Được xây dựng bằng Python và Streamlit.

## 🌟 Tính năng nổi bật
* **Quản lý dữ liệu:** Thêm và Xóa sinh viên với cơ chế tự cân bằng cây.
* **Chỉ mục (Indexing):** Tìm kiếm Mã SV cực nhanh với độ phức tạp $O(\log n)$.
* **Trực quan hóa:** Vẽ sơ đồ cây động bằng Graphviz mỗi khi dữ liệu thay đổi.
* **Tìm kiếm:** Hỗ trợ tìm theo Mã SV (Index) hoặc Họ tên (Linear Search).

## 🛠️ Công nghệ sử dụng
* **Ngôn ngữ:** Python 3.9+
* **Framework UI:** [Streamlit](https://streamlit.io/)
* **Thư viện đồ họa:** Graphviz
* **Xử lý dữ liệu:** Pandas

## 💻 Hướng dẫn cài đặt & Chạy
Để chạy ứng dụng này trên máy cục bộ, hãy làm theo các bước sau:

1. **Clone dự án:**
   git clone [https://github.com/username/ten-repo-cua-ban.git](https://github.com/username/ten-repo-cua-ban.git)
   cd ten-repo-cua-ban

2. **Cài đặt thư viện:**
    pip install -r requirements.txt

3. **Chạy ứng dụng:**
    streamlit run app.py