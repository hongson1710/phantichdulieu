"""Build a 13-slide IE313 presentation from Slides.pptx and notebook charts.

The first two slide XML parts are copied byte-for-byte from the template.
All authored labels and chart explanations remain editable PowerPoint text.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "thuyetrinh" / "Slides.pptx"
OUTPUT = ROOT / "thuyetrinh" / "phantichhanhvikhachhang.pptx"
CHARTS = ROOT / "charts"

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_R = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
ET.register_namespace("p", P)
ET.register_namespace("a", A)
ET.register_namespace("r", R)
ET.register_namespace("", CT)

EMU = 914400
SLIDE_WIDTH = 12192000
SLIDE_HEIGHT = 6858000
INK = "18212B"
MUTED = "4B5563"
ACCENT = "D9534F"


def inch(value: float) -> int:
    return int(round(value * EMU))


def elm(namespace: str, tag: str, attrs: dict | None = None) -> ET.Element:
    return ET.Element(f"{{{namespace}}}{tag}", attrs or {})


def add_text(
    tree: ET.Element,
    shape_id: int,
    name: str,
    text: str,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    size: int = 22,
    color: str = INK,
    bold: bool = False,
    align: str = "l",
) -> None:
    shape = ET.SubElement(tree, f"{{{P}}}sp")
    nonvisual = ET.SubElement(shape, f"{{{P}}}nvSpPr")
    ET.SubElement(nonvisual, f"{{{P}}}cNvPr", {"id": str(shape_id), "name": name})
    ET.SubElement(nonvisual, f"{{{P}}}cNvSpPr", {"txBox": "1"})
    ET.SubElement(nonvisual, f"{{{P}}}nvPr")
    shape_properties = ET.SubElement(shape, f"{{{P}}}spPr")
    transform = ET.SubElement(shape_properties, f"{{{A}}}xfrm")
    ET.SubElement(transform, f"{{{A}}}off", {"x": str(inch(x)), "y": str(inch(y))})
    ET.SubElement(transform, f"{{{A}}}ext", {"cx": str(inch(w)), "cy": str(inch(h))})
    geometry = ET.SubElement(shape_properties, f"{{{A}}}prstGeom", {"prst": "rect"})
    ET.SubElement(geometry, f"{{{A}}}avLst")
    ET.SubElement(shape_properties, f"{{{A}}}noFill")
    line = ET.SubElement(shape_properties, f"{{{A}}}ln")
    ET.SubElement(line, f"{{{A}}}noFill")
    text_body = ET.SubElement(shape, f"{{{P}}}txBody")
    ET.SubElement(
        text_body,
        f"{{{A}}}bodyPr",
        {
            "wrap": "square",
            "anchor": "ctr",
            "lIns": "0",
            "rIns": "0",
            "tIns": "0",
            "bIns": "0",
        },
    )
    ET.SubElement(text_body, f"{{{A}}}lstStyle")
    paragraph = ET.SubElement(text_body, f"{{{A}}}p")
    ET.SubElement(paragraph, f"{{{A}}}pPr", {"algn": align})
    run = ET.SubElement(paragraph, f"{{{A}}}r")
    properties = ET.SubElement(
        run,
        f"{{{A}}}rPr",
        {"lang": "vi-VN", "sz": str(size * 100), **({"b": "1"} if bold else {})},
    )
    fill = ET.SubElement(properties, f"{{{A}}}solidFill")
    ET.SubElement(fill, f"{{{A}}}srgbClr", {"val": color})
    ET.SubElement(properties, f"{{{A}}}latin", {"typeface": "Calibri"})
    ET.SubElement(run, f"{{{A}}}t").text = text
    ET.SubElement(paragraph, f"{{{A}}}endParaRPr", {"lang": "vi-VN"})


def add_picture(
    tree: ET.Element,
    shape_id: int,
    name: str,
    relationship_id: str,
    x: float,
    y: float,
    w: float,
    h: float,
) -> None:
    picture = ET.SubElement(tree, f"{{{P}}}pic")
    nonvisual = ET.SubElement(picture, f"{{{P}}}nvPicPr")
    ET.SubElement(nonvisual, f"{{{P}}}cNvPr", {"id": str(shape_id), "name": name})
    picture_props = ET.SubElement(nonvisual, f"{{{P}}}cNvPicPr")
    ET.SubElement(picture_props, f"{{{A}}}picLocks", {"noChangeAspect": "1"})
    ET.SubElement(nonvisual, f"{{{P}}}nvPr")
    blip_fill = ET.SubElement(picture, f"{{{P}}}blipFill")
    ET.SubElement(blip_fill, f"{{{A}}}blip", {f"{{{R}}}embed": relationship_id})
    stretch = ET.SubElement(blip_fill, f"{{{A}}}stretch")
    ET.SubElement(stretch, f"{{{A}}}fillRect")
    shape_properties = ET.SubElement(picture, f"{{{P}}}spPr")
    transform = ET.SubElement(shape_properties, f"{{{A}}}xfrm")
    ET.SubElement(transform, f"{{{A}}}off", {"x": str(inch(x)), "y": str(inch(y))})
    ET.SubElement(transform, f"{{{A}}}ext", {"cx": str(inch(w)), "cy": str(inch(h))})
    geometry = ET.SubElement(shape_properties, f"{{{A}}}prstGeom", {"prst": "rect"})
    ET.SubElement(geometry, f"{{{A}}}avLst")


def empty_slide() -> tuple[ET.Element, ET.Element]:
    slide = elm(P, "sld")
    content = ET.SubElement(slide, f"{{{P}}}cSld")
    tree = ET.SubElement(content, f"{{{P}}}spTree")
    group = ET.SubElement(tree, f"{{{P}}}nvGrpSpPr")
    ET.SubElement(group, f"{{{P}}}cNvPr", {"id": "1", "name": ""})
    ET.SubElement(group, f"{{{P}}}cNvGrpSpPr")
    ET.SubElement(group, f"{{{P}}}nvPr")
    group_props = ET.SubElement(tree, f"{{{P}}}grpSpPr")
    transform = ET.SubElement(group_props, f"{{{A}}}xfrm")
    for tag in ["off", "ext", "chOff", "chExt"]:
        attrs = {"x": "0", "y": "0"} if "off" in tag.lower() else {"cx": "0", "cy": "0"}
        ET.SubElement(transform, f"{{{A}}}{tag}", attrs)
    color_mapping = ET.SubElement(slide, f"{{{P}}}clrMapOvr")
    ET.SubElement(color_mapping, f"{{{A}}}masterClrMapping")
    return slide, tree


def fit_chart(path: Path, x: float, y: float, w: float, h: float) -> tuple[float, float, float, float]:
    # Chart images come from the notebook and must remain uncropped.
    from PIL import Image

    with Image.open(path) as image:
        width, height = image.size
    scale = min(w / width, h / height)
    actual_width, actual_height = width * scale, height * scale
    return (x + (w - actual_width) / 2, y + (h - actual_height) / 2, actual_width, actual_height)


def slide_contents(number: int, tree: ET.Element) -> list[str]:
    """Add native text and pictures; return chart paths in relationship order."""
    drawings: list[str] = []
    next_id = 2

    def text(name: str, value: str, x: float, y: float, w: float, h: float, **style: object) -> None:
        nonlocal next_id
        add_text(tree, next_id, name, value, x, y, w, h, **style)
        next_id += 1

    def picture(name: str, filename: str, x: float, y: float, w: float, h: float) -> None:
        nonlocal next_id
        chart_path = CHARTS / filename
        actual = fit_chart(chart_path, x, y, w, h)
        relationship_id = f"rId{len(drawings) + 2}"
        add_picture(tree, next_id, name, relationship_id, *actual)
        next_id += 1
        drawings.append(filename)

    def title(value: str) -> None:
        text("Slide title", value, .72, .36, 11.9, .64, size=29, bold=True)
        text("Section rule", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", .72, .98, 11.86, .13, size=10, color=ACCENT)

    if number == 3:
        title("1. Giới thiệu tổng quan")
        text("Purpose", "Khám phá hành vi khách hàng thương mại điện tử từ 350 hồ sơ", .82, 1.42, 11.6, .55, size=26, bold=True)
        for index, line in enumerate([
            "Phân khúc: khách hàng chi tiêu ra sao và lần mua gần nhất cách bao lâu?",
            "Hài lòng: các hạng thành viên khác nhau như thế nào?",
            "Khuyến mãi: nhóm dùng giảm giá có chi tiêu và số sản phẩm khác biệt không?",
            "Giữ chân: nhóm nào nên ưu tiên tái kích hoạt?",
            "Thành phố: hành vi mua và mức hài lòng khác nhau ra sao?",
        ]):
            text(f"Question {index + 1}", f"{index + 1}. {line}", .95, 2.18 + index * .74, 11.45, .55, size=20)
        text("Agenda", "Dữ liệu → Phương pháp → Phân tích thăm dò → Kết quả → Demo", .95, 6.4, 11.3, .36, size=16, color=MUTED)
    elif number == 4:
        title("2. Mô tả bộ dữ liệu")
        text("Dataset size", "350 khách hàng  |  11 cột dữ liệu  |  1 dòng/khách", .82, 1.38, 11.6, .6, size=25, bold=True)
        for y, heading, body in [
            (2.25, "Nhân khẩu học", "Age, Gender, City"),
            (3.15, "Hành vi mua", "Total Spend, Items Purchased, Discount Applied, Days Since Last Purchase"),
            (4.05, "Quan hệ và đánh giá", "Membership Type, Average Rating, Satisfaction Level"),
        ]:
            text(heading, heading, .95, y, 3.0, .42, size=21, bold=True)
            text(f"{heading} columns", body, 4.05, y, 8.3, .62, size=20)
        text("Data quality", "2 giá trị Satisfaction Level thiếu; các phân tích khác vẫn giữ hai khách này.", .95, 5.28, 11.4, .6, size=19)
        text("Data source", "Nguồn: data/E-commerce_Customer_Behavior.csv. Total Spend chưa xác định đơn vị tiền tệ.", .95, 6.36, 11.35, .42, size=15, color=MUTED)
    elif number == 5:
        title("3. Phương pháp phân tích")
        steps = [
            ("01", "Nạp và làm sạch", "Kiểm tra trùng, thiếu, kiểu dữ liệu và phạm vi hợp lệ."),
            ("02", "Lọc chung", "Một tập khách được dùng đồng thời cho KPI và các biểu đồ."),
            ("03", "Thống kê mô tả", "Đếm khách, median, mean, tỷ lệ trong nhóm và boxplot."),
            ("04", "Phân vùng có quy tắc", "Ngưỡng chi tiêu 775,2 và 23 ngày lấy từ toàn bộ dữ liệu sạch."),
        ]
        for index, (ordinal, heading, body) in enumerate(steps):
            y = 1.47 + index * 1.19
            text(f"Step {ordinal}", ordinal, .86, y, .75, .55, size=25, bold=True, color=ACCENT)
            text(f"Step title {ordinal}", heading, 1.7, y, 3.4, .43, size=22, bold=True)
            text(f"Step detail {ordinal}", body, 5.05, y, 7.36, .72, size=19)
        text("Caution", "Các khác biệt quan sát được không chứng minh quan hệ nhân quả hoặc dự đoán rời bỏ.", .95, 6.45, 11.4, .37, size=16, color=MUTED)
    elif number == 6:
        title("4. Phân tích thăm dò: hạng thành viên và chi tiêu")
        picture("CH03 membership donut", "CH03_co_cau_hang_thanh_vien.png", .66, 1.27, 4.35, 4.61)
        picture("CH05 spend by membership", "CH05_chi_tieu_theo_hang.png", 5.13, 1.34, 7.53, 4.39)
        text("Membership explanation", "Bronze, Silver và Gold có quy mô gần bằng nhau: 116, 117 và 117 khách.", .82, 5.92, 11.55, .45, size=18)
        text("Membership finding", "Median chi tiêu: Gold 1.210,6; Silver 770,2; Bronze 475,25 (đơn vị chưa xác định).", .82, 6.38, 11.55, .4, size=17, color=MUTED)
    elif number == 7:
        title("4. Phân tích thăm dò: phân vùng để giữ chân")
        picture("CH07 customer segments", "CH07_so_ngay_va_chi_tieu.png", .78, 1.25, 11.78, 4.98)
        text("Retention finding", "32 khách chi tiêu cao nhưng mua đã lâu là nhóm ưu tiên tái kích hoạt.", .82, 6.27, 11.6, .45, size=20, bold=True)
        text("Retention caveat", "Ngưỡng: 775,2 chi tiêu và 23 ngày; đây là phân nhóm mô tả.", .82, 6.7, 11.6, .3, size=15, color=MUTED)
    elif number == 8:
        title("4. Phân tích thăm dò: mức độ hài lòng")
        picture("CH08 satisfaction by membership", "CH08_hai_long_theo_hang.png", .87, 1.22, 11.58, 5.02)
        text("Satisfaction finding", "Gold: 100% hài lòng; Silver: 6,8%; Bronze: 0% trong số khách có dữ liệu hợp lệ.", .82, 6.27, 11.68, .45, size=19, bold=True)
        text("Satisfaction denominator", "Tỷ lệ được tính riêng trong từng hạng; 2 khách Bronze thiếu mức hài lòng.", .82, 6.72, 11.65, .3, size=15, color=MUTED)
    elif number == 9:
        title("4. Phân tích thăm dò: tình trạng giảm giá")
        picture("CH09 discount comparison", "CH09_chi_tieu_theo_giam_gia.png", .81, 1.23, 11.7, 4.95)
        text("Discount finding", "Median chi tiêu: không giảm giá 800,9; có giảm giá 690,6. Cả hai nhóm mua median 12 sản phẩm.", .82, 6.26, 11.7, .5, size=18, bold=True)
        text("Discount caveat", "Đây là so sánh quan sát; dữ liệu không cho phép kết luận giảm giá gây ra khác biệt.", .82, 6.73, 11.7, .3, size=15, color=MUTED)
    elif number == 10:
        title("4. Phân tích thăm dò: hành vi theo thành phố")
        picture("CH10 city behavior profile", "CH10_ho_so_hanh_vi_theo_thanh_pho.png", .8, 1.2, 11.74, 5.08)
        text("City finding", "San Francisco có median chi tiêu 1.470,5 và median 11 ngày chưa mua trong tập dữ liệu.", .82, 6.3, 11.67, .42, size=18, bold=True)
        text("City color legend", "Số trong ô là giá trị thực; màu được chuẩn hóa riêng cho từng chỉ tiêu.", .82, 6.72, 11.67, .3, size=15, color=MUTED)
    elif number == 11:
        title("5. Kết quả đạt được")
        lines = [
            ("Phân khúc", "Gold có median chi tiêu cao nhất: 1.210,6."),
            ("Hài lòng", "Gold đạt 100% hài lòng trong 117 khách có mức hợp lệ."),
            ("Khuyến mãi", "Nhóm không giảm giá có median chi tiêu cao hơn 110,3."),
            ("Giữ chân", "32 khách chi tiêu cao, mua đã lâu cần được ưu tiên tiếp cận."),
            ("Thành phố", "San Francisco dẫn đầu median chi tiêu; thời gian từ lần mua gần nhất thấp nhất."),
        ]
        for index, (label, finding) in enumerate(lines):
            y = 1.46 + index * 1.0
            text(f"Finding label {index}", label, .84, y, 2.2, .5, size=20, bold=True, color=ACCENT)
            text(f"Finding detail {index}", finding, 3.06, y, 9.41, .65, size=19)
        text("Limits", "Giới hạn: chưa có ngày giao dịch, giá trị giảm giá và lịch sử mua lặp lại; các kết quả là mô tả.", .85, 6.55, 11.66, .34, size=15, color=MUTED)
    elif number == 12:
        title("6. Demo dashboard")
        text("Demo timing", "5 phút: đi từ toàn bộ dữ liệu đến một nhóm khách cụ thể", .83, 1.5, 11.64, .55, size=26, bold=True)
        for index, item in enumerate([
            "Mở dashboard và xác nhận 350 khách cùng 6 KPI.",
            "Chọn New York: còn 59 khách; quan sát CH10 và các KPI đổi theo lọc.",
            "Chọn hạng thành viên hoặc trạng thái giảm giá để xem CH07–CH09.",
            "Đặt lại bộ lọc và nhắc lại giới hạn: đây là phân tích mô tả.",
        ]):
            text(f"Demo step {index + 1}", f"{index + 1}. {item}", .96, 2.35 + index * .84, 11.36, .62, size=20)
        text("Demo command", "Chạy từ thư mục dự án: python3 -m streamlit run dashboard.py", .96, 6.37, 11.35, .37, size=16, color=MUTED)
    else:
        raise ValueError(f"Không có nội dung cho slide {number}")
    return drawings


def relationships_for_slide(images: list[str]) -> bytes:
    root = elm(PKG_R, "Relationships")
    ET.SubElement(
        root,
        f"{{{PKG_R}}}Relationship",
        {
            "Id": "rId1",
            "Type": f"{R}/slideLayout",
            "Target": "../slideLayouts/slideLayout2.xml",
        },
    )
    for index, filename in enumerate(images, start=2):
        ET.SubElement(
            root,
            f"{{{PKG_R}}}Relationship",
            {"Id": f"rId{index}", "Type": f"{R}/image", "Target": f"../media/{filename}"},
        )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def build() -> None:
    with ZipFile(SOURCE) as original:
        existing = {name: original.read(name) for name in original.namelist()}

    # Slides 3–12 are authored; slide 13 reuses the template's Q&A slide.
    original_qa = existing["ppt/slides/slide9.xml"]
    original_qa_rels = existing["ppt/slides/_rels/slide9.xml.rels"]
    for slide_number in range(3, 13):
        slide, tree = empty_slide()
        chart_files = slide_contents(slide_number, tree)
        existing[f"ppt/slides/slide{slide_number}.xml"] = ET.tostring(
            slide, encoding="utf-8", xml_declaration=True
        )
        existing[f"ppt/slides/_rels/slide{slide_number}.xml.rels"] = relationships_for_slide(chart_files)
        for filename in chart_files:
            existing[f"ppt/media/{filename}"] = (CHARTS / filename).read_bytes()
    existing["ppt/slides/slide13.xml"] = original_qa
    existing["ppt/slides/_rels/slide13.xml.rels"] = original_qa_rels

    presentation = ET.fromstring(existing["ppt/presentation.xml"])
    slide_ids = presentation.find(f"{{{P}}}sldIdLst")
    assert slide_ids is not None
    for index in range(10, 14):
        ET.SubElement(
            slide_ids,
            f"{{{P}}}sldId",
            {"id": str(265 + index - 10), f"{{{R}}}id": f"rId{index + 5}"},
        )
    existing["ppt/presentation.xml"] = ET.tostring(
        presentation, encoding="utf-8", xml_declaration=True
    )

    presentation_rels = ET.fromstring(existing["ppt/_rels/presentation.xml.rels"])
    for index in range(10, 14):
        ET.SubElement(
            presentation_rels,
            f"{{{PKG_R}}}Relationship",
            {"Id": f"rId{index + 5}", "Type": f"{R}/slide", "Target": f"slides/slide{index}.xml"},
        )
    existing["ppt/_rels/presentation.xml.rels"] = ET.tostring(
        presentation_rels, encoding="utf-8", xml_declaration=True
    )

    content_types = ET.fromstring(existing["[Content_Types].xml"])
    if not any(child.attrib.get("Extension") == "png" for child in content_types):
        ET.SubElement(content_types, f"{{{CT}}}Default", {"Extension": "png", "ContentType": "image/png"})
    for index in range(10, 14):
        ET.SubElement(
            content_types,
            f"{{{CT}}}Override",
            {
                "PartName": f"/ppt/slides/slide{index}.xml",
                "ContentType": "application/vnd.openxmlformats-officedocument.presentationml.slide+xml",
            },
        )
    existing["[Content_Types].xml"] = ET.tostring(
        content_types, encoding="utf-8", xml_declaration=True
    )

    app_path = "docProps/app.xml"
    if app_path in existing:
        app = ET.fromstring(existing[app_path])
        for element in app.iter():
            if element.tag.endswith("}Slides"):
                element.text = "13"
        existing[app_path] = ET.tostring(app, encoding="utf-8", xml_declaration=True)

    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as deck:
        for name, content in existing.items():
            deck.writestr(name, content)
    print(OUTPUT)


if __name__ == "__main__":
    build()
