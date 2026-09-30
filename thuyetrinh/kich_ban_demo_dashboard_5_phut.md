# Kịch bản demo dashboard — 5 phút

**Mục tiêu:** cho thấy một bộ lọc thay đổi đồng thời 6 KPI và các biểu đồ, sau đó minh họa hai phát hiện chính: nhóm khách cần tái tiếp cận và khác biệt về hài lòng, giảm giá. Dùng cùng file dữ liệu đã làm sạch trong `dashboard.py`.

**Chuẩn bị trước khi bắt đầu:** tại thư mục dự án, chạy `python3 -m streamlit run dashboard.py`; mở sẵn dashboard trên trình duyệt, phóng to cửa sổ và để trạng thái chưa lọc. Không tính thời gian khởi động ứng dụng vào 5 phút demo.

| Thời gian | Thao tác trên màn hình | Lời thoại gợi ý |
|---|---|---|
| **0:00–0:40** | Chuyển từ slide demo sang dashboard. Chỉ vào bộ lọc chung, dòng `N = 350` và 6 KPI. | “Đây là dashboard phân tích hành vi khách hàng. Ban đầu là toàn bộ **350 khách**. Sáu chỉ số ở trên lần lượt cho biết số khách, tổng chi tiêu ghi nhận, chi tiêu trung vị, điểm đánh giá trung bình, tỷ lệ dùng giảm giá và trung vị số ngày chưa mua. Tất cả dùng chung một tập dữ liệu sau bộ lọc.” |
| **0:40–1:20** | Ở tab **01 · Tổng quan**, cuộn đến CH10, chỉ vào cột “Chi tiêu trung vị” và “Ngày chưa mua trung vị”. | “Ở trạng thái toàn bộ dữ liệu, heatmap so sánh hồ sơ của sáu thành phố. Số trong ô là giá trị thực. Màu được chuẩn hóa **riêng từng chỉ tiêu**, nên chúng ta đọc và so sánh theo cột. Ví dụ San Francisco có chi tiêu trung vị cao nhất, **1.470,5**, và số ngày chưa mua trung vị thấp nhất, **11 ngày**.” |
| **1:20–2:05** | Quay lên bộ lọc **Thành phố**, bỏ các lựa chọn khác và chỉ giữ **New York**. Chỉ vào `N = 59` và KPI. | “Bây giờ tôi chọn New York. Toàn bộ dashboard còn **59 khách**. Chi tiêu trung vị của nhóm là **1.160,6**, điểm đánh giá trung bình khoảng **4,54**, và trung vị ngày chưa mua là **25 ngày**. KPI và biểu đồ đều cập nhật theo cùng bộ lọc; CH10 lúc này chỉ thể hiện hồ sơ New York.” |
| **2:05–3:15** | Mở tab **02 · Chi tiêu & hành vi mua**, cuộn đến **CH07**. Chỉ trục ngang, trục dọc, hai đường nét đứt và vùng trên bên phải. | “Trên CH07, mỗi điểm là một khách New York. Trục ngang là số ngày từ lần mua gần nhất, trục dọc là tổng chi tiêu. Hai đường ngưỡng **23 ngày** và **775,2** được lấy từ **toàn bộ dữ liệu sạch** và giữ cố định khi lọc. Trong 59 khách New York, **32 khách** nằm ở vùng chi tiêu cao nhưng mua đã lâu. Đây là nhóm nên ưu tiên tiếp cận lại; biểu đồ chưa dự đoán họ sẽ rời bỏ.” |
| **3:15–3:30** | Quay lên, bấm **Đặt lại bộ lọc**; xác nhận `N = 350`. Mở tab **03 · Hài lòng & giảm giá**. | “Tôi đặt lại bộ lọc để hai biểu đồ tiếp theo có đủ các hạng thành viên và cả hai nhóm giảm giá để so sánh.” |
| **3:30–4:15** | Chỉ **CH08** và lần lượt các cột Bronze, Silver, Gold. | “CH08 là tỷ lệ hài lòng **trong từng hạng**. Trong dữ liệu hợp lệ, Gold có **100%** khách hài lòng, Silver khoảng **6,8%**, Bronze **0%**. Hai khách Bronze thiếu mức hài lòng được loại khỏi riêng phép tính này, không bị xóa khỏi các KPI khác.” |
| **4:15–4:45** | Cuộn đến **CH09**, chỉ ô chi tiêu rồi ô số sản phẩm. | “CH09 đối chiếu tình trạng dùng giảm giá. Chi tiêu trung vị ở nhóm không dùng giảm giá là **800,9**, ở nhóm có dùng là **690,6**; cả hai nhóm đều có trung vị **12 sản phẩm**. Đây là khác biệt quan sát được, không chứng minh giảm giá gây ra chênh lệch.” |
| **4:45–5:00** | Dừng ở CH09 hoặc quay lên đầu dashboard. | “Dashboard giúp chuyển từ bức tranh chung sang một nhóm khách cụ thể và kiểm tra kết quả trên cùng tập lọc. Để đánh giá tác động của khuyến mãi hay dự đoán rời bỏ, cần thêm dữ liệu giao dịch theo thời gian.” |

## Thao tác cần luyện trước

1. Xác định vị trí CH10, CH07, CH08 và CH09 trong ba tab để cuộn đến đúng biểu đồ mà không mất thời gian tìm kiếm.
2. Tập thao tác ở bộ lọc Thành phố để chỉ giữ New York; sau đó dùng **Đặt lại bộ lọc** trước khi xem CH08–CH09. Khi chỉ còn New York, toàn bộ 59 khách đều có giảm giá, nên CH09 không còn nhóm “Không” để so sánh.
3. Nếu trang tải chậm, bỏ qua phần nói về từng KPI sau khi lọc và giữ ba điểm bắt buộc: **350 → 59 khách**, **32 khách ở vùng ưu tiên tái tiếp cận**, và **đặt lại lọc trước CH08–CH09**.

**Cách đọc số:** `1.160,6` đọc là “một nghìn một trăm sáu mươi phẩy sáu”; `775,2` đọc là “bảy trăm bảy mươi lăm phẩy hai”. `Total Spend` chưa được nguồn xác nhận đơn vị tiền tệ, nên không đọc là USD hay VND.
