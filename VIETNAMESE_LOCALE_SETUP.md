# Hướng dẫn Cấu hình Ngôn ngữ Tiếng Việt cho CKAN Data Requests Extension

## 1. Cấu hình CKAN để hỗ trợ tiếng Việt

Thêm các dòng sau vào file cấu hình CKAN (thường là `/etc/ckan/default/ckan.ini`):

```ini
# Thêm tiếng Việt vào danh sách ngôn ngữ được hỗ trợ
ckan.locales_offered = en vi es de pt_BR
ckan.locales_filtered_out = en_GB

# Đặt ngôn ngữ mặc định (tuỳ chọn)
ckan.locale_default = vi
```

## 2. Restart CKAN server

Sau khi cập nhật cấu hình, restart CKAN server để áp dụng thay đổi:

```bash
sudo supervisorctl restart ckan-uwsgi:*
# hoặc
sudo systemctl restart apache2
# hoặc restart development server nếu đang chạy trong dev mode
```

## 3. Kiểm tra Translation

### Trong Interface:
- Truy cập vào CKAN site của bạn
- Tìm selector ngôn ngữ (thường ở header hoặc footer)
- Chọn "Tiếng Việt" hoặc "vi"
- Navigate tới Data Requests section để xem translation

### Programmatically:
```python
import ckan.lib.i18n as i18n

# Set locale to Vietnamese
i18n.set_lang('vi')

# Test translation
from ckan.common import _
translated = _('Data Requests')  # Should return "Yêu cầu Dữ liệu"
```

## 4. Các chuỗi được dịch

Extension đã bao gồm translation cho:
- Tất cả UI elements (buttons, labels, messages)
- Form fields và validation messages  
- Navigation elements
- Email notifications
- Status messages (success/error)
- Help text và descriptions

## 5. Cập nhật Translation

Để cập nhật hoặc thêm translation mới:

1. Chỉnh sửa file `.po`:
```bash
vi ckanext/datarequests/i18n/vi/LC_MESSAGES/ckanext-datarequests.po
```

2. Compile lại file `.mo`:
```bash
msgfmt ckanext/datarequests/i18n/vi/LC_MESSAGES/ckanext-datarequests.po \
       -o ckanext/datarequests/i18n/vi/LC_MESSAGES/ckanext-datarequests.mo
```

3. Restart CKAN server

## 6. Troubleshooting

### Translation không hiển thị:
- Kiểm tra file `.mo` có tồn tại và có quyền read
- Verify CKAN config có include 'vi' trong `ckan.locales_offered`
- Clear browser cache và CKAN cache
- Restart CKAN server

### Một số chuỗi vẫn bằng tiếng Anh:
- Có thể là core CKAN strings, cần cài đặt CKAN Vietnamese locale
- Hoặc extension khác chưa có Vietnamese translation

## 7. CKAN Core Vietnamese Locale

Nếu muốn toàn bộ CKAN interface bằng tiếng Việt, cài thêm:

```bash
# Download CKAN Vietnamese locale từ GitHub
wget https://github.com/ckan/ckan/raw/master/ckan/i18n/vi/LC_MESSAGES/ckan.po
msgfmt ckan.po -o /usr/lib/ckan/default/src/ckan/ckan/i18n/vi/LC_MESSAGES/ckan.mo
```

## Kết quả mong đợi

Sau khi cấu hình đúng:
- Interface chuyển sang tiếng Việt khi user chọn locale 'vi'
- Tất cả Data Requests elements hiển thị bằng tiếng Việt
- Email notifications gửi bằng tiếng Việt
- Form validation messages bằng tiếng Việt