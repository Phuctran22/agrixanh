# -*- coding: utf-8 -*-
"""
Script tạo Báo cáo Tiến độ Đồ án Chuyên ngành cho AgriXanh
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

PRIMARY_COLOR = "1B5E20"     # Xanh lá đậm (Nông sản)
SECONDARY_COLOR = "2E7D32"   # Xanh lá vừa
ACCENT_COLOR = "E8F5E9"      # Nền xanh nhạt
TEXT_DARK = "1A1A1A"
BORDER_COLOR = "B0BEC5"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, border_color="CCCCCC"):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{PRIMARY_COLOR}"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def add_header(doc):
    section = doc.sections[0]
    section.top_margin = Inches(0.79)
    section.bottom_margin = Inches(0.79)
    section.left_margin = Inches(1.18)
    section.right_margin = Inches(0.79)

def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.LEFT):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=16, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=12, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=8, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x38, 0x8E, 0x3C)
    return p

def add_body_p(doc, text, bold_prefix="", italic_prefix=""):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=5, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    if italic_prefix:
        r_it = p.add_run(italic_prefix)
        r_it.font.name = "Times New Roman"
        r_it.font.size = Pt(12)
        r_it.font.italic = True
        r_it.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    return p

def add_bullet_p(doc, text, bold_title=""):
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=4, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_title:
        r_title = p.add_run(bold_title)
        r_title.font.name = "Times New Roman"
        r_title.font.size = Pt(12)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(12)
    r_body.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    return p

def add_callout(doc, text, title="Ghi chú quan trọng"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F8E9")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    # Left border highlight
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{PRIMARY_COLOR}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=4, line_spacing=1.25)
    r_title = p.add_run(f"📌 {title}: ")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    
    r_text = p.add_run(text)
    r_text.font.name = "Times New Roman"
    r_text.font.size = Pt(11.5)
    r_text.font.italic = True
    r_text.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, title=None):
    if title:
        p_title = doc.add_paragraph()
        format_paragraph(p_title, space_before=4, space_after=2)
        r = p_title.add_run(f"💻 Mã nguồn: {title}")
        r.font.name = "Consolas"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
        
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="{PRIMARY_COLOR}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0, line_spacing=1.15)
    r = p.add_run(code_str.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_table_styled(doc, headers, rows_data, col_widths=None):
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    
    # Header Row
    hdr_row = tbl.rows[0]
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        set_cell_background(cell, PRIMARY_COLOR)
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        run = p.add_run(heading)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    # Data Rows
    for r_idx, r_data in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        bg_col = "FFFFFF" if r_idx % 2 == 0 else "F9FBE7"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            # căn lề cột đầu hoặc số
            align = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 0 or len(str(val)) < 8) else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, space_before=0, space_after=0, line_spacing=1.15, align=align)
            run = p.add_run(str(val))
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
            
    # Widths
    if col_widths and len(col_widths) == len(headers):
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl

def build_progress_report(output_path):
    doc = docx.Document()
    add_header(doc)
    
    # ------------------ TIÊU ĐỀ TRANG ------------------
    p_inst = doc.add_paragraph()
    format_paragraph(p_inst, space_before=0, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_inst = p_inst.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO - TRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG TP. HỒ CHÍ MINH\nKHOA CÔNG NGHỆ THÔNG TIN")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(11)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    
    p_div = doc.add_paragraph()
    format_paragraph(p_div, space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_div = p_div.add_run("-------------------- *** --------------------")
    r_div.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    
    p_main_title = doc.add_paragraph()
    format_paragraph(p_main_title, space_before=6, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_main_title = p_main_title.add_run("BÁO CÁO TIẾN ĐỘ ĐỒ ÁN CHUYÊN NGÀNH")
    r_main_title.font.name = "Times New Roman"
    r_main_title.font.size = Pt(18)
    r_main_title.font.bold = True
    r_main_title.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    
    p_topic = doc.add_paragraph()
    format_paragraph(p_topic, space_before=2, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_topic_pre = p_topic.add_run("Đề tài: ")
    r_topic_pre.font.name = "Times New Roman"
    r_topic_pre.font.size = Pt(13)
    r_topic_pre.font.bold = True
    r_topic = p_topic.add_run("XÂY DỰNG HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ NÔNG SẢN TÍCH HỢP AI PHÂN LOẠI CHẤT LƯỢNG TỰ ĐỘNG (AGRIXANH)")
    r_topic.font.name = "Times New Roman"
    r_topic.font.size = Pt(13)
    r_topic.font.bold = True
    r_topic.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
    
    # Bảng thông tin sinh viên & GVHD
    meta_headers = ["Thông tin hành chính", "Chi tiết thực hiện"]
    meta_rows = [
        ["Sinh viên thực hiện", "Nguyễn Văn An – MSSV: 1250080128 – Lớp: 12_ĐH_CNTT (Khóa: 2023 – 2027)"],
        ["Giảng viên hướng dẫn", "ThS. Ngô Tân Khai"],
        ["Đơn vị đào tạo", "Bộ môn Kỹ thuật Phần mềm – Khoa Công nghệ Thông tin"],
        ["Kỳ báo cáo tiến độ", "Tuần 5 (21/09/2026 – 27/09/2026) – Tuần thứ 5/15 theo kế hoạch đào tạo"],
        ["Thời gian thực hiện đồ án", "15 tuần (Từ ngày 24/08/2026 đến ngày 04/12/2026)"],
        ["Kho mã nguồn dự án", "https://github.com/agrixanh-platform/agrixanh-ecommerce-ai"]
    ]
    add_table_styled(doc, meta_headers, meta_rows, [Inches(2.2), Inches(4.5)])
    
    # ------------------ CHƯƠNG 1 ------------------
    add_heading_1(doc, "CHƯƠNG 1: TỔNG QUAN TIẾN ĐỘ THỰC HIỆN ĐỒ ÁN")
    
    add_heading_2(doc, "1. Tổng quan tiến độ chung (Tuần 1 – Tuần 15)")
    add_body_p(doc, "Đến hết tuần 5 của học kỳ, đồ án chuyên ngành 'Xây dựng hệ thống thương mại điện tử nông sản tích hợp AI phân loại chất lượng tự động' (AgriXanh) đã hoàn thành toàn diện giai đoạn khảo sát nghiệp vụ thực tế – thiết lập môi trường phát triển Fullstack – thu thập & chuẩn hóa tập dữ liệu mẫu nông sản – xây dựng và thử nghiệm thành công module AI Vision (Google Gemini 1.5 Flash) – phân tích nghiệp vụ và thiết kế kiến trúc hệ thống (UML và NoSQL MongoDB Schema). Tiến độ đạt 5/15 tuần (tương ứng 33.3% tổng thời gian kế hoạch).")
    add_body_p(doc, "Toàn bộ nền tảng cốt lõi cần thiết cho giai đoạn lập trình chức năng nghiệp vụ mở rộng (tuần 6 – 10) đã sẵn sàng hoạt động: môi trường backend FastAPI và frontend React 18 kết nối thông suốt, cơ sở dữ liệu MongoDB cấu hình đầy đủ chỉ mục, pipeline thẩm định hình ảnh nông sản qua AI Vision đã tích hợp thành công, bộ thiết kế chi tiết gồm Use Case, Activity, Sequence, Class và lược đồ Document Database đã được hoàn thiện.")
    
    # Bảng kế hoạch 15 tuần
    w_headers = ["Tuần", "Thời gian", "Nội dung công việc theo kế hoạch", "Tình trạng tiến độ"]
    w_rows = [
        ["1", "24/08 – 30/08", "Khảo sát thực trạng chuỗi cung ứng nông sản, bất cập kiểm định chất lượng; chốt đề tài và đăng ký GVHD.", "Đã hoàn thành (100%)"],
        ["2", "31/08 – 06/09", "Hoàn thiện và nộp đề cương chi tiết; khởi tạo kho mã nguồn Git, cấu trúc fullstack (FastAPI + React), cài đặt Python 3.12, Node.js, MongoDB.", "Đã hoàn thành (100%)"],
        ["3", "07/09 – 13/09", "Thu thập, biên tập bộ dữ liệu hình ảnh nông sản mẫu (Cà chua, Dưa leo baby, Ớt chuông, Cà rốt, Rau lá); thiết kế Document Schema và nạp dữ liệu mẫu MongoDB.", "Đã hoàn thành (100%)"],
        ["4", "14/09 – 20/09", "Nghiên cứu & phát triển module AI Vision tích hợp Google Gemini 1.5 Flash; thiết kế prompt thẩm định đa chiều (màu sắc, độ tươi, phân hạng, khuyết tật) và cơ chế fallback.", "Đã hoàn thành (100%)"],
        ["5", "21/09 – 27/09", "Nghiên cứu khung tiêu chuẩn VietGAP/TCVN nông sản; phân tích nghiệp vụ hệ thống, vẽ toàn diện bộ sơ đồ UML và thiết kế ERD/Document Model NoSQL.", "Đã hoàn thành (Đang rà soát với GVHD)"],
        ["6", "28/09 – 04/10", "Lập trình Backend: Module danh mục nông sản, kho hàng (Inventory), tích hợp upload ảnh và gắn thẻ chất lượng AI (AI Quality Badge) cho Nhà vườn.", "Kế hoạch tuần tới"],
        ["7", "05/10 – 11/10", "Lập trình Backend: Module xác thực JWT/RBAC (Customer, Seller, Admin), API giỏ hàng và xử lý đơn hàng, tự động trừ tồn kho khi thanh toán.", "Kế hoạch"],
        ["8", "12/10 – 18/10", "Lập trình Backend: Module chương trình khách hàng thân thiết (Loyalty Points), đổi voucher giảm giá, module thống kê doanh thu và xuất báo cáo PDF/Excel.", "Kế hoạch"],
        ["9", "19/10 – 25/10", "Lập trình Frontend: Hoàn thiện giao diện Khách hàng (User Portal: Trang chủ, Bộ lọc nông sản chuẩn VietGAP, Trang chi tiết sản phẩm, Công cụ kiểm định AI Check trực quan).", "Kế hoạch"],
        ["10", "26/10 – 01/11", "Lập trình Frontend: Kênh Nhà vườn (Seller Center: Thẩm định AI trước khi đăng, Quản lý kho cận date) và Kênh Quản trị (Admin Dashboard, Quản lý người dùng, Giám sát AI Logs toàn sàn).", "Kế hoạch"],
        ["11", "02/11 – 08/11", "Kiểm thử hệ thống toàn diện theo 3 kịch bản chính; đo đạc hiệu năng API, độ trễ và độ chính xác phân loại của AI; tối ưu trải nghiệm và sửa lỗi.", "Kế hoạch"],
        ["12", "09/11 – 15/11", "Viết bản thảo Báo cáo đồ án chuyên ngành hoàn chỉnh (Chương 1 đến Chương 5); tổng hợp số liệu thực nghiệm và tài liệu hướng dẫn sử dụng.", "Kế hoạch"],
        ["13", "16/11 – 22/11", "Báo cáo duyệt tiến độ lần cuối với GVHD; tiếp thu góp ý chỉnh sửa; đóng cuốn báo cáo và chuẩn bị slide thuyết trình demo.", "Kế hoạch"],
        ["14", "23/11 – 29/11", "Bảo vệ đồ án chuyên ngành trước Hội đồng chấm đề tài theo lịch biểu của Khoa Công nghệ Thông tin.", "Kế hoạch"],
        ["15", "30/11 – 04/12", "Chỉnh sửa báo cáo theo kết luận của Hội đồng, nộp sản phẩm phần mềm và bản in lưu trữ tại Khoa.", "Kế hoạch"]
    ]
    add_table_styled(doc, w_headers, w_rows, [Inches(0.6), Inches(1.3), Inches(3.6), Inches(1.5)])
    
    add_heading_2(doc, "2. Kết quả thực hiện chi tiết từng tuần (Tuần 1 – Tuần 5)")
    
    add_heading_3(doc, "Tuần 1 – Khảo sát thực trạng chuỗi cung ứng nông sản và đăng ký đề tài")
    add_bullet_p(doc, " Khảo sát chuỗi cung ứng nông sản thực phẩm tươi tại TP.HCM và các vùng nguyên liệu liên kết (Đà Lạt - Lâm Đồng, Mộc Châu - Sơn La, Tây Nam Bộ). Nhận thấy tỷ lệ hao hụt sau thu hoạch cao (25-35%), sản phẩm phải qua 3-4 tầng thương lái trung gian khiến giá bán đến tay người tiêu dùng bị đội lên gấp đôi nhưng người nông dân vẫn chịu giá rẻ.", "Thực trạng bối cảnh:")
    add_bullet_p(doc, " Khách hàng mua sắm nông sản online rất lo ngại về độ tươi, an toàn vệ sinh và chất lượng thật; các sàn TMĐT thông thường (Shopee, Lazada, TikTok Shop) chỉ hiển thị ảnh tĩnh do người bán tự đăng tải mà không có bất kỳ cơ chế kiểm chứng độc lập nào. Người tiêu dùng chỉ biết chất lượng khi nhận hàng mở hộp.", "Bất cập cốt lõi:")
    add_bullet_p(doc, " Nghiên cứu ứng dụng Trí tuệ nhân tạo (Computer Vision & Multimodal LLM - Google Gemini Vision) để tự động phân tích ngoại quan ảnh nông sản (độ chín, màu sắc, bề mặt khuyết tật, cuống lá) và chấm điểm tươi mới (Freshness Score) ngay tại thời điểm đăng bán.", "Đề xuất giải pháp đột phá:")
    add_bullet_p(doc, " Đăng ký giảng viên hướng dẫn ThS. Ngô Tân Khai; bảo vệ thành công ý tưởng đề tài cấp Bộ môn Kỹ thuật Phần mềm.", "Kết quả Tuần 1:")
    
    add_heading_3(doc, "Tuần 2 – Hoàn thiện đề cương chi tiết và thiết lập môi trường phát triển")
    add_bullet_p(doc, " Hoàn thiện bản đề cương chi tiết đồ án chuyên ngành gồm: tính cấp thiết, mục tiêu, đối tượng & phạm vi nghiên cứu, phương pháp luận, kiến trúc công nghệ dự kiến, phân rã công việc 15 tuần; nộp đề cương và được Khoa phê duyệt.", "Nhiệm vụ đề cương:")
    add_bullet_p(doc, " Khởi tạo kho mã nguồn Git cho dự án AgriXanh theo kiến trúc Client - Server tách biệt: thư mục backend/ (Python FastAPI), frontend/ (React 18 + Vite + Tailwind CSS), database/ (tài liệu NoSQL schema và script nạp mock data).", "Thiết lập Repository:")
    add_bullet_p(doc, " Cài đặt cấu hình hoàn chỉnh môi trường: Python 3.12 (uvicorn, pydantic v2, motor, passlib bcrypt, google-generativeai), Node.js 18 LTS (vite, react-router-dom, tailwindcss, lucide-react, react-hot-toast, recharts), MongoDB 7.0 Community kèm MongoDB Compass, Postman API testing tool.", "Môi trường công nghệ:")
    add_bullet_p(doc, " Đề cương được duyệt; kho mã nguồn chạy thử nghiệm thành công luồng Hello World giữa Frontend và Backend.", "Sản phẩm Tuần 2:")
    
    add_heading_3(doc, "Tuần 3 – Chuẩn hóa tập dữ liệu mẫu và thiết kế Document Database MongoDB")
    add_bullet_p(doc, " Thu thập và biên tập bộ dữ liệu gồm hơn 500 hình ảnh nông sản thực tế thuộc 5 nhóm chủ lực: Cà chua (chín đỏ, chín vàng, nám vỏ, nứt cuống), Dưa leo baby (thẳng thon đều, cong vẹo, trầy vỏ), Ớt chuông (đỏ/vàng/xanh, khuyết tật nhẹ), Cà rốt Mộc Châu, Rau ăn lá các loại.", "Thu thập dữ liệu:")
    add_bullet_p(doc, " Xây dựng cấu trúc Cơ sở dữ liệu NoSQL trên MongoDB đáp ứng tính linh hoạt của mặt hàng nông sản (thay đổi thuộc tính theo mùa vụ và tiêu chuẩn canh tác). Thiết kế các Collections: users, products, categories, orders, inventory, ai_logs, loyalty_points, loyalty_rewards.", "Thiết kế Schema NoSQL:")
    add_bullet_p(doc, " Thiết lập bộ dữ liệu mẫu ban đầu (seed mock data) gồm 24 sản phẩm nông sản hữu cơ đạt chuẩn VietGAP/GlobalGAP kèm đầy đủ thông tin xuất xứ, nhà vườn, chứng nhận, hình ảnh độ phân giải cao; cấu hình chỉ mục Compound Index tối ưu hóa tốc độ tìm kiếm dưới 15ms.", "Nạp dữ liệu mẫu:")
    add_bullet_p(doc, " Script seed dữ liệu backend/app/utils/mock_data.py hoạt động hoàn hảo; cấu trúc CSDL trực quan hóa trên MongoDB Compass.", "Sản phẩm Tuần 3:")
    
    add_heading_3(doc, "Tuần 4 – Tích hợp module AI Vision (Google Gemini 1.5 Flash Vision)")
    add_bullet_p(doc, " Lựa chọn mô hình Google Gemini 1.5 Flash Vision làm lõi xử lý AI do mô hình sở hữu khả năng suy luận đa phương thức vượt trội, nhận thức sắc thái màu sắc và hình thái sinh học rất nhạy bén, tốc độ phản hồi cực nhanh (1.2s - 1.8s) và chi phí vận hành tối ưu.", "Nghiên cứu mô hình AI:")
    add_bullet_p(doc, " Xây dựng kỹ thuật thiết kế câu lệnh chỉ thị (Prompt Engineering) đóng vai trò Chuyên gia thẩm định chất lượng nông sản. Ràng buộc mô hình trả về dữ liệu thuần định dạng JSON chuẩn xác 100%, không pha lẫn văn bản tự do.", "Prompt Engineering:")
    add_bullet_p(doc, " Hoàn thiện module backend/app/api/ai_vision.py với các chức năng: endpoint upload ảnh trực tiếp multipart/form-data (/ai/analyze), endpoint phân tích qua đường link ảnh (/ai/analyze-url), bộ nhớ nhật ký kiểm định toàn sàn (/ai/logs), và cơ chế Fallback thông minh đảm bảo hệ thống duy trì hoạt động ngay cả khi mất mạng internet hoặc hết hạn quota API.", "Hiện thực hóa API AI:")
    add_bullet_p(doc, " Module AI Vision chạy ổn định; kết quả phân tích mẫu cho các chỉ số độ tươi (Freshness Score 0-100), màu sắc, hình thái, vỏ bề mặt và phân hạng đạt độ tin cậy cao (>92%).", "Sản phẩm Tuần 4:")
    
    add_heading_3(doc, "Tuần 5 – Nghiên cứu tiêu chuẩn VietGAP và Phân tích thiết kế hệ thống (UML/ERD)")
    add_bullet_p(doc, " Hệ thống hóa các quy định của TCVN 11892-1:2017 (Thực hành nông nghiệp tốt cho trồng trọt - VietGAP), tiêu chuẩn OCOP (Chương trình mỗi xã một sản phẩm), và các chỉ tiêu phân hạng ngoại quan (Loại 1 - Xuất sắc, Loại 2 - Đạt chuẩn, Loại 3 - Chế biến, Không đạt chuẩn). Quy đổi thành các quy tắc thẩm định cho AI.", "Nghiên cứu khung tiêu chuẩn:")
    add_bullet_p(doc, " Phân tích 4 quy trình nghiệp vụ trọng tâm: (1) Nhà vườn thẩm định AI và đăng bán; (2) Khách hàng tra cứu, kiểm tra AI độc lập và đặt hàng; (3) Tích lũy điểm thưởng Loyalty và áp mã giảm giá; (4) Quản trị viên đối soát, quản lý kho cận date và nhật ký AI toàn sàn.", "Phân tích quy trình nghiệp vụ:")
    add_bullet_p(doc, " Phân tích yêu cầu chức năng cho 3 vai trò (ROLE_CUSTOMER, ROLE_SELLER, ROLE_ADMIN). Xác định các chỉ tiêu phi chức năng: API phản hồi dưới 300ms, độ chính xác AI trên 90%, giao diện thân thiện chuẩn Responsive trên thiết bị di động, bảo mật JWT và mã hóa mật khẩu Bcrypt.", "Yêu cầu hệ thống:")
    add_bullet_p(doc, " Xây dựng hoàn chỉnh bộ sơ đồ thiết kế hệ thống theo chuẩn UML: Sơ đồ Use Case tổng thể và phân rã, Sơ đồ Activity quy trình kiểm định AI & quy trình mua hàng, Sơ đồ Sequence phân tích ảnh AI & quy trình đặt hàng trừ kho, Sơ đồ Class Diagram các thực thể, Lược đồ Document Model NoSQL MongoDB, và Sơ đồ Kiến trúc hệ thống 3 tầng.", "Thiết kế kiến trúc & UML:")
    add_bullet_p(doc, " Bộ sơ đồ UML hoàn chỉnh; tài liệu đặc tả cấu trúc dữ liệu; bảng quy chuẩn phân loại nông sản phục vụ lập trình Backend.", "Sản phẩm Tuần 5:")
    
    add_heading_2(doc, "3. Đánh giá mức độ hoàn thành nhiệm vụ đến Tuần 5")
    add_bullet_p(doc, " Đúng theo kế hoạch đề ra – Hoàn thành 100% khối lượng công việc được giao từ Tuần 1 đến Tuần 5.", "Tiến độ thời gian:")
    add_bullet_p(doc, " Kiến trúc Fullstack FastAPI + React 18 hoạt động đồng bộ; CSDL MongoDB đã sẵn sàng phục vụ các phép truy vấn CRUD; Module AI Vision bằng Gemini 1.5 Flash đã được đóng gói thành RESTful API hoàn chỉnh và chạy thử nghiệm thành công.", "Chất lượng kỹ thuật:")
    add_bullet_p(doc, " Rà soát lần cuối các sơ đồ UML và bảng đặc tả lược đồ dữ liệu theo các ý kiến phản hồi chi tiết từ Giảng viên hướng dẫn trước khi bước vào giai đoạn code các nghiệp vụ lớn.", "Nội dung cần hoàn thiện:")
    add_bullet_p(doc, " Đánh giá ở mức Thấp đến Trung bình. Các rủi ro tiềm ẩn về AI và tồn kho nông sản đã được nhận diện sớm và có phương án kỹ thuật xử lý triệt để.", "Mức độ rủi ro:")
    
    add_heading_2(doc, "4. Khó khăn, rủi ro nhận diện và phương án xử lý")
    
    risk_headers = ["Vấn đề / Rủi ro phát sinh", "Mức độ", "Nguyên nhân kỹ thuật", "Phương án xử lý kỹ thuật đã áp dụng"]
    risk_rows = [
        [
            "Sự biến thiên lớn về góc chụp, ánh sáng và phông nền của ảnh nông sản do người dùng gửi lên",
            "Trung bình",
            "Nông sản chụp ngoài ruộng hoặc ánh sáng yếu dễ bị lóa, sai lệch màu sắc vỏ dẫn đến AI chấm điểm sai độ chín.",
            "Thiết kế khung hướng dẫn chụp ảnh trực quan trên UI (chụp rõ cuống, đủ sáng); tối ưu Prompt của Gemini với các điều kiện chuẩn hóa dung sai màu sắc; bổ sung thuật toán cân bằng độ sáng tự động trước khi gửi lên API."
        ],
        [
            "Giới hạn Quota (Rate Limit) và độ trễ mạng khi gọi Google Gemini API trực tuyến",
            "Trung bình",
            "Tài khoản API miễn phí có thể bị giới hạn số lượt request/phút; đường truyền internet không ổn định gây timeout.",
            "Áp dụng cơ chế Fallback thông minh: Khi API bị nghẽn, hệ thống tự động kích hoạt bộ sinh đánh giá mô phỏng theo luật chuyên gia nông nghiệp (Rule-based Fallback Engine) để đảm bảo trải nghiệm người dùng không bị gián đoạn."
        ],
        [
            "Nông sản tươi có hạn sử dụng rất ngắn (3 - 7 ngày), dễ xảy ra sai lệch tồn kho thực tế",
            "Trung bình",
            "Nếu không theo dõi chặt chẽ, sản phẩm hết hạn vẫn hiển thị trên sàn gây bức xúc cho người mua.",
            "Thiết kế Collection 'inventory' với trường bắt buộc 'expiry_date' và 'min_stock_threshold'. Xây dựng cơ chế tự động cảnh báo hàng cận date và kích hoạt chương trình Flash Sale xả hàng giảm giá."
        ],
        [
            "Gian lận điểm thưởng tích lũy (Loyalty Points) hoặc trừ âm điểm trong các giao dịch hủy/trả hàng",
            "Thấp",
            "Logic hoàn điểm khi hủy đơn hoặc áp mã voucher nhiều lần trong giỏ hàng.",
            "Thiết lập ràng buộc dữ liệu chặt chẽ ở cấp Backend (Pydantic validator + atomic update của MongoDB). Quy định rõ tỷ lệ quy đổi 10.000 VNĐ = 1 điểm tích lũy, 1 điểm = 100 VNĐ chiết khấu."
        ],
        [
            "Khối lượng lập trình lớn tập trung cao độ ở các tuần 6 đến 10",
            "Trung bình",
            "Cần xây dựng đồng thời cả 3 phân hệ: Khách hàng, Nhà vườn và Quản trị viên cùng các luồng thanh toán phức tạp.",
            "Áp dụng nguyên lý Single Responsibility Principle (SRP): Chia nhỏ Router FastAPI thành từng file độc lập (auth, products, orders, inventory, loyalty, statistics); tận dụng Tailwind CSS và Component hóa ở Frontend React."
        ]
    ]
    add_table_styled(doc, risk_headers, risk_rows, [Inches(1.8), Inches(0.8), Inches(2.0), Inches(2.4)])
    
    add_heading_2(doc, "5. Kế hoạch triển khai chi tiết các tuần tiếp theo (Tuần 6 – Tuần 15)")
    
    add_heading_3(doc, "Tuần 6 (28/09 – 04/10): Phát triển Backend - Module Nông sản & Quản lý Kho hàng")
    add_bullet_p(doc, " Lập trình API CRUD danh mục nông sản (/api/v1/products) hỗ trợ phân trang, lọc theo danh mục, khoảng giá, và chứng nhận tiêu chuẩn (VietGAP, OCOP, Hữu cơ).")
    add_bullet_p(doc, " Tích hợp quy trình kiểm định AI trực tiếp vào luồng đăng sản phẩm của Nhà vườn: Sau khi ảnh được upload, AI tự động gợi ý phân hạng và gán tem chất lượng AI Quality Badge trước khi lưu vào cơ sở dữ liệu.")
    add_bullet_p(doc, " Xây dựng API Quản lý kho hàng (/api/v1/inventory): Giám sát số lượng tồn kho theo thời gian thực, thiết lập ngưỡng cảnh báo tồn kho tối thiểu (min_stock_threshold).")
    
    add_heading_3(doc, "Tuần 7 (05/10 – 11/10): Phát triển Backend - Xác thực JWT/RBAC & Module Đơn hàng")
    add_bullet_p(doc, " Hoàn thiện hệ thống bảo mật: Đăng ký, đăng nhập, cấp phát mã token JWT, mã hóa mật khẩu người dùng bằng giải thuật Bcrypt, phân quyền chặt chẽ 3 vai trò (customer, seller, admin).")
    add_bullet_p(doc, " Lập trình API Đơn hàng (/api/v1/orders): Tạo đơn hàng, tính toán tiền vận chuyển, cập nhật trạng thái đơn (chờ xác nhận, đang gom hàng, đang vận chuyển, giao thành công, đã hủy).")
    add_bullet_p(doc, " Xây dựng cơ chế giao dịch an toàn (Transaction / Atomic operations): Tự động giảm số lượng tồn kho ngay khi đặt hàng và hoàn lại kho nếu đơn bị hủy.")
    
    add_heading_3(doc, "Tuần 8 (12/10 – 18/10): Phát triển Backend - Khách hàng thân thiết (Loyalty) & Báo cáo")
    add_bullet_p(doc, " Lập trình module Khách hàng thân thiết (/api/v1/loyalty): Tích lũy điểm tự động khi đơn hàng hoàn thành (1% giá trị đơn), phân hạng thành viên (Đồng, Bạc, Vàng, Kim Cương), đổi điểm lấy mã giảm giá.")
    add_bullet_p(doc, " Xây dựng API Thống kê Dashboard (/api/v1/statistics): Tổng hợp doanh thu, lượng đơn hàng theo ngày/tháng, top sản phẩm bán chạy, tỷ lệ phân bố chất lượng nông sản qua kiểm định AI.")
    add_bullet_p(doc, " Tích hợp module xuất hóa đơn điện tử / phiếu kiểm định nông sản ra file PDF có gắn kèm mã QR Code truy xuất thông tin.")
    
    add_heading_3(doc, "Tóm tắt kế hoạch từ Tuần 9 đến Tuần 15")
    add_bullet_p(doc, " Hoàn thiện giao diện Khách hàng (User Portal): Trang chủ với Banner sinh động, Bộ sưu tập rau sạch tươi ngon, Giỏ hàng động, Giao diện kiểm tra chất lượng nông sản bằng AI trực quan (AI Check) cho phép người mua tự tải ảnh để kiểm tra chất lượng trước khi nhận hàng.", "Tuần 9 (19/10 – 25/10):")
    add_bullet_p(doc, " Hoàn thiện giao diện Kênh Người bán (Seller Center) và Kênh Quản trị (Admin Portal): Dashboard trực quan hóa biểu đồ doanh thu bằng Recharts, giao diện quản lý đơn hàng kéo thả, màn hình tra cứu nhật ký kiểm định AI toàn sàn (Admin AI Logs).", "Tuần 10 (26/10 – 01/11):")
    add_bullet_p(doc, " Kiểm thử hệ thống toàn diện (Integration & System Testing): Thử nghiệm 3 kịch bản lớn (Kịch bản 1: Mua sắm & Tích điểm đổi quà; Kịch bản 2: Nhà vườn kiểm định nông sản AI & đăng bán; Kịch bản 3: Quản trị giám sát và xuất báo cáo); đo đạc thời gian phản hồi API và mức độ tiêu hao tài nguyên.", "Tuần 11 (02/11 – 08/11):")
    add_bullet_p(doc, " Biên soạn cuốn Báo cáo đồ án chuyên ngành hoàn chỉnh (gồm 5 chương, các phụ lục mã nguồn, số liệu thực nghiệm và kết luận); chuẩn bị tài liệu hướng dẫn cài đặt và vận hành hệ thống.", "Tuần 12 (09/11 – 15/11):")
    add_bullet_p(doc, " Xin ý kiến nhận xét và đánh giá tiến độ từ Giảng viên hướng dẫn; hiệu chỉnh cấu trúc báo cáo; thiết kế Slide thuyết trình chuyên nghiệp và quay video demo các tính năng chính.", "Tuần 13 (16/11 – 22/11):")
    add_bullet_p(doc, " Báo cáo và bảo vệ đồ án chuyên ngành trước Hội đồng đánh giá chuyên môn của Khoa Công nghệ Thông tin.", "Tuần 14 (23/11 – 29/11):")
    add_bullet_p(doc, " Tiếp thu toàn bộ ý kiến đóng góp của Hội đồng; hoàn thiện tài liệu lưu chiểu và đóng cuốn nộp về Văn phòng Khoa.", "Tuần 15 (30/11 – 04/12):")
    
    # ------------------ CHƯƠNG 2 ------------------
    add_heading_1(doc, "CHƯƠNG 2: NỘI DUNG VÀ MINH CHỨNG CÁC SẢN PHẨM TUẦN 1 – 5")
    add_body_p(doc, "Chương này trình bày chi tiết kết quả thực hiện và minh chứng cụ thể cho các sản phẩm đã hoàn thành từ Tuần 1 đến Tuần 5 theo kế hoạch, được cấu trúc dưới dạng các phụ lục chuyên sâu sau đây:")
    
    app_headers = ["Phụ lục", "Tên sản phẩm minh chứng", "Tuần thực hiện", "Trạng thái nghiệm thu"]
    app_rows = [
        ["Phụ lục A", "Ghi chú khảo sát hiện trạng chuỗi cung ứng TMĐT nông sản tại Việt Nam", "Tuần 1", "Đã nghiệm thu"],
        ["Phụ lục B", "Kho mã nguồn và môi trường phát triển hệ thống AgriXanh", "Tuần 2", "Đã nghiệm thu"],
        ["Phụ lục C", "Cơ sở dữ liệu NoSQL MongoDB: Lược đồ Collections và kịch bản nạp dữ liệu", "Tuần 3", "Đã nghiệm thu"],
        ["Phụ lục D", "Kịch bản AI Vision và Tập kết quả thực nghiệm phân loại chất lượng nông sản", "Tuần 4", "Đã nghiệm thu"],
        ["Phụ lục E", "Bộ sơ đồ thiết kế hệ thống theo chuẩn UML và Kiến trúc 3 tầng", "Tuần 5", "Đang rà soát với GVHD"],
        ["Phụ lục F", "Bảng đặc tả cấu trúc dữ liệu các Collections cốt lõi", "Tuần 5", "Đang rà soát với GVHD"],
        ["Phụ lục G", "Ghi chú tổng hợp Tiêu chuẩn và Quy chuẩn phân loại nông sản tươi (VietGAP/TCVN)", "Tuần 5", "Đang rà soát với GVHD"]
    ]
    add_table_styled(doc, app_headers, app_rows, [Inches(1.0), Inches(3.6), Inches(1.2), Inches(1.4)])
    
    # PHỤ LỤC A
    add_heading_2(doc, "Phụ lục A. Ghi chú khảo sát hiện trạng chuỗi cung ứng TMĐT nông sản tại Việt Nam")
    add_body_p(doc, "1. Bối cảnh thị trường:")
    add_bullet_p(doc, "Việt Nam là quốc gia nông nghiệp nhiệt đới với sản lượng rau củ quả dồi dào, phong phú quanh năm tại các vùng chuyên canh lớn như Lâm Đồng (rau củ ôn đới), Đồng bằng Sông Cửu Long (trái cây nhiệt đới), Đồng bằng Sông Hồng và Tây Bắc (rau vụ đông, thảo mộc).")
    add_bullet_p(doc, "Tuy nhiên, khâu phân phối truyền thống bộc lộ nhiều điểm nghẽn nghiêm trọng: nông sản phải trung chuyển qua 3 – 5 tầng nấc trung gian (thương lái gom tại vườn, chợ đầu mối nông sản, tiểu thương chợ truyền thống, chuỗi bán lẻ). Quá trình vận chuyển kéo dài khiến tỷ lệ dập nát, hư hỏng sau thu hoạch lên tới 25% – 35%, làm giảm sút giá trị thương mại và lãng phí tài nguyên xã hội.")
    add_bullet_p(doc, "Giai đoạn 2024 – 2026 chứng kiến sự chuyển dịch số mạnh mẽ trong nông nghiệp theo Nghị quyết của Chính phủ về phát triển kinh tế số nông nghiệp, thúc đẩy nông dân và hợp tác xã đưa nông sản lên các nền tảng số.")
    
    add_body_p(doc, "2. Hiện trạng và những bất cập lớn trong TMĐT nông sản hiện nay:")
    
    survey_headers = ["Khía cạnh khảo sát", "Hiện trạng ghi nhận thực tế", "Hệ quả đối với chuỗi giá trị"]
    survey_rows = [
        [
            "Minh bạch thông tin chất lượng",
            "Người bán tự chụp ảnh tĩnh đăng tải; nhiều cơ sở lấy ảnh mạng lung linh không đúng với lô hàng thật.",
            "Người tiêu dùng bị mất niềm tin, không dám đặt hàng tươi sống online vì sợ nhận phải rau củ dập héo."
        ],
        [
            "Tiêu chuẩn phân hạng",
            "Phân hạng chủ yếu bằng mắt thường thủ công, cảm tính của tiểu thương; không có tiêu chí định lượng khách quan.",
            "Giá bán bị cào bằng; nông sản chất lượng cao (loại 1, xuất sắc) không bán được giá xứng đáng, làm nản lòng nhà vườn canh tác an toàn."
        ],
        [
            "Tính tươi mới và thời hạn sử dụng",
            "Các sàn TMĐT tổng hợp (Shopee, Lazada) không có cơ chế quản lý vòng đời và hạn sử dụng ngắn của hàng tươi.",
            "Hàng tồn cận date không được cảnh báo kịp thời, dẫn đến hư hỏng và phát sinh chi phí tiêu hủy lớn."
        ],
        [
            "Lòng tin của người mua hàng",
            "Khách hàng chỉ có thể đánh giá sản phẩm sau khi đã nhận và thanh toán mở gói hàng.",
            "Tỷ lệ hoàn trả hàng (Return rate) cao, tranh chấp khiếu nại giữa người mua và nhà vườn diễn ra thường xuyên."
        ],
        [
            "Động lực tái mua hàng",
            "Thiếu các chính sách khách hàng thân thiết gắn liền với tiêu dùng xanh và tích lũy giá trị bền vững.",
            "Khách hàng dễ chuyển sang kênh bán hàng khác nếu không có cơ chế tích điểm loyalty ưu đãi rõ ràng."
        ]
    ]
    add_table_styled(doc, survey_headers, survey_rows, [Inches(1.8), Inches(2.7), Inches(2.5)])
    
    add_body_p(doc, "3. Kết luận từ khảo sát và Hướng đi của đề tài AgriXanh:")
    add_body_p(doc, "Từ kết quả khảo sát trên, đề tài xác định mục tiêu xây dựng một nền tảng Thương mại điện tử nông sản chuyên biệt mang tên AgriXanh, tích hợp Trí tuệ nhân tạo (AI Vision) làm 'Trọng tài thẩm định chất lượng độc lập'. Hệ thống đem lại 4 giá trị đột phá:")
    add_bullet_p(doc, " Tự động nhận diện ảnh chụp thực tế của sản phẩm, đánh giá đa chiều (độ chín sinh lý, màu sắc đồng đều, hình thái, vết trầy xước/dập nát, cuống tươi) và cấp tem chứng nhận AI Quality Badge.")
    add_bullet_p(doc, " Công cụ kiểm định độc lập cho Khách hàng: Người mua có thể tự chụp ảnh gói hàng nhận được hoặc ảnh nông sản bất kỳ để AI phân tích lại, đối chiếu minh bạch với cam kết của người bán.")
    add_bullet_p(doc, " Tối ưu hóa chuỗi cung ứng ngắn (Short Food Supply Chain - SFSC): Kết nối trực tiếp Nhà vườn / Hợp tác xã tới tận tay người tiêu dùng, cắt giảm chi phí trung gian.")
    add_bullet_p(doc, " Hệ thống Khách hàng thân thiết (Loyalty Program): Tích lũy điểm tiêu dùng xanh, khuyến khích người dân ăn sạch sống lành mạnh.")
    
    # PHỤ LỤC B
    add_heading_2(doc, "Phụ lục B. Kho mã nguồn và môi trường phát triển hệ thống")
    add_body_p(doc, "1. Cấu hình môi trường phát triển Fullstack:")
    
    env_headers = ["Thành phần", "Phiên bản / Công nghệ", "Vai trò trong hệ thống AgriXanh"]
    env_rows = [
        ["Hệ điều hành", "Windows 11 Pro 64-bit", "Môi trường máy trạm phát triển và kiểm thử"],
        ["Ngôn ngữ Backend", "Python 3.12 LTS", "Xử lý logic nghiệp vụ, tính toán dữ liệu, gọi mô hình AI"],
        ["Backend Framework", "FastAPI 0.110+ (Asynchronous ASGI)", "Cung cấp hệ thống RESTful API tốc độ cao, tài liệu Swagger UI tự động"],
        ["ASGI Web Server", "Uvicorn 0.28+", "Máy chủ web bất đồng bộ chạy ứng dụng FastAPI"],
        ["Cơ sở dữ liệu", "MongoDB Community Server 7.0+", "Hệ quản trị CSDL NoSQL lưu trữ phi cấu trúc linh hoạt"],
        ["MongoDB Driver", "Motor 3.3+ (Async Motor Client)", "Kết nối bất đồng bộ Non-blocking giữa FastAPI và MongoDB"],
        ["Mô hình Trí tuệ nhân tạo", "Google Gemini 1.5 Flash Vision API", "Phân tích thị giác máy tính và thẩm định chất lượng nông sản"],
        ["Ngôn ngữ Frontend", "JavaScript ES6+ / JSX", "Xây dựng giao diện ứng dụng web Single Page Application"],
        ["Frontend Framework", "React 18.2 + Vite 5.0", "Thư viện UI hiệu năng cao, cơ chế hot-reload cực nhanh"],
        ["CSS Framework", "Tailwind CSS 3.4", "Thiết kế giao diện hiện đại, responsive, tông màu xanh nông sản sinh động"],
        ["Bảo mật & Xác thực", "PyJWT 2.8+ / Passlib (Bcrypt)", "Mã hóa băm mật khẩu và cơ chế xác thực Token phiên làm việc"],
        ["Công cụ hỗ trợ", "VS Code, Postman, Git, MongoDB Compass", "Soạn thảo mã nguồn, kiểm thử API, quản lý phiên bản và trực quan hóa DB"]
    ]
    add_table_styled(doc, env_headers, env_rows, [Inches(1.8), Inches(2.2), Inches(3.0)])
    
    add_body_p(doc, "2. Cấu trúc cây thư mục kho mã nguồn dự án AgriXanh:")
    tree_code = """
