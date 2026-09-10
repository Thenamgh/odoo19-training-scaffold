# Phát triển tiếp từ module khung

| Phần | File chỉnh sửa | Khi nào cần nâng cấp |
|---|---|---|
| Trường dữ liệu hồ sơ | custom_addons/odoo_training/models/training_item.py | Sau thêm/sửa field |
| Danh mục | custom_addons/odoo_training/models/training_category.py | Sau thêm/sửa field |
| Giao diện | custom_addons/odoo_training/views/*_views.xml | Sau sửa XML |
| Menu | custom_addons/odoo_training/views/training_menus.xml | Sau sửa menu |
| ACL | custom_addons/odoo_training/security/ir.model.access.csv | Sau sửa quyền |
| Demo | custom_addons/odoo_training/demo/training_demo.xml | Kiểm tra trên DB demo mới |
| Test | custom_addons/odoo_training/tests/test_training.py | Chạy test sau sửa |

Trình tự nhập khi thêm model:
1. Tạo file Python và khai báo model.
2. Import file tại models/__init__.py.
3. Thêm ACL tham chiếu model mới.
4. Tạo view, action, menu.
5. Thêm file XML vào manifest theo thứ tự phụ thuộc.
6. Viết test, nâng cấp module trên database thực hành và kiểm tra log.

Phần riêng Short Course: mở rộng bài thực hành theo tiến độ 15 buổi.
Phần riêng HTTTQL: bổ sung phân tích tác nhân, dữ liệu, quy trình và ý nghĩa quản lý.
Cả hai sử dụng cùng module khung, không nhân bản thành hai module trùng technical name.

Nếu đổi tên module cho đề tài cá nhân: đổi tên thư mục và tất cả external ID
có prefix odoo_training; cập nhật test-tags, đường dẫn tài liệu và câu lệnh cài.
Nếu đổi technical name model: cập nhật model_id trong ACL, res_model/action,
model của view, comodel_name, inverse_name và test. Thử trên database mới.
