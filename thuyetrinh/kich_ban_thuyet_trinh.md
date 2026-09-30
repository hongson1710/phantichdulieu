# Kịch bản thuyết trình IE313

Áp dụng cho `phantichhanhvikhachhang.pptx` (13 slide). Phần trình bày: **10 phút** cho slide 1–11. Demo: **5 phút** ở slide 12. Slide 13 dành cho hỏi đáp, không tính vào thời lượng chuẩn bị. Các số liệu dưới đây lấy từ dữ liệu sau làm sạch; `Total Spend` chưa có đơn vị tiền tệ được nguồn xác nhận.

## Slide 1 — Trang bìa (0:20)

> Em chào thầy cô và các bạn. Nhóm [số nhóm] trình bày đề tài phân tích hành vi khách hàng thương mại điện tử. Thành viên nhóm gồm [tên các thành viên]. Trong phần trình bày, nhóm sẽ giới thiệu dữ liệu, phương pháp, những phát hiện chính và demo dashboard tương tác.

**Chuẩn bị:** thay toàn bộ chữ mẫu trên slide bìa, đặc biệt là tên đề tài, khoa và thành viên.

## Slide 2 — Giới thiệu nhóm (0:20)

> Đây là các thành viên thực hiện đề tài: [tên, mã số sinh viên, vai trò nếu muốn nêu]. Nhóm sẽ đi thẳng vào câu hỏi phân tích và kết quả để dành thời gian cho phần demo.

**Chuẩn bị:** điền ảnh, tên và mã số sinh viên; nếu không cần giới thiệu nhóm, có thể nói một câu chuyển ý ngắn rồi sang slide 3.

## Slide 3 — Giới thiệu tổng quan (0:50)

> Đề tài dùng 350 hồ sơ khách hàng để trả lời năm câu hỏi. Thứ nhất, có thể phân nhóm khách theo mức chi tiêu và thời gian từ lần mua gần nhất không? Thứ hai, mức hài lòng khác nhau ra sao giữa các hạng thành viên? Thứ ba, nhóm có và không dùng giảm giá khác nhau thế nào về chi tiêu và số sản phẩm? Hai câu hỏi còn lại là nhóm nào nên ưu tiên giữ chân và hành vi ở các thành phố có khác nhau không. Sau phần dữ liệu và phương pháp, nhóm chỉ trình bày những biểu đồ trực tiếp trả lời các câu hỏi này.

**Chuyển slide:** “Trước tiên, dữ liệu cho phép đo những gì?”

## Slide 4 — Mô tả bộ dữ liệu (0:55)

> Bộ CSV có 350 khách hàng, 11 cột và mỗi dòng đại diện cho một khách. Các biến nhân khẩu học gồm tuổi, giới tính và thành phố. Hành vi mua được thể hiện qua tổng chi tiêu, số sản phẩm, trạng thái dùng giảm giá và số ngày từ lần mua cuối. Ngoài ra còn có hạng thành viên, điểm đánh giá và mức hài lòng. Có hai khách thiếu mức hài lòng; nhóm vẫn giữ họ cho các phân tích không dùng biến này và chỉ loại khỏi mẫu số của biểu đồ hài lòng. Nguồn không ghi rõ đơn vị của tổng chi tiêu, nên nhóm dùng con số gốc và không gán USD hay VND.

**Nhấn mạnh:** không gọi `Total Spend` là doanh thu, giá trị đơn hàng hoặc số tiền USD.

## Slide 5 — Phương pháp phân tích (1:00)

> Quy trình gồm bốn bước. Đầu tiên là nạp CSV, kiểm tra kiểu dữ liệu, giá trị thiếu, trùng lặp và phạm vi hợp lệ. Tiếp theo là áp dụng cùng một bộ lọc cho KPI và biểu đồ để các số có thể đối chiếu. Sau đó nhóm dùng thống kê mô tả: số khách, tỷ lệ theo nhóm, trung bình, trung vị và boxplot. Trung vị là giá trị ở giữa sau khi sắp xếp, nên phù hợp khi muốn so sánh mức chi tiêu điển hình mà ít bị các giá trị rất cao kéo lệch. Cuối cùng, nhóm chia vùng khách hàng bằng hai ngưỡng cố định từ toàn bộ dữ liệu sạch: chi tiêu 775,2 và 23 ngày chưa mua. Đây là phân nhóm mô tả, chưa phải mô hình dự đoán rời bỏ.

**Chuyển slide:** “Từ quy trình đó, chúng ta xem hạng thành viên và chi tiêu trước.”

## Slide 6 — Hạng thành viên và chi tiêu, CH03 + CH05 (1:00)

