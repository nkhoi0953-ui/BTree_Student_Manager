class Student:
    def __init__(self, ma_sv, ho_ten, gioi_tinh, ngay_sinh):
        self.ma_sv = ma_sv      # Khóa chính 
        self.ho_ten = ho_ten
        self.gioi_tinh = gioi_tinh

    def to_dict(self):
        return {
            "Mã SV": self.ma_sv,
            "Họ và Tên": self.ho_ten,
            "Giới tính": self.gioi_tinh
        }