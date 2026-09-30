# Yêu cầu cập nhật code dashboard phân tích hành vi khách hàng

## 1. Mục tiêu

Cập nhật phần phân tích và trực quan hóa của đồ án IE313 từ bộ dữ liệu khách hàng thương mại điện tử. Dashboard phải cho phép xem tổng quan khách hàng, mức chi tiêu, hành vi mua và mức hài lòng; các chỉ số và biểu đồ sử dụng cùng một tập dữ liệu sau làm sạch và cùng bộ lọc.

**Phạm vi:** thống kê mô tả, so sánh nhóm, trực quan hóa. Không bổ sung mô hình dự đoán, chức năng bán hàng, phễu chuyển đổi hoặc chỉ số doanh thu theo thời gian.

**Hình thức triển khai:** duy trì `phantich.ipynb` làm tài liệu phân tích và demo chính. Nếu dự án hiện có ứng dụng dashboard (ví dụ Streamlit), triển khai giao diện trong file ứng dụng hiện có hoặc `app.py`, tái sử dụng logic tính toán; không nhân đôi các công thức. Nếu chưa có ứng dụng, có thể trình bày các bảng và biểu đồ trong notebook trước.

## 2. Dữ liệu đầu vào và giả định cần xác nhận

| Nhóm | Tên cột trong Kaggle CSV dự kiến | Tên tiếng Việt | Kiểu cần dùng |
|---|---|---|---|
| Định danh | `Customer ID` (nếu có) | Mã khách hàng | Mã/chuỗi, không dùng để tính tương quan |
| Nhân khẩu học | `Gender` | Giới tính | Phân loại |
| Nhân khẩu học | `Age` | Độ tuổi | Số |
| Nhân khẩu học | `City` | Thành phố | Phân loại |
| Thành viên | `Membership Type` | Hạng thành viên | Phân loại |
| Mua sắm | `Total Spend` | Tổng chi tiêu | Số không âm |
| Mua sắm | `Items Purchased` | Tổng sản phẩm đã mua | Số nguyên không âm |
| Đánh giá | `Average Rating` | Điểm đánh giá trung bình | Số, xác nhận thang điểm của dữ liệu |
| Khuyến mãi | `Discount Applied` | Có sử dụng giảm giá | Boolean/nhãn hai giá trị |
| Mua sắm | `Days Since Last Purchase` | Số ngày từ lần mua gần nhất | Số nguyên không âm |
| Hài lòng | `Satisfaction Level` | Mức độ hài lòng | Phân loại |

**Cần xác nhận trước khi lập trình:** “Tổng sản phẩm chi tiêu” trong yêu cầu được hiểu là **số sản phẩm đã mua**, tương ứng `Items Purchased`. Nếu file thực tế mang nghĩa khác, phải cập nhật nhãn và các biểu đồ liên quan. Mỗi dòng được giả định là một khách hàng; nếu dữ liệu có nhiều dòng cho một khách, cần xác định quy tắc gộp trước khi tính KPI.

Đơn vị tiền tệ, thời điểm chốt dữ liệu và định nghĩa `Discount Applied` phải được lấy từ tài liệu của dữ liệu hoặc ghi “chưa xác định”; không tự gán USD/VND, kỳ tháng hoặc ý nghĩa “đã từng dùng” khi chưa có bằng chứng.

## 3. Chuẩn bị và làm sạch dữ liệu

1. Đọc CSV bằng đường dẫn tương đối từ thư mục dự án; giữ file gốc không thay đổi.
2. Kiểm tra cột bắt buộc, kiểu dữ liệu, số dòng, số khách duy nhất (nếu có ID), giá trị thiếu và bản ghi trùng.
3. Chuyển các cột số sang numeric, chuẩn hóa giá trị boolean/categorical; không âm thầm ép dữ liệu không hợp lệ thành 0.
4. Kiểm tra các giá trị bất hợp lý: tuổi, chi tiêu, số sản phẩm, số ngày không âm; điểm đánh giá trong thang điểm xác nhận được.
5. Ghi rõ số dòng trước/sau, số giá trị không hợp lệ và cách xử lý từng cột. Không xóa ngoại lệ chỉ vì nằm ngoài ngưỡng boxplot.
6. Với `Satisfaction Level` bị thiếu, chỉ loại khỏi phép tính tỷ lệ hài lòng; các dòng đó vẫn có thể tham gia các KPI/biểu đồ khác khi những trường cần thiết hợp lệ.

## 4. Bộ lọc chung