> Biểu đồ tròn bên trái cho thấy ba hạng thành viên gần như cân bằng: Bronze 116, Silver 117 và Gold 117 khách. Vì quy mô nhóm tương đương, khi nhìn sang biểu đồ bên phải chúng ta có thể tập trung vào phân phối chi tiêu. Trung vị chi tiêu tăng rõ theo hạng: Bronze 475,25; Silver 770,2; Gold 1.210,6. Boxplot còn cho thấy độ trải của từng nhóm, nên không nên chỉ nhìn vào một số trung bình. Phát hiện ở đây là Gold có mức chi tiêu điển hình cao nhất trong bộ dữ liệu, chứ chưa thể nói hạng thành viên đã gây ra mức chi tiêu đó.

**Chỉ vào biểu đồ:** nêu quy mô nhóm ở biểu đồ tròn, rồi chỉ đường trung vị trong từng hộp của CH05.

## Slide 7 — Phân vùng để giữ chân, CH07 (1:10)

> Mỗi chấm là một khách hàng. Trục ngang là số ngày từ lần mua gần nhất; đi sang phải nghĩa là đã lâu hơn. Trục dọc là tổng chi tiêu ghi nhận; đi lên nghĩa là chi tiêu cao hơn. Hai đường chia dùng ngưỡng 23 ngày và 775,2, lấy từ toàn bộ dữ liệu sạch. Vùng cần chú ý là khách chi tiêu cao nhưng lần mua đã lâu: có 32 người. Đây là nhóm hợp lý để ưu tiên tiếp cận lại, vì họ từng có giá trị chi tiêu cao nhưng gần đây ít hoạt động theo chỉ số có sẵn. Chúng ta chưa biết họ đã rời bỏ hay chưa, do dữ liệu không có lịch sử giao dịch theo thời gian.

**Chỉ vào biểu đồ:** đi theo hai trục, hai đường ngưỡng, rồi khoanh vùng “chi tiêu cao, mua đã lâu”.

## Slide 8 — Mức độ hài lòng, CH08 (1:00)

> Biểu đồ cột chồng thể hiện tỷ lệ mức hài lòng bên trong từng hạng, nên mỗi cột cộng lại bằng 100%. Trong số khách có dữ liệu hợp lệ, toàn bộ 117 khách Gold được ghi nhận là hài lòng. Tỷ lệ này ở Silver là khoảng 6,8%, còn Bronze là 0%. Riêng Bronze chỉ có 114 mức hài lòng hợp lệ do hai khách bị thiếu dữ liệu. Chênh lệch giữa các hạng rất rõ trong tập dữ liệu này; bước tiếp theo về mặt nghiệp vụ là tìm hiểu nguyên nhân qua phản hồi chi tiết hoặc khảo sát, vì CSV hiện tại không cho biết vì sao khách không hài lòng.

**Nhấn mạnh:** 100% là tỷ lệ trong hạng Gold của bộ dữ liệu, không phải tỷ lệ của toàn bộ khách hàng.

## Slide 9 — Tình trạng giảm giá, CH09 (1:00)

> Hai boxplot so sánh khách có và không dùng giảm giá. Ở phần chi tiêu, trung vị của nhóm không giảm giá là 800,9; nhóm có giảm giá là 690,6, chênh 110,3. Ở phần số sản phẩm, cả hai nhóm đều có trung vị 12 sản phẩm. Như vậy, trong dữ liệu quan sát được, nhóm dùng giảm giá không có mức chi tiêu điển hình cao hơn; nhưng không thể kết luận giảm giá làm giảm chi tiêu. Chúng ta không có giá trị giảm giá, cách phân bổ khuyến mãi hoặc thông tin trước và sau chương trình.

**Chỉ vào biểu đồ:** so sánh hai đường trung vị ở ô chi tiêu, sau đó sang ô số sản phẩm.

## Slide 10 — Hành vi theo thành phố, CH10 (1:05)

> Heatmap tổng hợp sáu chỉ tiêu theo sáu thành phố. Con số trong từng ô là giá trị thực; màu chỉ thể hiện vị trí tương đối của thành phố trong riêng cột đó, vì các chỉ tiêu có đơn vị khác nhau. San Francisco có trung vị chi tiêu 1.470,5, cao nhất trong sáu thành phố, và trung vị số ngày chưa mua là 11, thấp nhất. Điều đó gợi ý hành vi mua ở đây khác với các thành phố còn lại trong bộ dữ liệu. Mỗi thành phố chỉ có khoảng 58 đến 59 khách, nên nên xem đây là tín hiệu để tìm hiểu sâu hơn trước khi thiết kế chiến dịch theo địa điểm.

**Chỉ vào biểu đồ:** chọn cột chi tiêu và cột ngày chưa mua; tránh so màu trực tiếp giữa hai cột khác đơn vị.

## Slide 11 — Kết quả đạt được (1:20)

