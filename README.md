# Dashboard IE313: hành vi khách hàng thương mại điện tử

Dashboard dùng dữ liệu `data/E-commerce_Customer_Behavior.csv`, gồm 6 KPI và 10 biểu đồ phân tích hành vi khách hàng.

## Notebook phân tích

Mở `phantich.ipynb` trong VS Code hoặc Jupyter và chọn **Restart Kernel → Run All** khi đang ở thư mục dự án. Notebook trình bày từ nạp CSV, kiểm tra và làm sạch dữ liệu, thống kê mô tả đến 10 biểu đồ có giải thích dữ liệu, kỹ thuật và nhận xét. File đã lưu sẵn kết quả và biểu đồ để xem ngay; chạy lại notebook sau khi CSV thay đổi.

## Xem ngay

Mở `dashboard.html` bằng trình duyệt, chọn **01 · Tổng quan** hoặc **02 · Mối liên hệ**. Nút **Tải PNG 16:9** lưu đúng màn hình đang xem. Có thể đưa trực tiếp các file `charts/dashboard_*.png` vào slide, không cần chụp màn hình.

## Dashboard tương tác

Chạy giao diện Streamlit:

```bash
python3 -m streamlit run dashboard.py
```

Một bộ lọc chung luôn hiển thị và áp dụng đồng thời cho 6 KPI cùng 10 biểu đồ. Bộ lọc gồm thành phố, giới tính, hạng thành viên, trạng thái giảm giá, độ tuổi và mức hài lòng; nút **Đặt lại bộ lọc** khôi phục toàn bộ dữ liệu.

## Tạo lại biểu đồ từ CSV

```bash
python3 -m pip install -r requirements.txt
python3 build_dashboard.py
```

Kết quả nằm trong `charts/`: 8 biểu đồ riêng và 2 ảnh dashboard. Script luôn đọc CSV bằng đường dẫn tương đối với thư mục dự án. Nếu CSV được cập nhật, chạy lại script để đồng bộ số liệu và hình.

## Cách tính và giới hạn

- Trung vị chi tiêu và Pearson được tính trên các cột số của 350 dòng CSV.
- Biểu đồ hài lòng loại 2 dòng thiếu `Satisfaction Level` **chỉ trong biểu đồ này**; tỷ lệ của mỗi hạng có mẫu số là số dòng còn mức hài lòng trong hạng đó.
- `Items Purchased` là **số sản phẩm**, không phải số lần đặt hàng.
- CSV gốc không xác nhận loại tiền tệ của `Total Spend`; dashboard và notebook hiển thị “đơn vị chưa xác định”.
- Các so sánh và tương quan không chứng minh tác động nhân quả của hạng thành viên, giảm giá hoặc thời gian từ lần mua gần nhất.
