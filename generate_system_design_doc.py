# -*- coding: utf-8 -*-
"""
Script tạo tài liệu thiết kế hệ thống và cập nhật báo cáo đồ án AgriXanh
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from use_cases_data import AGRIXANH_USE_CASES
from build_full_diagrams_doc import (
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, DIAGRAMS_DIR,
    set_cell_background, set_cell_margins, set_table_borders,
    add_heading_1, add_heading_2, add_heading_3, add_body_p,
    add_image_with_caption, add_uc_spec_table, format_paragraph
)

def build_diagrams_doc(output_path):
    doc = docx.Document()
    
    # Page setup
    section = doc.sections[0]
    section.top_margin = Inches(0.79)
    section.bottom_margin = Inches(0.79)
    section.left_margin = Inches(1.18)
    section.right_margin = Inches(0.79)

    # Title
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=10, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_title.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO - TRƯỜNG ĐH TÀI NGUYÊN VÀ MÔI TRƯỜNG TP.HCM\nKHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN KỸ THUẬT PHẦN MỀM\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_doc_type = doc.add_paragraph()
    format_paragraph(p_doc_type, space_before=6, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_dt = p_doc_type.add_run("TÀI LIỆU PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG THEO CHUẨN UML")
    r_dt.font.name = "Times New Roman"
    r_dt.font.size = Pt(16)
    r_dt.font.bold = True
    r_dt.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=2, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_sub = p_sub.add_run("Đề tài: XÂY DỰNG HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ NÔNG SẢN TÍCH HỢP AI PHÂN LOẠI CHẤT LƯỢNG TỰ ĐỘNG (AGRIXANH)\nSinh viên thực hiện: Nguyễn Văn An – MSSV: 1250080128 – Lớp: 12_ĐH_CNTT | GVHD: ThS. Ngô Tân Khai")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True

    # 1. DANH MỤC TỔNG HỢP USE CASE
    add_heading_1(doc, "DANH MỤC TỔNG HỢP USE CASE HỆ THỐNG")
    add_body_p(doc, "Hệ thống sàn giao dịch thương mại điện tử nông sản AgriXanh bao gồm 20 Use Case phân bổ trên 6 phân hệ cốt lõi: Quản lý người dùng & Xác thực, Phân hệ thương mại điện tử Khách hàng, Phân hệ quản lý Kênh Nhà vườn (Seller Center), Phân hệ Trí tuệ nhân tạo thẩm định ngoại quan nông sản (Google Gemini 1.5 Flash Vision), Phân hệ Khách hàng thân thiết (Loyalty Program & Tiêu dùng xanh), và Phân hệ Quản trị sàn (Admin Backoffice & Analytics):")

    # Table of 20 Use Cases
    tbl_headers = ["STT", "Mã UC", "Tên Use Case", "Actor chính", "Phân hệ chức năng"]
    tbl_rows = [
        ["1", "UC-01", "Đăng ký tài khoản", "Khách hàng, Nhà vườn", "Quản lý Người dùng & Xác thực"],
        ["2", "UC-02", "Đăng nhập hệ thống & Cấp phát JWT", "Khách hàng, Nhà vườn, Admin", "Quản lý Người dùng & Xác thực"],
        ["3", "UC-03", "Quản lý hồ sơ cá nhân & Địa chỉ nhận hàng", "Khách hàng", "Quản lý Người dùng & Xác thực"],
        ["4", "UC-04", "Tìm kiếm và lọc nông sản VietGAP", "Khách hàng", "Thương mại điện tử & Bán hàng"],
        ["5", "UC-05", "Xem chi tiết nông sản & Tem chất lượng AI", "Khách hàng", "Thương mại điện tử & Bán hàng"],
        ["6", "UC-06", "Quản lý giỏ hàng", "Khách hàng", "Thương mại điện tử & Bán hàng"],
        ["7", "UC-07", "Đặt hàng và Thanh toán", "Khách hàng", "Thương mại điện tử & Bán hàng"],
        ["8", "UC-08", "Theo dõi trạng thái và Lịch sử đơn hàng", "Khách hàng", "Thương mại điện tử & Bán hàng"],
        ["9", "UC-09", "Hủy đơn hàng và Hoàn tồn kho", "Khách hàng, Admin", "Thương mại điện tử & Bán hàng"],
        ["10", "UC-10", "Đăng ký gian hàng & Thông tin trang trại", "Nhà vườn (Seller)", "Kênh Nhà vườn (Seller Center)"],
        ["11", "UC-11", "Quản lý sản phẩm đăng bán & Bảng giá", "Nhà vườn (Seller)", "Kênh Nhà vườn (Seller Center)"],
        ["12", "UC-12", "Quản lý kho hàng & Cảnh báo date nông sản", "Nhà vườn (Seller)", "Kênh Nhà vườn (Seller Center)"],
        ["13", "UC-13", "Tiếp nhận, xác nhận đóng gói và duyệt đơn", "Nhà vườn (Seller)", "Kênh Nhà vườn (Seller Center)"],
        ["14", "UC-14", "Thẩm định chất lượng nông sản qua AI Vision", "Nhà vườn (Seller), Gemini AI", "Trí tuệ nhân tạo & AI Vision"],
        ["15", "UC-15", "Kiểm định ảnh nông sản độc lập (AI Check)", "Khách hàng, Gemini AI", "Trí tuệ nhân tạo & AI Vision"],
        ["16", "UC-16", "Giám sát nhật ký kiểm định AI toàn sàn", "Quản trị viên (Admin)", "Trí tuệ nhân tạo & AI Vision"],
        ["17", "UC-17", "Tích lũy điểm thưởng tiêu dùng xanh (Loyalty)", "Khách hàng, Order Service", "Khách hàng thân thiết (Loyalty)"],
        ["18", "UC-18", "Đổi điểm thưởng lấy Voucher giảm giá", "Khách hàng, Loyalty Service", "Khách hàng thân thiết (Loyalty)"],
        ["19", "UC-19", "Nâng hạng thành viên khách hàng", "Khách hàng, Loyalty Service", "Khách hàng thân thiết (Loyalty)"],
        ["20", "UC-20", "Báo cáo thống kê doanh thu & Giám sát sàn", "Quản trị viên (Admin)", "Quản trị viên (Admin Backoffice)"]
    ]

    tbl_uc = doc.add_table(rows=len(tbl_rows)+1, cols=len(tbl_headers))
    tbl_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_uc)
    
    # header
    for c_idx, h in enumerate(tbl_headers):
        cell = tbl_uc.rows[0].cells[c_idx]
        set_cell_background(cell, PRIMARY_COLOR)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_vals in enumerate(tbl_rows):
        row = tbl_uc.rows[r_idx+1]
        bg = "FFFFFF" if r_idx % 2 == 0 else "F9FBE7"
        for c_idx, v in enumerate(row_vals):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, space_before=0, space_after=0, align=align)
            r = p.add_run(v)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 2. SƠ ĐỒ USE CASE HỆ THỐNG
    add_heading_1(doc, "SƠ ĐỒ USE CASE HỆ THỐNG AGRIXANH")
    add_body_p(doc, "Sơ đồ Use Case tổng thể biểu diễn ranh giới hệ thống, các tác nhân (Actors) chính bao gồm Khách hàng (Customer), Nhà vườn / Người bán (Seller), Quản trị viên (Admin), và Phân hệ Trí tuệ nhân tạo (Google Gemini 1.5 Flash Vision Engine), cùng các mối quan hệ liên kết và quan hệ phụ thuộc <<include>> giữa các ca sử dụng:")
    
    add_image_with_caption(
        doc,
        filename="use_case_overall.png",
        caption_text="Hình 1. Sơ đồ Use Case tổng thể Hệ thống Thương mại điện tử Nông sản AgriXanh tích hợp AI Vision",
        width_in=6.2
    )

    # 3. NỘI DUNG ĐẶC TẢ CHI TIẾT TỪNG USE CASE
    add_heading_1(doc, "NỘI DUNG ĐẶC TẢ CHI TIẾT TỪNG USE CASE")
    add_body_p(doc, "Tất cả 20 Use Case của hệ thống được lập thành bảng đặc tả hoàn chỉnh theo đúng mẫu quy định, phân định tường minh giữa hành vi của Tác nhân (Actor) và nghiệp vụ tương ứng của Hệ thống (FastAPI Web Controller, Business Services, MongoDB Database, Google Gemini AI Vision Engine):")

    for uc in AGRIXANH_USE_CASES:
        add_uc_spec_table(
            doc,
            uc_id=uc["id"],
            uc_name=uc["name"],
            actor=uc["actor"],
            desc=uc["desc"],
            pre=uc["pre"],
            post=uc["post"],
            basic_steps=uc["basic"],
            alt_steps=uc["alt"]
        )

    # 4. SƠ ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAMS)
    doc.add_page_break()
    add_heading_1(doc, "HỆ THỐNG SƠ ĐỒ HOẠT ĐỘNG (ACTIVITY DIAGRAMS)")
    add_body_p(doc, "Các sơ đồ hoạt động dưới đây được mô hình hóa theo phong cách Swimlane 3 làn chuẩn (Làn 1: Người dùng / Tác nhân; Làn 2: Web Controller FastAPI; Làn 3: Cơ sở dữ liệu MongoDB hoặc AI Vision Engine), biểu diễn chi tiết dòng điều khiển nghiệp vụ, điểm rẽ nhánh điều kiện và luồng dữ liệu tương ứng:")

    add_heading_2(doc, "1. Sơ đồ Hoạt động: UC-01 - Đăng ký tài khoản")
    add_image_with_caption(
        doc,
        filename="activity_uc01_register.png",
        caption_text="Hình 2. Sơ đồ Hoạt động: UC-01 - Đăng ký tài khoản (Register)",
        width_in=6.0
    )

    add_heading_2(doc, "2. Sơ đồ Hoạt động: UC-02 - Đăng nhập hệ thống & Cấp phát JWT")
    add_image_with_caption(
        doc,
        filename="activity_uc02_login.png",
        caption_text="Hình 3. Sơ đồ Hoạt động: UC-02 - Đăng nhập hệ thống & Cấp phát JWT Token",
        width_in=6.0
    )

    add_heading_2(doc, "3. Sơ đồ Hoạt động: UC-07 - Đặt hàng và Thanh toán (Checkout)")
    add_image_with_caption(
        doc,
        filename="activity_uc07_checkout.png",
        caption_text="Hình 4. Sơ đồ Hoạt động: UC-07 - Đặt hàng, Khóa kiểm tra tồn kho và Thanh toán",
        width_in=6.0
    )

    add_heading_2(doc, "4. Sơ đồ Hoạt động: UC-14 - Thẩm định nông sản qua AI Vision (Nhà vườn)")
    add_image_with_caption(
        doc,
        filename="activity_uc14_ai_vision_seller.png",
        caption_text="Hình 5. Sơ đồ Hoạt động: UC-14 - Thẩm định chất lượng nông sản qua Google Gemini AI Vision và cấp tem AI Badge",
        width_in=6.0
    )

    add_heading_2(doc, "5. Sơ đồ Hoạt động: UC-15 - Khách hàng tự kiểm định AI độc lập (AI Check)")
    add_image_with_caption(
        doc,
        filename="activity_uc15_ai_check_cust.png",
        caption_text="Hình 6. Sơ đồ Hoạt động: UC-15 - Khách hàng kiểm định độ tươi ảnh nông sản độc lập qua AI Check",
        width_in=6.0
    )

    add_heading_2(doc, "6. Sơ đồ Hoạt động: UC-18 - Đổi điểm thưởng Loyalty lấy Voucher")
    add_image_with_caption(
        doc,
        filename="activity_uc18_loyalty.png",
        caption_text="Hình 7. Sơ đồ Hoạt động: UC-18 - Khách hàng đổi điểm thưởng Loyalty lấy Voucher giảm giá",
        width_in=6.0
    )

    # 5. SƠ ĐỒ TUẦN TỰ (SEQUENCE DIAGRAMS)
    doc.add_page_break()
    add_heading_1(doc, "HỆ THỐNG SƠ ĐỒ TUẦN TỰ (SEQUENCE DIAGRAMS)")
    add_body_p(doc, "Các sơ đồ tuần tự mô hình hóa tương tác theo thời gian giữa các đối tượng trong hệ thống: Tác nhân -> Giao diện Client (React View) -> FastAPI Controller -> Business Service -> Gemini Vision AI Engine -> MongoDB NoSQL Database:")

    add_heading_2(doc, "1. Sơ đồ Tuần tự: Quy trình Đặt hàng, Áp Voucher và Trừ kho tự động")
    add_image_with_caption(
        doc,
        filename="sequence_01_checkout.png",
        caption_text="Hình 8. Sơ đồ Tuần tự: Quy trình Đặt hàng, Khóa giao dịch kiểm tra tồn kho và Khấu trừ điểm Loyalty",
        width_in=6.2
    )

    add_heading_2(doc, "2. Sơ đồ Tuần tự: Nhà vườn Thẩm định nông sản qua Google Gemini 1.5 Flash")
    add_image_with_caption(
        doc,
        filename="sequence_02_ai_evaluation.png",
        caption_text="Hình 9. Sơ đồ Tuần tự: Luồng xử lý Thẩm định chất lượng nông sản đa tiêu chí qua AI Vision",
        width_in=6.2
    )

    add_heading_2(doc, "3. Sơ đồ Tuần tự: Khách hàng tự kiểm định chất lượng độc lập (AI Check)")
    add_image_with_caption(
        doc,
        filename="sequence_03_ai_check.png",
        caption_text="Hình 10. Sơ đồ Tuần tự: Công cụ AI Check thẩm định hình ảnh nông sản cho Khách hàng",
        width_in=6.2
    )

    add_heading_2(doc, "4. Sơ đồ Tuần tự: Tích điểm tiêu dùng xanh Loyalty và Đổi Voucher")
    add_image_with_caption(
        doc,
        filename="sequence_04_loyalty.png",
        caption_text="Hình 11. Sơ đồ Tuần tự: Vòng đời tích lũy điểm thưởng khi đơn hoàn thành và Đổi mã giảm giá",
        width_in=6.2
    )

    add_heading_2(doc, "5. Sơ đồ Tuần tự: Xác thực người dùng và Cấp phát Token JWT (RBAC)")
    add_image_with_caption(
        doc,
        filename="sequence_05_auth_jwt.png",
        caption_text="Hình 12. Sơ đồ Tuần tự: Quy trình Xác thực Mật khẩu Bcrypt, Sinh Token JWT và Phân quyền",
        width_in=6.2
    )

    doc.save(output_path)
    print(f"Tao thanh cong Tai lieu Thiet ke He thong: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "Tai_Lieu_So_Do_Thiet_Ke_He_Thong_AgriXanh.docx")
    build_diagrams_doc(out)
