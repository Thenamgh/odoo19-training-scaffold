# COM-04 — Checklist nghiệm thu

Các ô dưới đây để người kiểm thử tự đánh dấu sau khi thực hiện; chưa xác nhận
cài đặt thành công trên máy Nguyễn Thế Nam.

- [ ] Source Odoo đúng nhánh 19.0; ghi commit: __________.
- [ ] Python/dependencies và PostgreSQL kết nối đúng theo COM-02.
- [ ] Chạy scripts/validate_scaffold.py thành công.
- [ ] Config dùng đúng custom_addons và không trỏ nhầm module trùng tên.
- [ ] Cài odoo_training mới trên database thực hành thành công.
- [ ] Cấp nhóm Odoo Training / Người thực hành cho tài khoản học.
- [ ] Tạo danh mục và hồ sơ; sửa, đọc, xóa hồ sơ thành công.
- [ ] Không lưu được hồ sơ khi thiếu tên hoặc danh mục.
- [ ] Không xóa được danh mục đang có hồ sơ (ondelete=restrict).
- [ ] List/Form/Search hiển thị đúng; lọc/nhóm theo danh mục hoạt động.
- [ ] Archive hồ sơ, tìm qua bộ lọc Đã lưu trữ, khôi phục thành công.
- [ ] Người dùng nội bộ không có nhóm không truy cập được model, kể cả qua ORM.
- [ ] Nếu cài có demo: đúng hai danh mục, hai hồ sơ minh họa.
- [ ] Nâng cấp module bằng -u thành công, không làm mất hồ sơ đã tạo.
- [ ] Chạy bộ test Odoo; log xác nhận test thực sự chạy, không có lỗi.
- [ ] Git không theo dõi config thật, source upstream, logs, filestore, .venv.

Minh chứng: ảnh giao diện, đoạn log đã bỏ bí mật, commit và thông tin phiên bản.
Không đánh dấu COM-04 Hoàn thành chỉ dựa vào việc đã giải nén bộ source.