- Thành phố (`City`).
- Giới tính (`Gender`).
- Hạng thành viên (`Membership Type`).
- Có sử dụng giảm giá (`Discount Applied`).
- Khoảng tuổi (`Age`).
- Mức độ hài lòng (`Satisfaction Level`), nếu cần.

Mặc định mỗi bộ lọc chọn **Tất cả**. Khi đổi bộ lọc, cập nhật KPI, bảng và biểu đồ trên cùng tập bản ghi; hiển thị `N = số khách đang được phân tích`. Nếu tập lọc rỗng, hiển thị trạng thái không có dữ liệu và không vẽ biểu đồ rỗng/lỗi chia cho 0. Nên có nút đặt lại bộ lọc nếu dashboard tương tác hỗ trợ.

## 5. KPI và công thức

| Mã | Tên hiển thị | Cách tính trên tập đã lọc | Lưu ý |
|---|---|---|---|
| KPI01 | Số khách hàng | `nunique(Customer ID)` nếu ID có và duy nhất sau xử lý; nếu mỗi dòng là một khách và không có ID, đếm số dòng | Không cộng dồn các nhóm nếu ID trùng. |
| KPI02 | Tổng chi tiêu ghi nhận | Tổng `Total Spend` hợp lệ | Không ghi “doanh thu tháng” hoặc “doanh thu đơn hàng”. |
| KPI03 | Chi tiêu trung vị/khách | Median của `Total Spend` | Có thể kèm mean để so sánh khi phân phối lệch. |
| KPI04 | Điểm đánh giá trung bình | Mean của `Average Rating` hợp lệ | Hiển thị số bản ghi dùng để tính nếu thiếu nhiều. |
| KPI05 | Tỷ lệ có sử dụng giảm giá | Số khách `Discount Applied = True` / số khách có giá trị giảm giá hợp lệ × 100% | Công bố mẫu số; không coi là hiệu quả chương trình. |
| KPI06 | Số ngày từ lần mua gần nhất (trung vị) | Median của `Days Since Last Purchase` | Không suy ra ngày mua hoặc tỷ lệ rời bỏ. |

Không tính KPI khi không còn quan sát hợp lệ; hiển thị `—` hoặc “Không đủ dữ liệu” thay vì 0.

## 6. Biểu đồ cần triển khai

### Nhóm A. Tổng quan khách hàng

| Mã | Biểu đồ | Dữ liệu/logic | Cách kiểm tra |
|---|---|---|---|
| CH01 | Histogram độ tuổi | X: các khoảng tuổi nhất quán (ví dụ mỗi 10 tuổi); Y: số khách. | Tổng số đếm bằng số khách có `Age` hợp lệ sau lọc. |
| CH02 | Cột số khách theo thành phố | X: `City`; Y: số khách; sắp xếp giảm dần. | Mỗi cột là số khách của một thành phố, không phải tổng chi tiêu. |
| CH03 | Cột cơ cấu hạng thành viên | X: `Membership Type`; Y: số khách hoặc tỷ trọng, nhãn hiển thị rõ đơn vị. | Nếu là tỷ trọng, tổng các hạng bằng 100% sau khi loại giá trị thiếu. |

### Nhóm B. Chi tiêu và hành vi mua

| Mã | Biểu đồ | Dữ liệu/logic | Cách kiểm tra |
|---|---|---|---|
| CH04 | Histogram tổng chi tiêu | X: `Total Spend`; Y: số khách; có thể vẽ đường mean và median kèm chú giải. | Trục X hiển thị đơn vị đúng với nguồn; không gán một loại tiền chưa xác nhận. |
| CH05 | Boxplot chi tiêu theo hạng | X: `Membership Type`; Y: `Total Spend`; hiển thị số khách mỗi hạng. | Hộp thể hiện trung vị và IQR; ngoại lệ vẫn hiện trên hình. |
| CH06 | Scatter số sản phẩm và chi tiêu | X: `Items Purchased`; Y: `Total Spend`; màu theo hạng nếu không làm biểu đồ rối. | Mỗi điểm là một khách; nếu điểm chồng nhiều, dùng độ trong suốt. |
| CH07 | Scatter số ngày chưa mua và chi tiêu | X: `Days Since Last Purchase`; Y: `Total Spend`; có thể tô màu theo hạng. | Không ghi “xu hướng theo thời gian” vì không có ngày giao dịch. |

### Nhóm C. Hài lòng và giảm giá

