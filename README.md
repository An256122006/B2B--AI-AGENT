# Minh An B2B AI Agent

> Ứng dụng tiếp nhận yêu cầu mua hàng B2B, kiểm tra sản phẩm và tồn kho, tính báo giá, phân quyền phê duyệt và theo dõi cơ hội.

## Mục lục

- [Tính năng](#tính-năng)
- [Quy tắc nghiệp vụ](#quy-tắc-nghiệp-vụ)
- [Chạy trên máy cá nhân](#chạy-trên-máy-cá-nhân)
- [Tài khoản demo](#tài-khoản-demo)
- [Kiểm tra các tình huống mẫu](#kiểm-tra-các-tình-huống-mẫu)
- [Triển khai Vercel](#triển-khai-vercel)
- [Cấu trúc dự án](#cấu-trúc-dự-án)

## Tính năng

- Phân tích yêu cầu bằng tiếng Việt, nhận diện khách hàng, sản phẩm, số lượng, ngân sách, thời hạn và chiết khấu.
- Đối chiếu danh mục, giá, tồn kho và thời gian giao hàng.
- Tạo cơ hội, báo giá, nội dung cần làm rõ và phiếu xin duyệt.
- Tìm kiếm cơ hội theo mã, khách hàng, liên hệ hoặc trạng thái.
- Phân quyền theo vai trò; lưu cơ hội, tài khoản, danh mục và nhật ký khi chạy local.
- Giao diện có thông báo trong ứng dụng và cổng gửi yêu cầu dành cho khách hàng.

## Quy tắc nghiệp vụ

| Điều kiện | Kết quả |
|---|---|
| Thiếu thông tin bắt buộc | **Cần bổ sung thông tin** |
| Sản phẩm không phù hợp tồn kho hoặc tiến độ | **Chưa đáp ứng** |
| Chiết khấu trên 5% hoặc giá trị sau chiết khấu từ 500 triệu đồng | **Chờ duyệt** |
| Chiết khấu trên 15% | Cần **Admin** phê duyệt |
| Đủ điều kiện, trong hạn mức | **Có thể tiếp tục** |

> AI hỗ trợ thẩm định và soạn đề xuất. Các trường hợp vượt thẩm quyền cần người có quyền phê duyệt.

## Chạy trên máy cá nhân

Yêu cầu: Python 3.8 trở lên.

1. Mở terminal tại thư mục dự án.
2. Khởi động máy chủ:

   ```powershell
   python server.py
   ```

   Nếu máy dùng Python Launcher:

   ```powershell
   py server.py
   ```

3. Mở [http://localhost:8888](http://localhost:8888).

Trên macOS/Linux có thể chạy `./start_localhost.sh`.

Ứng dụng lưu dữ liệu local tại `database/minhan_app.sqlite3`. Tệp này bị loại khỏi Git; hãy sao lưu riêng nếu cần giữ dữ liệu.

## Tài khoản demo

| Vai trò | Email | Mật khẩu | Quyền chính |
|---|---|---|---|
| Admin | `admin@minhan.com.vn` | `admin123` | Quản trị, audit, danh mục và phê duyệt cấp cao |
| Sales Manager | `tuan.le@minhan.com.vn` | `manager123` | Xem toàn bộ cơ hội, duyệt trong hạn mức, xuất báo cáo |
| Sales Rep | `an.nguyen@minhan.com.vn` | `sales123` | Tạo báo giá và xem cơ hội được giao |
| Khách hàng | `user@digitech.vn` | `user123` | Gửi yêu cầu và xem yêu cầu của chính mình |

Các tài khoản trên chỉ phục vụ demo. Đăng ký công khai chỉ tạo tài khoản khách hàng; không dùng mật khẩu demo trong môi trường thật.

## Kiểm tra các tình huống mẫu

Dữ liệu mẫu nằm trong `modules/b2b_agent.py`. Bốn tình huống bao gồm báo giá đủ điều kiện, thiếu thông tin, cần phê duyệt và không đáp ứng tồn kho/tiến độ.

Để kiểm tra luồng phê duyệt:

1. Đăng nhập Sales Rep và gửi yêu cầu của Viễn Thông Toàn Cầu: 30 Router Cisco C8200L, chiết khấu 10%, ngân sách 700 triệu, giao trong 10 ngày.
2. Xác nhận cơ hội ở trạng thái **Chờ duyệt**. Sales Rep không được mở hộp thư phê duyệt.
3. Đăng nhập Sales Manager, mở **Hộp thư phê duyệt** và duyệt hoặc từ chối yêu cầu.

Mã phiếu demo `APV-2026-003` chỉ đúng khi đây là cơ hội thứ ba trong dữ liệu sạch.

## Triển khai Vercel

Vercel cần cơ sở dữ liệu PostgreSQL dùng chung vì ổ đĩa của môi trường serverless không phù hợp để lưu SQLite lâu dài. Cấu hình các biến môi trường sau trong Vercel:

| Biến | Giá trị |
|---|---|
| `DATABASE_URL` | Chuỗi kết nối PostgreSQL (`postgres://` hoặc `postgresql://`) |
| `SESSION_SECRET` | Chuỗi bí mật dài, ngẫu nhiên |

Có thể xem tên biến trong `.env.example`. Không commit thông tin kết nối hoặc khóa bí mật. Cài dependencies từ `requirements.txt` khi build.

## Cấu trúc dự án

```text
api/                 Điểm vào API cho Vercel
database/            Lớp lưu trạng thái ứng dụng
modules/             Luồng nghiệp vụ, danh mục và chính sách
web/                 Giao diện HTML, CSS, JavaScript
server.py            Máy chủ local và API
vercel.json          Cấu hình rewrite cho Vercel
```