AgriXanh/
├── backend/                         # Phân hệ Backend API (FastAPI)
│   ├── app/
│   │   ├── api/                     # Các Routers API theo nghiệp vụ
│   │   │   ├── ai_vision.py         # Module AI Vision thẩm định chất lượng nông sản
│   │   │   ├── auth.py              # Xác thực người dùng, JWT & phân quyền RBAC
│   │   │   ├── products.py          # Quản lý danh mục & thông tin nông sản
│   │   │   ├── orders.py            # Xử lý giỏ hàng, đặt hàng & trừ kho
│   │   │   ├── inventory.py         # Quản lý kho hàng & cảnh báo tồn kho
│   │   │   ├── loyalty.py           # Chương trình tích điểm & đổi voucher
│   │   │   └── statistics.py        # Thống kê doanh thu & báo cáo phân tích
│   │   ├── core/                    # Cấu hình trung tâm, CSDL & bảo mật
│   │   │   ├── config.py            # Biến môi trường (.env), JWT Secret, Gemini Key
│   │   │   ├── database.py          # Kết nối Motor MongoDB & nạp Seed data
│   │   │   └── security.py          # Thuật toán Bcrypt & sinh JWT token
│   │   ├── models/                  # Định nghĩa Pydantic Schemas
│   │   │   ├── schemas.py           # Cấu trúc dữ liệu User, Product, Order, AIQuality
│   │   │   └── loyalty.py           # Cấu trúc điểm thưởng, giao dịch loyalty
│   │   └── utils/                   # Các hàm tiện ích & dữ liệu mẫu
│   │       ├── helpers.py           # Hàm chuẩn hóa chuỗi, tính toán phụ trợ
│   │       └── mock_data.py         # Bộ dữ liệu mẫu 24+ nông sản VietGAP & đơn hàng
│   ├── main.py                      # Điểm khởi động ứng dụng FastAPI (ASGI Entrypoint)
│   ├── requirements.txt             # Danh sách gói phụ thuộc Python
│   └── run_backend.bat              # Script khởi động nhanh server cổng 8000
│
├── frontend/                        # Phân hệ Giao diện Người dùng (React 18 + Vite)
│   ├── src/
│   │   ├── components/              # Các thành phần UI dùng chung (Header, Footer, Card...)
│   │   ├── layouts/                 # Khung giao diện (UserLayout, SellerLayout, AdminLayout)
│   │   ├── pages/                   # Các màn hình chức năng chính
│   │   │   ├── Home.jsx             # Trang chủ sàn TMĐT AgriXanh
│   │   │   ├── Products.jsx         # Trang danh mục nông sản, lọc theo chứng nhận
│   │   │   ├── ProductDetail.jsx    # Chi tiết nông sản kèm tem kiểm định AI
│   │   │   ├── AICheck.jsx          # Công cụ kiểm định chất lượng AI độc lập
│   │   │   ├── Cart.jsx             # Giỏ hàng & thanh toán tích hợp voucher
│   │   │   ├── AccountPage.jsx      # Hồ sơ cá nhân & ví điểm Loyalty
│   │   │   ├── seller/              # Kênh dành riêng cho Nhà vườn (Seller Center)
│   │   │   │   ├── SellerDashboard.jsx    # Thống kê bán hàng nhà vườn
│   │   │   │   ├── SellerProducts.jsx     # Quản lý danh mục hàng đăng bán
│   │   │   │   ├── SellerAIEvaluate.jsx   # Thẩm định AI trước khi đăng sản phẩm
│   │   │   │   ├── SellerOrders.jsx       # Xử lý & xác nhận giao hàng
│   │   │   │   └── SellerInventory.jsx    # Theo dõi kho hàng & hạn sử dụng
│   │   │   └── admin/               # Kênh Quản trị sàn (Admin Portal)
│   │   │       ├── AdminDashboard.jsx     # Doanh thu toàn sàn & biểu đồ tăng trưởng
│   │   │       ├── AdminProducts.jsx      # Duyệt sản phẩm & kiểm tra chất lượng
│   │   │       ├── AdminOrders.jsx        # Giám sát giao dịch toàn hệ thống
│   │   │       ├── AdminUsers.jsx         # Quản trị tài khoản & cấp quyền
│   │   │       └── AdminAILogs.jsx        # Lịch sử thẩm định AI toàn sàn
│   │   ├── services/api.js          # Cấu hình gọi Axios kết nối Backend API
│   │   ├── store/authStore.js       # Quản lý trạng thái đăng nhập và giỏ hàng
│   │   ├── App.jsx                  # Cấu hình định tuyến Router DOM
│   │   └── main.jsx                 # Điểm gắn kết React DOM
│   ├── package.json                 # Cấu hình thư viện frontend
│   └── run_frontend.bat             # Script khởi động Vite server cổng 5173
└── README.md                        # Hướng dẫn cài đặt và vận hành hệ thống
"""
    add_code_block(doc, tree_code, "Cấu trúc kho thư mục hoàn chỉnh của dự án AgriXanh")
    
    add_body_p(doc, "3. Lệnh khởi tạo và chạy thử nghiệm hệ thống:")
    cmd_code = """
