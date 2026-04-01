import streamlit as st
import pandas as pd
from btree_logic import BTree
from database import Student


if 'tree' not in st.session_state:
    st.session_state.tree = BTree(m=3)
    st.session_state.database = [] # Bảng gốc

st.title("Quản lý Sinh viên")

# Giao diện nhập liệu
with st.sidebar:
    st.header("Thêm Sinh viên")
    ma_sv = st.text_input("Mã SV")
    ho_ten = st.text_input("Họ tên")
    gioi_tinh = st.selectbox("Giới tính", ["Nam", "Nữ"])
    
    if st.button("Thêm"):
        if ma_sv and ho_ten:
            new_student = Student(ma_sv, ho_ten, gioi_tinh)
            st.session_state.tree.insert(new_student)
            st.session_state.database.append(new_student.to_dict())
            st.success("Đã thêm thành công!")

# Hiển thị bảng gốc
st.header("Bảng dữ liệu gốc")
if st.session_state.database:
    st.table(pd.DataFrame(st.session_state.database))
else:
    st.info("Chưa có dữ liệu.")

st.header("Cấu trúc Chỉ mục (B-Tree Index)")
# Lấy đối tượng Graphviz từ cây
dot = st.session_state.tree.get_graphviz_source()
# Hiển thị lên Streamlit
st.graphviz_chart(dot)



st.divider() # Vạch kẻ ngăn cách
st.header("🔍 Tìm kiếm sinh viên")

search_type = st.radio("Chọn phương thức tìm kiếm:", ["Theo Mã SV (Sử dụng B-Tree Index)", "Theo Họ tên (Quét tuần tự)"])

if search_type == "Theo Mã SV (Sử dụng B-Tree Index)":
    s_id = st.text_input("Nhập Mã SV cần tìm")
    if s_id:
        # Gọi hàm search trong bộ não B-Tree
        result = st.session_state.tree.search(s_id)
        if result:
            st.success(f"✅ Tìm thấy bằng Index: **{result.ho_ten}** - Giới tính: {result.gioi_tinh}")
        else:
            st.error("❌ Không tìm thấy sinh viên này.")

else:
    s_name = st.text_input("Nhập Họ tên cần tìm")
    if s_name:
        # Tìm tuần tự trong list database (bảng gốc)
        results = [s for s in st.session_state.database if s_name.lower() in s["Họ và Tên"].lower()]
        if results:
            st.write(f"Tìm thấy {len(results)} kết quả:")
            st.table(results)
        else:
            st.error("❌ Không tìm thấy tên này.")


st.sidebar.divider()
st.sidebar.header("🗑️ Xóa Sinh viên")
delete_id = st.sidebar.text_input("Nhập Mã SV muốn xóa")

if st.sidebar.button("Xóa"):
    if delete_id:
        # Kiểm tra xem có tồn tại không trước khi xóa
        target = st.session_state.tree.search(delete_id)
        if target:
            # Xóa trong B-Tree
            st.session_state.tree.delete(delete_id)
            
            # Xóa trong danh sách database gốc
            st.session_state.database = [s for s in st.session_state.database if s["Mã SV"] != delete_id]
            
            st.sidebar.warning(f"Đã xóa sinh viên mã {delete_id}")
            st.rerun() # Load lại trang để cập nhật cây và bảng
        else:
            st.sidebar.error("Mã SV không tồn tại!")