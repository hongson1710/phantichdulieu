# Bảng mô tả dữ liệu

## 1. Nguồn và phạm vi dữ liệu

- **Nguồn:** `data/E-commerce_Customer_Behavior.csv`
- **Kích thước sau kiểm tra/làm sạch:** 350 dòng, 11 cột.
- **Định danh:** `Customer ID` không bị trùng; được dùng để kiểm tra định danh, không dùng như biến hành vi.
- **Giá trị thiếu:** 2 dòng thiếu `Satisfaction Level`. Hai dòng này được giữ lại trong bộ dữ liệu; chỉ loại riêng khi tính tỷ lệ hài lòng.
- **Đơn vị chi tiêu:** chưa xác định; CSV gốc không xác nhận USD/VND.

## 2. Bảng mô tả các cột

| STT | Tên cột | Kiểu dữ liệu | Phạm vi | Giải thích |
|---:|---|---|---|---|
| 1 | `Customer ID` | Số nguyên (`int64`) | 101–450; mỗi ID là duy nhất | Mã định danh khách hàng. Dùng để kiểm tra bản ghi trùng và liên kết bản ghi; không dùng để tính tương quan hoặc đo hành vi. |
| 2 | `Gender` | Chuỗi (`string`) | `Female`, `Male` | Giới tính được ghi trong dữ liệu của khách hàng. Có thể dùng để mô tả cơ cấu mẫu; không dùng làm biến dự đoán trong phiên bản phân tích này. |
| 3 | `Age` | Số nguyên (`int64`) | 26–43 tuổi | Độ tuổi của khách hàng tại thời điểm ghi nhận dữ liệu. Dùng để vẽ histogram và mô tả nhóm tuổi phổ biến. |
| 4 | `City` | Chuỗi (`string`) | New York, Los Angeles, Chicago, San Francisco, Miami, Houston | Thành phố của khách hàng. Dùng để mô tả phân bố địa lý nếu cần; chưa dùng làm biến chính trong 8 biểu đồ ưu tiên. |
| 5 | `Membership Type` | Chuỗi (`string`) | `Bronze`, `Silver`, `Gold` | Hạng thành viên của khách hàng. Dùng để chia nhóm và so sánh chi tiêu, cơ cấu hài lòng giữa các hạng. |
| 6 | `Total Spend` | Số thực (`float64`) | 410,80–1.520,10; đơn vị chưa xác định | Tổng chi tiêu của khách hàng. Dùng cho histogram, boxplot, scatter plot, trung vị và tương quan. |
| 7 | `Items Purchased` | Số nguyên (`int64`) | 7–21 sản phẩm | Số sản phẩm đã mua. Đây là số sản phẩm, không phải số lần đặt hàng; dùng để phân tích mối liên hệ với tổng chi tiêu. |
| 8 | `Average Rating` | Số thực (`float64`) | 3,0–4,9 điểm | Điểm đánh giá trung bình của khách hàng. Thang đo quan sát trong CSV; chưa dùng trong 8 biểu đồ ưu tiên. |
| 9 | `Discount Applied` | Boolean (`bool`) | `True` / `False` | Cho biết khách hàng có áp dụng giảm giá hay không. Dùng để chia hai nhóm và so sánh phân phối chi tiêu; không suy ra tác động nhân quả. |
| 10 | `Days Since Last Purchase` | Số nguyên (`int64`) | 9–63 ngày | Số ngày tính từ lần mua gần nhất. Dùng để phân tích mối liên hệ với tổng chi tiêu. Giá trị lớn hơn nghĩa là lần mua gần nhất đã xa hơn. |
| 11 | `Satisfaction Level` | Chuỗi (`string`) | `Satisfied`, `Neutral`, `Unsatisfied`; thiếu 2 dòng | Mức độ hài lòng của khách hàng. Dùng để tính tỷ lệ theo hạng thành viên; hai dòng thiếu không được tự động gán nhãn. |

## 3. Quy tắc làm sạch liên quan đến bảng

1. Đọc CSV bằng đường dẫn tương đối và loại bỏ khoảng trắng thừa ở tên cột và các trường dạng phân loại.
2. Ép các cột số về kiểu số để phát hiện giá trị không hợp lệ; chuẩn hóa `Discount Applied` về Boolean.
3. Kiểm tra ID trùng, miền giá trị và nhãn phân loại. Dữ liệu hiện tại không có ID trùng, không có chi tiêu âm và không có giá trị ngoài miền kiểm tra.
4. Giữ nguyên 2 giá trị thiếu ở `Satisfaction Level` vì không có cơ sở để suy đoán nhãn đúng.

**Lưu ý:** bảng này mô tả dữ liệu quan sát, không khẳng định quan hệ nhân quả giữa hạng thành viên, giảm giá, mức hài lòng và chi tiêu.