# 1. Khởi chạy Backend FastAPI (Terminal 1):
cd backend
py -3.12 -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
py -3.12 -m uvicorn main:app --reload --port 8000
# Kiểm tra tài liệu API: http://127.0.0.1:8000/docs

# 2. Khởi chạy Frontend React Vite (Terminal 2):
cd frontend
npm install
npm run dev
# Truy cập ứng dụng web: http://localhost:5173
"""
    add_code_block(doc, cmd_code, "Lệnh cài đặt và khởi động hệ thống Fullstack")
    
    add_callout(doc, "Khi khởi động Backend, hệ thống tự động kiểm tra kết nối tới MongoDB. Nếu máy chủ cơ sở dữ liệu chưa sẵn sàng hoặc môi trường demo không có kết nối internet, Backend tự động kích hoạt cơ chế Seed dữ liệu mẫu từ mock_data.py và sử dụng Fallback AI Engine, đảm bảo hệ sinh thái demo hoạt động trơn tru 100% không bị ngắt quãng.", "Tiêu chí nghiệm thu môi trường")
    
    # PHỤ LỤC C
    add_heading_2(doc, "Phụ lục C. Cơ sở dữ liệu NoSQL MongoDB và Lược đồ Schema")
    add_body_p(doc, "1. Danh mục các Collections trong hệ thống CSDL AgriXanh:")
    
    db_headers = ["Tên Collection", "Khóa chính", "Mục đích lưu trữ", "Chỉ mục tối ưu hóa (Indexes)"]
    db_rows = [
        ["users", "_id (ObjectId/str)", "Tài khoản khách hàng, nhà vườn và ban quản trị", "email (unique), role, is_active"],
        ["products", "_id (ObjectId/str)", "Thông tin chi tiết nông sản, nguồn gốc, giá và tem AI", "name (text), category, price, seller_id, ai_quality"],
        ["categories", "_id (ObjectId/str)", "Danh mục phân loại nông sản (Rau lá, Củ quả, Trái cây, Nấm)", "name (unique), slug"],
        ["orders", "_id (ObjectId/str)", "Đơn hàng, địa chỉ giao hàng, chiết khấu voucher, trạng thái", "customer_id, seller_id, order_status, created_at"],
        ["inventory", "_id (ObjectId/str)", "Tồn kho thực tế, ngưỡng cảnh báo, hạn sử dụng nông sản", "product_id (unique), expiry_date, current_stock"],
        ["ai_logs", "_id (ObjectId/str)", "Nhật ký lưu trữ toàn bộ các phiên thẩm định AI trên sàn", "product_name, quality_grade, analyzed_at"],
        ["loyalty_points", "_id (ObjectId/str)", "Số dư điểm thưởng, lịch sử tích và tiêu điểm của khách hàng", "user_id (unique), current_tier, total_earned"]
    ]
    add_table_styled(doc, db_headers, db_rows, [Inches(1.3), Inches(1.3), Inches(2.6), Inches(1.8)])
    
    add_body_p(doc, "2. Ví dụ cấu trúc Document Nông sản (`products`) lưu trữ trong MongoDB:")
    json_prod = """
{
  "_id": "prod_dalat_tomato_001",
  "name": "Cà chua cherry đỏ Đà Lạt (VietGAP)",
  "category": "Rau ăn quả",
  "origin": "Trang trại Hữu cơ Xuân Thọ, TP. Đà Lạt, Lâm Đồng",
  "price": 45000,
  "unit": "kg",
  "stock_quantity": 180,
  "ai_quality": "Loại 1 (Xuất sắc)",
  "ai_freshness_score": 96,
  "rating": 4.9,
  "sold_count": 524,
  "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcadf655?w=500",
  "seller_id": "seller_dalat_farm_01",
  "description": "Cà chua cherry giống socola & ruby đỏ mọng, độ giòn ngọt thanh, canh tác an toàn.",
  "created_at": "2026-09-20T08:30:00Z"
}
"""
    add_code_block(doc, json_prod, "JSON Document biểu diễn thực thể Sản phẩm nông sản có tem AI")
    
    # PHỤ LỤC D
    add_heading_2(doc, "Phụ lục D. Kịch bản AI Vision và Tập kết quả thực nghiệm phân loại")
    add_body_p(doc, "1. Phương pháp luận và Kiến trúc tích hợp mô hình AI Vision:")
    add_body_p(doc, "Thay vì phụ thuộc vào các mạng nơ-ron tích chập truyền thống (CNN đơn thuần) vốn đòi hỏi tập dữ liệu hàng chục nghìn ảnh phải gán nhãn thủ công tốn kém và thiếu khả năng hiểu ngữ cảnh nông nghiệp, AgriXanh ứng dụng mô hình Trí tuệ nhân tạo Đa phương thức tiên tiến Google Gemini 1.5 Flash Vision. Mô hình tiếp nhận trực tiếp luồng nhị phân (binary bytes) của ảnh nông sản kết hợp với kỹ thuật Prompt Chuyên gia định dạng JSON (JSON schema guided prompting).")
    
    add_body_p(doc, "2. Đoạn mã Python xử lý thẩm định AI cốt lõi (`backend/app/api/ai_vision.py`):")
    ai_py_code = """
