# COM-04 — Repository và module khung Odoo 19.0

Người thực hiện: Nguyễn Thế Nam. Dùng chung cho Short Course và học phần HTTTQL.
Bộ bàn giao mới, không phải bản sao repository Research_Odoo19 và không thay đổi
delivery_management. Đã đọc manifest và __init__.py của module hiện có để tránh
trùng tên và tránh mang theo các phụ thuộc stock/sale/mail không cần cho bộ khung.

## 1. Cấu trúc theo workspace đã chốt

Giải nén để có đúng D:\EIT_Odoo19Workspace, không tạo thêm một lớp
EIT_Odoo19Workspace bên trong thư mục cùng tên.

| Đường dẫn | Vai trò | Đưa vào Git? |
|---|---|---|
| odoo/ | Source Odoo 19.0 lấy riêng từ upstream | Không |
| custom_addons/odoo_training/ | Module khung của COM-04 | Có |
| config/odoo.conf.example | Mẫu cấu hình, không chứa mật khẩu thật | Có |
| config/odoo.conf | Cấu hình riêng của máy | Không |
| logs/ | Nhật ký chạy | Không |
| .odoo_data/ | Dữ liệu runtime / filestore | Không |
| .venv/ | Môi trường Python tạo trên máy | Không |
| .vscode/ | Cấu hình debug VS Code | Có |
| docs/ | Checklist và hướng dẫn phát triển | Có |
| scripts/ | Kiểm tra tĩnh, không cần Odoo | Có |

ZIP giữ ba thư mục odoo/, logs/, .odoo_data/ ở trạng thái trống.
Không đóng gói source Odoo, database, mật khẩu hoặc môi trường Python.

## 2. Trước khi sử dụng

Nếu workspace đã có dữ liệu: sao lưu trước, so sánh từng file và chỉ đưa các file
mới vào vị trí tương ứng. KHÔNG ghi đè odoo.conf, README, .gitignore, .vscode hay
module cũ một cách tự động. Có thể hợp nhất các dòng .gitignore cần thiết.

Nếu source Odoo đã có thì giữ nguyên, không chạy git clone lần nữa.
Nếu odoo/ đang trống, mở PowerShell và chạy:

```powershell
Set-Location D:\EIT_Odoo19Workspace
git clone --branch 19.0 --single-branch https://github.com/odoo/odoo.git odoo
git -C odoo rev-parse HEAD
```

Ghi commit Odoo vào biên bản nghiệm thu để các máy dùng cùng source.
Nhánh 19.0 là nhánh cập nhật liên tục, không phải bản khóa commit.

## 3. Môi trường và cấu hình cục bộ

Giả định Windows, Python 3.12 đã được cài theo cấu hình COM-02.
Dependencies phải lấy từ requirements.txt của chính source Odoo vừa clone.

```powershell
Set-Location D:\EIT_Odoo19Workspace
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\odoo\requirements.txt
```

Nếu pip báo lỗi thư viện hệ thống/build tools, xử lý theo hướng dẫn cài source
Odoo 19; bộ khung không tự cài PostgreSQL hoặc phần mềm hệ thống.

Tạo cấu hình thật chỉ khi chưa có:

```powershell
if (-not (Test-Path .\config\odoo.conf)) {
    Copy-Item .\config\odoo.conf.example .\config\odoo.conf
}
New-Item -ItemType Directory -Force -Path .\logs, .\.odoo_data | Out-Null
```

Mở config/odoo.conf và sửa:

- admin_passwd: mật khẩu quản trị database của Odoo.
- db_user/db_password: role PostgreSQL có thật; mẫu dùng odoo19, không tự tạo role.
- db_port: mẫu 5433, phải đổi nếu server đang chạy cổng khác.
- addons_path/data_dir/logfile: đúng thư mục thực tế.
- Mẫu lọc đúng database odoo19_training. Nếu dùng database khác, sửa dbfilter
  và tham số -d trong toàn bộ câu lệnh/VS Code đồng thời.
- Role PostgreSQL cần quyền tạo database cho lần tạo database thực hành.
  Không dùng role postgres để chạy Odoo.
- Không gửi mật khẩu thật lên GitHub hoặc vào báo cáo.

## 4. Cài module — chỉ trên database thực hành

Dừng tiến trình Odoo đang sử dụng cùng database trước khi cài/nâng cấp bằng CLI.
Lệnh -i có ghi database. Chỉ dùng tên database thực hành riêng; sao lưu nếu đã có dữ liệu.

Cài mới, không nạp demo:

```powershell
.\.venv\Scripts\python.exe .\odoo\odoo-bin -c .\config\odoo.conf -d odoo19_training -i odoo_training --without-demo --stop-after-init
```

Nếu MUỐN demo ngay từ lần cài đầu, dùng lệnh thay thế bên dưới, không chạy cả
hai lệnh rồi kỳ vọng demo được nạp lại:

```powershell
.\.venv\Scripts\python.exe .\odoo\odoo-bin -c .\config\odoo.conf -d odoo19_training -i odoo_training --with-demo --stop-after-init
```

