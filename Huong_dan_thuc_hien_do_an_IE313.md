# Hướng dẫn thực hiện đồ án IE313

## 1. Quyết định cấu trúc source

Với bộ dữ liệu E-commerce Customer Behavior Dataset và phạm vi **phân tích, trực quan hóa**, sử dụng **một notebook chính `phantich.ipynb`**. Notebook trình bày theo trình tự câu hỏi → phép tính → biểu đồ → nhận xét, giúp chạy thử và demo toàn bộ quá trình. Chỉ tách thêm module `.py` nếu có hàm được dùng lặp lại nhiều nơi hoặc nếu phát triển dashboard riêng.

```text
NhomXX_PhanTichHanhVi/
├── phantich.ipynb
├── data/
│   └── e_commerce_customer_behavior.csv
├── charts/
│   ├── 01_phan_phoi_tuoi.png
│   ├── 02_co_cau_hang_thanh_vien.png
│   └── ...
├── requirements.txt
└── README.md
```

Tên CSV và file biểu đồ thực tế có thể khác. Trong notebook, dùng đường dẫn tương đối từ thư mục dự án; không dùng đường dẫn riêng của máy cá nhân. Thư mục `charts/` chứa hình xuất ra để dùng trong báo cáo và slide.

### Khi nào tách thành nhiều file?

- Nếu chỉ đọc một CSV, làm sạch, thống kê và vẽ khoảng 6–8 biểu đồ: giữ trong notebook, chia thành các mục Markdown rõ ràng.
- Nếu một hàm xử lý/định dạng biểu đồ dùng nhiều lần và notebook khó đọc: chuyển hàm đó sang `src/utils.py` hoặc `src/plots.py`, rồi import vào notebook.
- Nếu làm dashboard Streamlit: thêm `app.py` riêng; giữ notebook làm minh chứng quá trình phân tích. Dashboard là phần tùy chọn, không thay thế báo cáo và notebook.

## 2. Các phần cần có trong `phantich.ipynb`

| Phần | Nội dung thực hiện | Kết quả cần nhìn thấy |
|---|---|---|
| 1. Mục tiêu và nguồn dữ liệu | Ghi tên đề tài, nguồn Kaggle, phạm vi, 4–5 câu hỏi phân tích | Người đọc biết notebook trả lời điều gì. |
| 2. Nạp dữ liệu | Import thư viện; đọc CSV; xem `shape`, `head()`, `info()` | Số dòng, số cột, tên trường và mẫu dữ liệu. |
| 3. Kiểm tra chất lượng | Tính giá trị thiếu, bản ghi/ID trùng, kiểu dữ liệu, giá trị không hợp lệ | Bảng kiểm tra trước xử lý. |
| 4. Làm sạch | Xử lý lỗi được phát hiện, ghi rõ lý do và số bản ghi thay đổi | Dữ liệu dùng cho phân tích và bảng đối chiếu trước/sau. |
| 5. Thống kê mô tả | Tính số lượng/tỷ lệ; mean, median, Q1, Q3, IQR, độ lệch chuẩn | Bảng tóm tắt các biến chính. |
| 6. Phân tích từng biến | Tuổi, hạng thành viên, chi tiêu, số sản phẩm, mức hài lòng | Histogram, biểu đồ cột, boxplot và nhận xét. |
| 7. Phân tích mối liên hệ | So sánh chi tiêu theo hạng/giảm giá; scatter plot, Pearson cho cặp biến số phù hợp | Bảng nhóm, biểu đồ, hệ số và diễn giải. |
| 8. Phân nhóm theo quy tắc | Đặt ngưỡng chi tiêu và số ngày từ lần mua gần nhất; mô tả từng nhóm | Bảng/biểu đồ phân nhóm và quy tắc có thể tái lập. |
| 9. Kết luận | Tổng hợp 3–5 phát hiện nổi bật, hạn chế dữ liệu | Nhận xét dựa trên số liệu, không suy đoán nhân quả. |

Mỗi phần phân tích nên kết thúc bằng 2–3 câu trả lời: **biểu đồ cho thấy gì, con số nào chứng minh, giới hạn diễn giải là gì**. Không viết sẵn nhận xét trước khi chạy dữ liệu.

## 3. Bộ biểu đồ ưu tiên

1. Histogram `Age`: khoảng tuổi phổ biến.
2. Biểu đồ cột `Membership Type`: số lượng và tỷ trọng khách theo hạng.
3. Histogram và boxplot `Total Spend`: mức chi tiêu điển hình, độ lệch và ngoại lệ.
4. Boxplot `Total Spend` theo `Membership Type`: so sánh phân phối chi tiêu giữa các hạng.
5. Scatter plot `Items Purchased` và `Total Spend`: quan sát mối liên hệ và tính Pearson khi phù hợp.
6. Scatter plot `Days Since Last Purchase` và `Total Spend`: quan sát quan hệ giữa thời gian chưa mua và chi tiêu.
7. Biểu đồ cột chồng 100% `Satisfaction Level` theo `Membership Type`: so sánh tỷ lệ hài lòng trong từng hạng.
8. Boxplot `Total Spend` theo `Discount Applied`: so sánh hai nhóm, không khẳng định tác động nhân quả.