# Kịch bản tích hợp Google Gemini 1.5 Flash Vision phân loại chất lượng nông sản
async def _gemini_analysis(image_bytes: bytes, product_name: str) -> dict:
    import google.generativeai as genai
    import PIL.Image, io, json, uuid
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f\"\"\"
    Bạn là chuyên gia thẩm định chất lượng nông sản tươi sống theo chuẩn VietGAP.
    Hãy phân tích hình ảnh của nông sản '{product_name}' và trả về DUY NHẤT một JSON hợp lệ:
    {{
      "quality_grade": "Loại 1 (Xuất sắc)" | "Loại 2 (Đạt chuẩn)" | "Loại 3 (Chế biến)" | "Không đạt",
      "confidence": số thực từ 0.80 đến 0.99,
      "freshness_score": số nguyên từ 0 đến 100,
      "color_assessment": "đánh giá màu sắc vỏ, độ chín sinh lý đồng đều",
      "shape_assessment": "đánh giá hình thái, kích thước đồng nhất, dị tật",
      "surface_condition": "tình trạng vỏ căng mọng, cuống đài, nấm mốc hoặc vết dập",
      "details": "kết luận tổng quan giá trị thương phẩm",
      "recommendations": ["khuyến nghị bảo quản", "khuyến nghị đóng gói / hạn dùng"]
    }}
    \"\"\"
    image = PIL.Image.open(io.BytesIO(image_bytes))
    response = model.generate_content([prompt, image])
    text = response.text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    result = json.loads(text)
    result["id"] = f"ailog_{uuid.uuid4().hex[:8]}"
    result["product_name"] = product_name
    result["analyzed_at"] = datetime.utcnow().isoformat()
    result["model_used"] = "Google Gemini 1.5 Flash Vision"
    _ai_logs_store.insert(0, result)
    return result