Chạy web sau khi cài:

```powershell
.\.venv\Scripts\python.exe .\odoo\odoo-bin -c .\config\odoo.conf -d odoo19_training
```

Mở http://127.0.0.1:8069. Quản trị viên bật chế độ nhà phát triển,
vào Settings → Users & Companies → Groups, mở nhóm
"Odoo Training / Người thực hành" và thêm tài khoản nội bộ dùng để học.
Tùy ngôn ngữ/cấu hình, tên menu có thể khác. Đăng nhập lại sau khi cấp quyền.

Trong ứng dụng Odoo Training: tạo Danh mục trước → tạo Hồ sơ thực hành →
tìm kiếm/lọc/nhóm theo danh mục. Không thấy ứng dụng thì kiểm tra nhóm quyền,
database đang mở và logs/odoo19.log.

## 5. VS Code và PyCharm

VS Code: mở chính thư mục EIT_Odoo19Workspace, cài Python/Python Debugger
theo gợi ý extensions; chọn interpreter .venv/Scripts/python.exe.
Nhấn F5, chọn "Odoo 19 - Run (không nâng cấp module)".

PyCharm: đặt interpreter vào .venv/Scripts/python.exe và tạo Python Run Configuration:

| Thuộc tính | Giá trị |
|---|---|
| Script path | D:\EIT_Odoo19Workspace\odoo\odoo-bin |
| Working directory | D:\EIT_Odoo19Workspace |
| Parameters | -c D:\EIT_Odoo19Workspace\config\odoo.conf -d odoo19_training |

Không mở đồng thời VS Code/PyCharm và CLI cùng cổng 8069.

## 6. Cập nhật module và test

Sau khi sửa model/view/security, dừng web và nâng cấp module:

```powershell
.\.venv\Scripts\python.exe .\odoo\odoo-bin -c .\config\odoo.conf -d odoo19_training -u odoo_training --stop-after-init
```

Kiểm tra tĩnh (chỉ dùng thư viện chuẩn Python, không cần cài Odoo):

```powershell
py -3.12 .\scripts\validate_scaffold.py
```

Chạy test Odoo trên database test riêng (không dùng database nghiệp vụ).
Lệnh này có tạo/ghi database odoo19_training_test; dữ liệu test không được
tự động xóa database sau khi chạy. -d chọn database trực tiếp, không phụ thuộc
dbfilter dùng cho truy cập web.

```powershell
.\.venv\Scripts\python.exe .\odoo\odoo-bin -c .\config\odoo.conf -d odoo19_training_test -i odoo_training --without-demo --test-enable --test-tags /odoo_training --stop-after-init
```

Ở các lần chạy sau trên database test đã cài, thay -i bằng -u.
Xem log để xác nhận số test đã chạy và không có failure/error; chỉ nhìn exit code
là chưa đủ. Test mẫu kiểm tra CRUD/quan hệ, archive và người nội bộ thiếu nhóm.
Checklist kiểm tra giao diện và an toàn nằm trong docs/ACCEPTANCE.md.

## 7. Khởi tạo repository Git

ZIP là bộ source để khởi tạo repository, không chứa lịch sử .git.
Nếu thư mục này đã thuộc repository hiện có, không git init lại và không thay remote.

Với workspace mới, chạy:

```powershell
git init -b main
git status --short
git add README.md .gitignore .gitattributes custom_addons config/odoo.conf.example docs scripts .vscode
git diff --cached --stat
git diff --cached
# Chỉ commit sau khi chắc chắn không có mật khẩu hay dữ liệu cá nhân:
git commit -m "COM-04: add Odoo 19 training scaffold"
```

Chưa tạo repository online hoặc push GitHub trong bộ bàn giao này.
Nếu muốn bổ sung vào Research_Odoo19, dùng nhánh mới, hợp nhất cấu hình có kiểm soát,
không thay thế delivery_management và không đưa source upstream odoo/ vào commit.

## 8. Giới hạn và nguồn

Module cố ý nhỏ: hai model, CRUD, quan hệ, giao diện và ACL.
Chưa có quy trình trạng thái, sequence, computed field, decorator, chatter,
record rule riêng tư hay chia công ty. Nhóm thực hành cùng đọc/sửa/xóa toàn bộ
dữ liệu module trong database này; nên dùng database riêng cho mỗi sinh viên.

Nguồn chính thức dùng để đối chiếu:
- https://github.com/odoo/odoo/tree/19.0
- https://github.com/odoo/odoo/blob/19.0/odoo/tests/common.py
- https://github.com/odoo/odoo/blob/19.0/odoo/tools/config.py (Odoo 19 dùng --with-demo để bật demo)
- https://www.odoo.com/documentation/19.0/developer/tutorials/server_framework_101.html
- https://www.odoo.com/documentation/19.0/administration/on_premise/source.html

Đã kiểm tra tĩnh trong môi trường tạo bộ bàn giao. Chưa chạy Odoo/PostgreSQL thực tế.
Xem docs/VALIDATION.md để phân biệt kết quả đã kiểm tra với phần chờ nghiệm thu.
