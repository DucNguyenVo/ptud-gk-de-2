# Ứng dụng Quản lý Công việc (Task Management)

## Thông tin cá nhân
- Họ và tên: Nguyễn Võ Đức
- MSSV: 21061511
- Lớp: DHKHDL18A

## Mô tả Project
Đây là ứng dụng quản lý công việc được xây dựng bằng Flask, cho phép:
- Quản lý tasks với các thông tin: tên công việc, trạng thái, thời gian tạo và hoàn thành
- Hỗ trợ 2 vai trò: admin và user
- Quản lý avatar người dùng với các tính năng:
  - Upload ảnh avatar (hỗ trợ PNG, JPG, JPEG, GIF)
  - Tạo avatar ngẫu nhiên từ DiceBear API
  - Avatar mặc định từ UI Avatars khi chưa có ảnh
- Hiển thị cảnh báo công việc trễ hạn
- Giao diện single column layout

## Cài đặt và Chạy ứng dụng

1. Clone repository:
```bash
git clone https://github.com/[DucNguyenVo]/ptud-gk-de-2.git
cd ptud-gk-de-2
```

2. Tạo môi trường ảo và kích hoạt:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

4. Tạo cấu trúc thư mục cần thiết:
```bash
mkdir -p app/static/img/avatars
```

5. Khởi động ứng dụng:
```bash
flask run
```

6. Truy cập ứng dụng tại: http://localhost:5000

## Cấu trúc thư mục
```
app/
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── avatars/  # Thư mục chứa ảnh avatar upload
├── templates/
│   ├── admin/
│   ├── task/
│   ├── base.html
│   └── profile.html
└── routes.py
```

## Công nghệ sử dụng
- Backend: Flask
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Avatar APIs:
  - DiceBear API: https://api.dicebear.com/6.x
  - UI Avatars: https://ui-avatars.com

## Tài khoản mặc định
- Admin account:
  - Username: admin
  - Password: admin123
  - Quyền: Xem tất cả tasks, quản lý người dùng

## Lưu ý
- Thư mục `app/static/img/avatars` phải có quyền ghi để lưu trữ ảnh avatar
- Kích thước file avatar nên nhỏ hơn 5MB
- Chỉ chấp nhận các định dạng ảnh: PNG, JPG, JPEG, GIF


   
