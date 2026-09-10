# odoo_training — module khung Odoo 19.0

Dùng chung cho COM-04, Short Course và học phần HTTTQL.

- Phụ thuộc duy nhất: base.
- Model: training.category và training.item.
- Quan hệ: một danh mục có nhiều hồ sơ; hồ sơ bắt buộc có danh mục.
- Giao diện: List, Form, Search; lọc hồ sơ lưu trữ và nhóm theo danh mục.
- Quyền CRUD thuộc nhóm "Odoo Training / Người thực hành".
- Thành viên nhóm dùng chung toàn bộ hồ sơ: CHƯA có record rule riêng tư,
- Chưa chia công ty. Không dùng trực tiếp cho dữ liệu nhạy cảm/sản xuất.
- Không cấp nhóm cho người dùng tự động; quản trị viên cấp sau cài đặt.
- Demo: hai danh mục, hai hồ sơ, chỉ nạp khi bật demo lúc cài.
- Kiểm thử Odoo: CRUD, quan hệ, archive, quyền truy cập âm.

Đây là điểm khởi đầu, chưa phải bài cuối khóa đầy đủ. Chưa thêm workflow,
sequence, decorator, chatter hay inheritance; phát triển theo từng bài.
Hướng dẫn cài, chạy và test nằm trong README.md ở gốc workspace.
Không sao chép hoặc thay thế module delivery_management đang có.