| Mã | Biểu đồ | Dữ liệu/logic | Cách kiểm tra |
|---|---|---|---|
| CH08 | Cột chồng 100% hài lòng theo hạng | X: `Membership Type`; phần màu: `Satisfaction Level`; mỗi tỷ lệ dùng **số khách có mức hài lòng hợp lệ trong chính hạng đó** làm mẫu số. | Mỗi cột cộng thành 100%; hiển thị số khách hợp lệ theo hạng. |
| CH09 | Boxplot chi tiêu theo giảm giá | X: `Discount Applied` (Có/Không); Y: `Total Spend`; hiển thị n của từng nhóm. | Tiêu đề là “So sánh chi tiêu theo tình trạng giảm giá”, không khẳng định tác động nhân quả. |

**Ưu tiên phiên bản đầu:** KPI01–KPI06 và CH01, CH03, CH04, CH05, CH07, CH08, CH09. Thêm CH02, CH06 sau khi đã xem bố cục và thấy biểu đồ đem lại nhận xét hữu ích. Heatmap Pearson của các biến số là bổ sung tùy chọn; loại `Customer ID` khỏi tính tương quan.

## 7. Bố cục giao diện gợi ý

1. **Tiêu đề và nguồn dữ liệu:** tên dashboard, phạm vi dữ liệu, ghi chú thời điểm chốt nếu có.
2. **Bộ lọc chung:** ở đầu trang hoặc thanh bên.
3. **Dãy KPI:** 6 chỉ số, có chú thích đơn vị và số mẫu hợp lệ.
4. **Tổng quan khách hàng:** CH01–CH03.
5. **Chi tiêu và hành vi mua:** CH04–CH07.
6. **Hài lòng và giảm giá:** CH08–CH09.
7. **Ghi chú phương pháp:** định nghĩa tổng chi tiêu, cách xử lý thiếu, giới hạn diễn giải.

Nếu màn hình quá dài, chia thành ba tab “Tổng quan”, “Hành vi mua”, “Hài lòng”, nhưng giữ một bộ lọc chung và cùng định nghĩa KPI.

## 8. Phân nhóm khách hàng (tùy chọn)

Nếu cần biểu đồ phân nhóm, dùng `Total Spend` và `Days Since Last Purchase` để tạo bốn ô theo trung vị của **toàn bộ dữ liệu sạch**; giữ ngưỡng cố định khi người xem đổi bộ lọc để các nhóm vẫn so sánh được. Ghi rõ ngưỡng, số khách và tỷ trọng từng nhóm. Không gọi đây là RFM đầy đủ vì `Items Purchased` không phải số lần đặt hàng.

## 9. Tiêu chí nghiệm thu cập nhật code

- [ ] `phantich.ipynb` chạy **Restart Kernel → Run All** không lỗi với file CSV được nộp kèm.
- [ ] Nếu có `app.py`, ứng dụng mở được, bộ lọc hoạt động và có trạng thái tập lọc rỗng.
- [ ] Mọi KPI và biểu đồ đều tính trên cùng tập đã lọc; con số `N` đối chiếu được với số bản ghi.
- [ ] Không đếm trùng khách; quy tắc sử dụng `Customer ID` được ghi rõ.
- [ ] Tỷ lệ hài lòng theo từng hạng cộng thành 100% trên các dòng hợp lệ của hạng đó.
- [ ] Trường thiếu/không hợp lệ được xử lý và công bố, không bị thay bằng 0 tùy tiện.
- [ ] Các chart có tiêu đề, trục, nhãn, đơn vị và số khách của từng nhóm khi so sánh.
- [ ] Báo cáo, slide và dashboard dùng cùng số liệu và định nghĩa chỉ số.
- [ ] Biểu đồ cần cho báo cáo được xuất ra `charts/` với kích thước/chất lượng đủ đọc.
- [ ] `README.md` ghi tên file dữ liệu, cách cài phụ thuộc, lệnh chạy notebook hoặc dashboard.

## 10. Ngoài phạm vi

Không thêm dự đoán chi tiêu/churn, hồi quy Ridge, tỷ lệ chuyển đổi, bỏ giỏ hàng, phễu mua hàng, doanh thu theo tháng, giá trị đơn hàng trung bình hoặc RFM đầy đủ khi file dữ liệu chưa có ngày/chi tiết đơn hàng và hành vi duyệt web cần thiết. Mọi kết luận so sánh nhóm chỉ mô tả sự khác biệt quan sát được trong bộ dữ liệu.