> Từ các biểu đồ, nhóm rút ra năm điểm. Một là Gold có mức chi tiêu điển hình cao nhất. Hai là tỷ lệ hài lòng của Gold đạt 100% trong 117 khách có dữ liệu hợp lệ, trong khi Bronze và Silver thấp hơn nhiều. Ba là nhóm không dùng giảm giá có trung vị chi tiêu cao hơn 110,3, nhưng đây chỉ là liên hệ quan sát. Bốn là có 32 khách chi tiêu cao nhưng đã lâu chưa mua, phù hợp để ưu tiên tiếp cận lại. Năm là San Francisco nổi bật về chi tiêu và thời gian từ lần mua gần nhất. Kết quả giúp đặt ưu tiên phân tích và thử nghiệm tiếp theo; nó chưa chứng minh nguyên nhân hay dự đoán tương lai. Dữ liệu còn thiếu ngày giao dịch, giá trị giảm giá và lịch sử mua lặp lại.

**Chuyển sang demo:** “Bây giờ nhóm sẽ cho thấy các kết quả này thay đổi thế nào khi lọc một nhóm khách cụ thể.”

## Slide 12 — Demo dashboard (5:00)

**0:00–0:40 — Mở dashboard**

> Nhóm chạy `python3 -m streamlit run dashboard.py`. Trạng thái ban đầu là toàn bộ 350 khách. Sáu KPI ở đầu trang cho biết quy mô tập lọc, tổng chi tiêu ghi nhận, chi tiêu trung vị, điểm đánh giá trung bình, tỷ lệ dùng giảm giá và trung vị số ngày chưa mua.

**0:40–2:00 — Lọc thành phố New York**

> Trong bộ lọc Thành phố, nhóm chỉ chọn New York. Tập còn 59 khách. Chúng ta quan sát sáu KPI thay đổi theo cùng một tập lọc; ở tab Tổng quan, CH10 bây giờ mô tả hồ sơ của nhóm khách thuộc thành phố này.

**2:00–3:30 — Xem phân vùng giữ chân**

> Sang tab Chi tiêu & hành vi mua, nhóm xem CH07. Các chấm chỉ còn khách New York, nhưng hai đường ngưỡng vẫn cố định theo toàn bộ dữ liệu sạch. Nhờ vậy, nhóm đang so sánh khách New York với cùng chuẩn phân vùng ban đầu, không tự đổi chuẩn mỗi khi lọc.

**3:30–4:30 — Đặt lại bộ lọc, xem hài lòng và giảm giá**

> Trước tiên nhóm đặt lại bộ lọc về 350 khách, rồi sang tab Hài lòng & giảm giá để xem CH08 và CH09. Việc đặt lại là cần thiết vì cả 59 khách New York đều có giảm giá, nên khi chỉ lọc New York, CH09 không còn nhóm “Không” để so sánh. CH08 so sánh tỷ lệ hài lòng trong từng hạng; CH09 so sánh chi tiêu và số sản phẩm giữa hai nhóm giảm giá.

**4:30–5:00 — Đặt lại và kết luận**

> Dashboard giúp khám phá các nhóm cụ thể, còn các kết luận vẫn là thống kê mô tả. Muốn đo hiệu quả khuyến mãi hay dự đoán rời bỏ, cần dữ liệu giao dịch theo thời gian và thiết kế phân tích bổ sung.

**Chuẩn bị trước khi nói:** mở sẵn terminal tại thư mục dự án, khởi chạy dashboard và kiểm tra trình duyệt để tiết kiệm thời gian. Nếu ứng dụng đã chạy, chỉ chuyển từ PowerPoint sang trình duyệt.

**Bản demo chi tiết:** xem [kich_ban_demo_dashboard_5_phut.md](kich_ban_demo_dashboard_5_phut.md).

## Slide 13 — Q&A

> Phần trình bày và demo của nhóm đến đây là kết thúc. Nhóm xin cảm ơn thầy cô và các bạn. Nhóm sẵn sàng trả lời câu hỏi.

### Ba câu hỏi có thể được hỏi

1. **Vì sao dùng median thay vì mean?** Median diễn tả giá trị giữa và ít bị chi phối bởi một số khách chi tiêu rất cao. Mean vẫn được dùng ở nơi cần trung bình, chẳng hạn điểm đánh giá.
2. **Có thể kết luận giảm giá không hiệu quả không?** Chưa thể. Biểu đồ chỉ so sánh hai nhóm quan sát; thiếu giá trị giảm giá, cơ chế chọn khách và dữ liệu trước/sau.
3. **32 khách ở CH07 có chắc sẽ rời bỏ không?** Không. Đó là nhóm ưu tiên xem xét dựa trên chi tiêu và số ngày chưa mua, chưa phải dự đoán churn.