Có thể thêm heatmap tương quan nếu nó giúp tổng hợp các cặp biến số. Chỉ đưa các biểu đồ có phát hiện rõ vào phần nội dung chính của báo cáo; biểu đồ bổ sung có thể để trong demo hoặc phụ lục.

## 4. Quy tắc phân tích cần tuân thủ

- `Customer ID` dùng để kiểm tra định danh/trùng lặp, không xem là một biến số hành vi.
- `Items Purchased` là số sản phẩm, **không phải** số lần đặt hàng. Vì vậy chưa đủ dữ liệu để tính Frequency trong RFM đầy đủ.
- Không có sự kiện xem hàng, thêm giỏ, ngày của từng đơn; không tính phễu chuyển đổi, bỏ giỏ hoặc doanh thu theo tháng.
- Một mối tương quan hoặc khác biệt giữa nhóm có/không giảm giá không chứng minh nguyên nhân.
- Với `Satisfaction Level` thiếu dữ liệu, nêu số dòng thiếu và cách xử lý; không xóa các dòng đó khỏi mọi phân tích nếu không cần.
- Chưa xây dựng mô hình dự đoán. Linear Regression, Ridge, train/test, MSE và R² trong Bài 06–07 không thuộc thực nghiệm của phiên bản đồ án này.

## 5. Liên kết với báo cáo Template_IE313

| Mục báo cáo | Lấy kết quả từ notebook |
|---|---|
| Giới thiệu | Mục tiêu, nguồn và phương pháp; kết quả nổi bật sau khi hoàn tất phân tích. |
| Mô tả bộ dữ liệu (bắt buộc) | Phần 2–4: kích thước, 11 trường, kiểu dữ liệu, giá trị thiếu và xử lý. |
| Phương pháp phân tích | Tự vẽ quy trình phản ánh đúng các phần trong notebook. |
| Phân tích thăm dò | Phần 5–6: thống kê mô tả, phân phối, ngoại lệ. |
| Kết quả phân tích | Phần 7–8: so sánh nhóm, tương quan, phân nhóm và biểu đồ. |
| Kết luận | Phần 9: chỉ chọn phát hiện có bằng chứng. |

Phần từ Giới thiệu đến Kết luận dài **5–10 trang**, không tính bìa, tài liệu tham khảo và phụ lục. Không đưa code dài vào thân báo cáo. Ghi nguồn Kaggle và mọi code/notebook tham khảo; phụ lục ghi nhiệm vụ cụ thể của từng thành viên.

## 6. File nộp và cách kiểm tra

- `NhomXX_Bao_cao.docx` và `NhomXX_Bao_cao.pdf` theo đúng template.
- `NhomXX_Slide.pptx` hoặc định dạng slide được giảng viên chấp nhận.
- `phantich.ipynb`, file CSV, `requirements.txt` và `README.md` hướng dẫn chạy.
- Video thuyết trình nếu nhóm học theo hệ trực tuyến và giảng viên yêu cầu theo template.

**Kiểm tra trước khi nộp:**

- [ ] Notebook chạy được bằng **Restart Kernel → Run All** từ đầu đến cuối.
- [ ] Đường dẫn đến CSV là đường dẫn tương đối; file dữ liệu được nộp cùng code.
- [ ] Có bảng đối chiếu dữ liệu trước/sau xử lý.
- [ ] Mỗi biểu đồ có tên, trục, đơn vị nếu biết và nhận xét có số liệu.
- [ ] Số liệu trong báo cáo, slide và notebook thống nhất.
- [ ] `README.md` ghi cách cài thư viện, đặt dữ liệu và chạy notebook.
- [ ] Mở thử báo cáo, slide và notebook trên máy dùng để demo.

## 7. Thứ tự triển khai đề xuất

1. Tải CSV, giữ bản gốc trong `data/` và ghi nguồn/ngày tải.
2. Tạo `phantich.ipynb`, hoàn thành phần nạp và kiểm tra dữ liệu.
3. Làm sạch có giải thích, sau đó tính thống kê mô tả.
4. Vẽ lần lượt các biểu đồ, bổ sung nhận xét ngay dưới mỗi biểu đồ.
5. Chọn kết quả nổi bật và viết báo cáo theo Template_IE313.
6. Xuất hình, làm slide, viết `README.md` và chạy thử demo.