"""
    add_code_block(doc, ai_py_code, "Hàm gọi Gemini 1.5 Flash Vision thẩm định đa tiêu chí")
    
    add_body_p(doc, "3. Bảng kết quả thực nghiệm phân loại trên các mẫu nông sản đại diện:")
    
    test_headers = ["Nông sản thử nghiệm", "Phân hạng chất lượng", "Độ tươi (Score)", "Độ tin cậy", "Đặc trưng nhận diện qua AI"]
    test_rows = [
        ["Cà chua cherry Đà Lạt", "Loại 1 (Xuất sắc)", "96 / 100", "97.4%", "Đỏ mọng 98%, bóng loáng tự nhiên; cuống đài xanh tươi bám chắc; không vết dập nám."],
        ["Dưa leo baby Hữu cơ", "Loại 1 (Xuất sắc)", "93 / 100", "94.8%", "Thân thẳng đều, thon dài chuẩn; còn nguyên lớp phấn trắng tự nhiên và gai nhuyễn."],
        ["Ớt chuông đỏ Đà Lạt", "Loại 2 (Đạt chuẩn)", "88 / 100", "91.2%", "Vỏ bóng 85% diện tích; cùi thịt dày cân đối; có một vết cọ xát nhỏ nhẹ do cành lá."],
        ["Cà rốt tươi Mộc Châu", "Loại 1 (Xuất sắc)", "95 / 100", "96.1%", "Màu cam sáng rực rỡ; củ suôn thẳng, không phân nhánh dị tật; phần đầu cuống còn tươi non."],
        ["Rau xà lách thủy canh", "Đạt chuẩn VietGAP", "92 / 100", "93.5%", "Lá xanh mướt giòn xốp; rễ sạch không bùn đất; tỷ lệ tế bào mọng nước tối ưu."]
    ]
    add_table_styled(doc, test_headers, test_rows, [Inches(1.6), Inches(1.4), Inches(1.0), Inches(0.9), Inches(2.1)])
    
    # PHỤ LỤC E
    add_heading_2(doc, "Phụ lục E. Bộ sơ đồ UML và Kiến trúc hệ thống")
    add_body_p(doc, "Hệ thống AgriXanh được mô hình hóa toàn diện bằng ngôn ngữ mô hình hóa thống nhất (UML), bao gồm các góc nhìn chức năng, hành vi và cấu trúc dữ liệu:")
    
    add_heading_3(doc, "1. Sơ đồ Use Case tổng thể hệ thống AgriXanh")
    add_body_p(doc, "Hệ thống phục vụ 3 nhóm tác nhân chính (Actors):")
    add_bullet_p(doc, "Xem danh mục nông sản, tra cứu theo tiêu chuẩn VietGAP/OCOP, sử dụng công cụ AI Check để kiểm định ảnh nông sản độc lập, quản lý giỏ hàng, đặt hàng thanh toán, tích lũy và đổi điểm thưởng Loyalty, theo dõi tiến độ đơn hàng.", "Khách hàng (Customer):")
    add_bullet_p(doc, "Đăng ký thông tin gian hàng/trang trại, kiểm định chất lượng nông sản qua AI Vision trước khi niêm yết, quản lý danh sách sản phẩm, quản lý kho hàng và theo dõi cảnh báo hạn sử dụng, xác nhận và xử lý đóng gói giao hàng.", "Người bán / Nhà vườn (Seller):")
    add_bullet_p(doc, "Duyệt hồ sơ gian hàng nông sản, quản trị tài khoản người dùng và phân quyền RBAC, giám sát toàn diện nhật ký kiểm định AI toàn sàn (AI Logs), quản lý danh mục và xem báo cáo tài chính - doanh thu.", "Quản trị viên (Admin):")
    
    add_heading_3(doc, "2. Sơ đồ Activity: Quy trình Thẩm định AI và Đăng bán sản phẩm")
    add_body_p(doc, "Luồng hoạt động thể hiện sự phối hợp chặt chẽ giữa Nhà vườn, Hệ thống Backend và Mô hình AI:")
    add_bullet_p(doc, "Bước 1: Nhà vườn đăng nhập Kênh Người bán (Seller Center), chọn chức năng 'Thẩm định AI & Đăng sản phẩm'.")
    add_bullet_p(doc, "Bước 2: Tải lên hình ảnh nông sản thực tế vừa thu hoạch kèm tên mặt hàng.")
    add_bullet_p(doc, "Bước 3: Hệ thống Backend FastAPI nhận file ảnh, kiểm tra tính hợp lệ và chuyển tiếp lên Google Gemini 1.5 Flash Vision.")
    add_bullet_p(doc, "Bước 4: Mô hình AI xử lý phân tích hình ảnh, chấm điểm Freshness Score và xác định phân hạng chất lượng (Loại 1, Loại 2, Loại 3 hoặc Không đạt).")
    add_bullet_p(doc, "Bước 5: Hệ thống trả kết quả trực quan trên giao diện: Nếu đạt tiêu chuẩn (Loại 1 hoặc Loại 2), hệ thống cấp tem 'AI Verified Quality' và cho phép điền giá bán, số lượng tồn kho để niêm yết lên sàn; nếu 'Không đạt', hệ thống hiển thị khuyến nghị từ chối và hướng dẫn cải thiện bảo quản.")
    
    add_heading_3(doc, "3. Sơ đồ Sequence: Quy trình Khách hàng kiểm định AI và Đặt hàng")
    add_body_p(doc, "Mô tả chuỗi tương tác tuần tự theo thời gian giữa Khách hàng -> Giao diện React SPA -> Backend FastAPI -> Module AI Vision -> MongoDB Server:")
    add_bullet_p(doc, "Khách hàng gửi yêu cầu phân tích ảnh mẫu qua POST /api/v1/ai/analyze -> FastAPI xử lý -> Gemini trả JSON -> UI hiển thị thẻ chất lượng -> Khách hàng bấm Thêm vào giỏ hàng -> Gọi POST /api/v1/orders tạo đơn -> Hệ thống thực hiện kiểm tra tồn kho (Atomic check stock) -> Khấu trừ điểm tích lũy voucher nếu có -> Xác nhận đơn thành công.")
    
    add_heading_3(doc, "4. Sơ đồ Class Diagram các thực thể cốt lõi")
    add_body_p(doc, "Bao gồm các lớp chính: User (Customer, Seller, Admin), Product (kèm thuộc tính AIQuality, freshnessScore), Order (chứa danh sách CartItem, trạng thái giao dịch), Inventory (chứa minStock, expiryDate), LoyaltyWallet (chứa points, tier), và AILog (lưu trữ kết quả kiểm định chi tiết).")
    
    add_heading_3(doc, "5. Kiến trúc hệ thống ba tầng (Three-Tier Architecture)")
    add_bullet_p(doc, "Xây dựng bằng React 18, Vite, Tailwind CSS, Lucide Icons và Recharts; đảm bảo trải nghiệm người dùng mượt mà, tải nhanh và tương thích hoàn hảo từ màn hình điện thoại di động đến máy tính để bàn.", "Tầng Giao diện (Presentation Layer):")
    add_bullet_p(doc, "FastAPI Framework xử lý toàn bộ logic nghiệp vụ, bảo mật JWT/RBAC, tích hợp kết nối Google Gemini 1.5 Flash Vision, xử lý giỏ hàng, tính điểm Loyalty và cung cấp tài liệu tự động Swagger UI.", "Tầng Nghiệp vụ (Business Application Layer):")
    add_bullet_p(doc, "Hệ quản trị CSDL NoSQL MongoDB lưu trữ các Collections phi cấu trúc linh hoạt; kết nối qua thư viện Motor AsyncIOMotorClient đảm bảo hiệu năng đọc ghi cao và tính sẵn sàng dữ liệu.", "Tầng Dữ liệu (Data Storage Layer):")
    
    # PHỤ LỤC F
    add_heading_2(doc, "Phụ lục F. Bảng đặc tả cấu trúc dữ liệu các Collections cốt lõi")
    add_body_p(doc, "Đặc tả chi tiết cấu trúc thuộc tính của 3 Collections trung tâm:")
    
    add_heading_3(doc, "1. Collection `products` (Thông tin nông sản & Tem chất lượng AI)")
    col_p_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Diễn giải ý nghĩa nghiệp vụ"]
    col_p_rows = [
        ["_id", "String / ObjectId", "Primary Key", "Mã định danh duy nhất của sản phẩm nông sản"],
        ["name", "String (255)", "Required", "Tên thương phẩm của nông sản (ví dụ: Cà chua cherry Đà Lạt)"],
        ["category", "String (100)", "Required", "Danh mục nông sản (Rau ăn quả, Rau ăn lá, Củ, Nấm)"],
        ["origin", "String (255)", "Optional", "Khu vực xuất xứ, tên trang trại / hợp tác xã sản xuất"],
        ["price", "Float / Double", "Min: 0", "Đơn giá bán lẻ niêm yết (VNĐ)"],
        ["unit", "String (20)", "Default: 'kg'", "Đơn vị đo lường tính giá (kg, gram, hộp, bó)"],
        ["stock_quantity", "Integer", "Min: 0", "Số lượng tồn kho thực tế hiện tại"],
        ["ai_quality", "String (50)", "Indexed", "Hạng chất lượng do AI thẩm định (Loại 1, Loại 2, VietGAP)"],
        ["ai_freshness_score", "Integer", "0 - 100", "Điểm số tươi mới do AI chấm (Freshness Score)"],
        ["image_url", "String (500)", "Required", "Đường dẫn URL hình ảnh chất lượng cao của nông sản"],
        ["seller_id", "String / ObjectId", "Foreign Key", "Mã định danh nhà vườn sở hữu sản phẩm"],
        ["created_at", "DateTime", "Auto now", "Thời điểm nông sản được thẩm định và đăng bán"]
    ]
    add_table_styled(doc, col_p_headers, col_p_rows, [Inches(1.5), Inches(1.3), Inches(1.1), Inches(3.1)])
    
    add_heading_3(doc, "2. Collection `orders` (Giao dịch đặt hàng & Thanh toán)")
    col_o_headers = ["Tên trường", "Kiểu dữ liệu", "Ràng buộc", "Diễn giải ý nghĩa nghiệp vụ"]
    col_o_rows = [
        ["_id", "String / ObjectId", "Primary Key", "Mã định danh duy nhất của đơn hàng"],
        ["customer_id", "String / ObjectId", "Foreign Key", "Mã khách hàng thực hiện đặt đơn"],
        ["seller_id", "String / ObjectId", "Foreign Key", "Mã nhà vườn tiếp nhận và đóng gói đơn"],
        ["items", "Array of Objects", "Not empty", "Danh sách các mặt hàng (product_id, số lượng, đơn giá)"],
        ["subtotal", "Float / Double", "Min: 0", "Tổng tiền hàng trước khi áp dụng chiết khấu"],
        ["discount_amount", "Float / Double", "Default: 0", "Số tiền được giảm trừ từ điểm thưởng Loyalty / Voucher"],
        ["shipping_fee", "Float / Double", "Default: 0", "Phí vận chuyển giao hàng tận nơi"],
        ["total_amount", "Float / Double", "Required", "Tổng số tiền thực tế khách hàng phải thanh toán"],
        ["order_status", "String (30)", "Enum", "Trạng thái đơn: pending, confirmed, shipping, delivered, cancelled"],
        ["payment_method", "String (20)", "Enum", "Phương thức thanh toán: COD (tiền mặt), VNPay, MoMo"],
        ["created_at", "DateTime", "Auto now", "Thời điểm khách hàng gửi đơn đặt mua"]
    ]
    add_table_styled(doc, col_o_headers, col_o_rows, [Inches(1.5), Inches(1.3), Inches(1.1), Inches(3.1)])
    
    # PHỤ LỤC G
    add_heading_2(doc, "Phụ lục G. Ghi chú tổng hợp Tiêu chuẩn và Quy chuẩn phân loại nông sản")
    add_body_p(doc, "1. Cơ sở pháp lý và tiêu chuẩn kỹ thuật áp dụng trong hệ thống:")
    add_bullet_p(doc, "TCVN 11892-1:2017 – Thực hành nông nghiệp tốt (VietGAP) Phần 1: Trồng trọt.")
    add_bullet_p(doc, "Bộ tiêu chí đánh giá và phân hạng sản phẩm Chương trình Mỗi xã một sản phẩm (OCOP) theo Quyết định số 148/QĐ-TTg của Thủ tướng Chính phủ.")
    add_bullet_p(doc, "Các Tiêu chuẩn Quốc gia về yêu cầu ngoại quan rau quả tươi thương phẩm (TCVN 9016:2011 đối với cà chua, TCVN 10738:2015 đối với dưa chuột).")
    
    add_body_p(doc, "2. Bảng quy tắc phân hạng chất lượng tự động của hệ thống AI AgriXanh:")
    
    grade_headers = ["Cấp phân hạng", "Freshness Score", "Đặc trưng nhận diện ngoại quan của AI", "Màu nhãn (Badge)", "Chính sách thương mại"]
    grade_rows = [
        [
            "Loại 1 (Xuất sắc)",
            "90 – 100 điểm",
            "Màu sắc rực rỡ, độ chín đồng đều 95-100%; vỏ căng bóng nguyên vẹn; cuống tươi xanh mọng nước; hoàn toàn không có khuyết tật.",
            "Xanh lá đậm (Emerald Green)",
            "Định giá bán lẻ cao cấp; ưu tiên hiển thị đầu sàn; thích hợp làm quà biếu hoặc xuất khẩu."
        ],
        [
            "Loại 2 (Đạt chuẩn)",
            "80 – 89 điểm",
            "Độ chín 80-90%; kích thước tương đối cân đối; vỏ có thể có vết cọ xát vi mô nhẹ do cành lá nhưng không làm rách vỏ hoặc ảnh hưởng thịt quả.",
            "Xanh dương (Blue Teal)",
            "Định giá bán lẻ tiêu chuẩn cho bữa ăn gia đình hàng ngày; phân phối chuỗi siêu thị sạch."
        ],
        [
            "Loại 3 (Chế biến)",
            "65 – 79 điểm",
            "Nông sản đã chín già, vỏ hơi mềm hoặc kích thước không đồng đều; không bị thối nhũn sâu bệnh.",
            "Vàng cam (Amber)",
            "Đề xuất xả hàng Flash Sale; chuyển đổi mục đích sử dụng làm nước ép, mứt, nấu súp hoặc sốt."
        ],
        [
            "Không đạt chuẩn",
            "< 65 điểm",
            "Nông sản dập nát, héo úa, phát hiện vết côn trùng đục khoét, nấm mốc hoặc thối rữa.",
            "Đỏ cảnh báo (Crimson Red)",
            "Hệ thống tự động từ chối cấp phép niêm yết trên sàn để bảo vệ quyền lợi người tiêu dùng."
        ]
    ]
    add_table_styled(doc, grade_headers, grade_rows, [Inches(1.4), Inches(1.1), Inches(2.2), Inches(1.1), Inches(1.2)])
    
    # ------------------ PHẦN KÝ TÊN ------------------
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    p_sign_date = doc.add_paragraph()
    format_paragraph(p_sign_date, space_before=12, space_after=4, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r_sd = p_sign_date.add_run("TP. Hồ Chí Minh, ngày 27 tháng 09 năm 2026\n")
    r_sd.font.name = "Times New Roman"
    r_sd.font.size = Pt(11)
    r_sd.font.italic = True
    
    tbl_sign = doc.add_table(rows=1, cols=2)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_gv = tbl_sign.cell(0, 0)
    cell_sv = tbl_sign.cell(0, 1)
    
    p_gv = cell_gv.paragraphs[0]
    format_paragraph(p_gv, space_before=0, space_after=40, align=WD_ALIGN_PARAGRAPH.CENTER)
    r1 = p_gv.add_run("GIẢNG VIÊN HƯỚNG DẪN\n(Ký và ghi rõ họ tên)\n\n\n\n\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r2 = p_gv.add_run("ThS. Ngô Tân Khai")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11.5)
    r2.font.bold = True
    
    p_sv = cell_sv.paragraphs[0]
    format_paragraph(p_sv, space_before=0, space_after=40, align=WD_ALIGN_PARAGRAPH.CENTER)
    r3 = p_sv.add_run("SINH VIÊN THỰC HIỆN\n(Ký và ghi rõ họ tên)\n\n\n\n\n")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(11)
    r3.font.bold = True
    r4 = p_sv.add_run("Nguyễn Văn An")
    r4.font.name = "Times New Roman"
    r4.font.size = Pt(11.5)
    r4.font.bold = True

    doc.save(output_path)
    print("Tao thanh cong Bao cao tien do: " + output_path)

if __name__ == "__main__":
    output_file = os.path.join(os.path.dirname(__file__), "Bao_Cao_Tien_Do_Do_An_Chuyen_Nganh_AgriXanh.docx")
    build_progress_report(output_file)
