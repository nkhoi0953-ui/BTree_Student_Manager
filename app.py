import streamlit as st
import pandas as pd
from btree_logic import BTree
from database import Student

# Khởi tạo cây trong session_state để không bị mất khi load lại trang
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