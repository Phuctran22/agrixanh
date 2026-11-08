# -*- coding: utf-8 -*-
"""
Script cập nhật Báo cáo Đồ án Chuyên ngành AgriXanh với trọn bộ:
- Danh mục tổng hợp 20 Use Cases trên 6 phân hệ
- Toàn bộ 20 Bảng mẫu đặc tả Use Case chi tiết (Basic flow & Alternate flow)
- Chèn trực tiếp các hình vẽ Sơ đồ Use Case, Sơ đồ Hoạt động Swimlane và Sơ đồ Tuần tự
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

PRIMARY_COLOR = "1B5E20"     # Deep Green
SECONDARY_COLOR = "2E7D32"   # Medium Green
ACCENT_COLOR = "E8F5E9"      # Light Green
BORDER_COLOR = "CCCCCC"

DIAGRAMS_DIR = os.path.join(os.path.dirname(__file__), "diagrams")

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
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
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{PRIMARY_COLOR}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def format_paragraph(p, space_before=0, space_after=5, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.LEFT):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=16, space_after=8)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=12, space_after=6)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2E, 0x7D, 0x32)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=8, space_after=4)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x38, 0x8E, 0x3C)
    return p

def add_body_p(doc, text, bold_prefix="", italic_prefix=""):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=4, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(11.5)
        r_pre.font.bold = True
    if italic_prefix:
        r_it = p.add_run(italic_prefix)
        r_it.font.name = "Times New Roman"
        r_it.font.size = Pt(11.5)
        r_it.font.italic = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11.5)
    return p

def add_image_with_caption(doc, filename, caption_text, width_in=6.0):
    img_path = os.path.join(DIAGRAMS_DIR, filename)
    if not os.path.exists(img_path):
        print(f"Warning: image {img_path} not found")
        return
    p_img = doc.add_paragraph()
    format_paragraph(p_img, space_before=8, space_after=3, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_img = p_img.add_run()
    r_img.add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    format_paragraph(p_cap, space_before=0, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10.5)
    r_cap.font.bold = True
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

def add_uc_spec_table(doc, uc_id, uc_name, actor, desc, pre, post, basic_steps, alt_steps):
    """
    Tạo bảng mẫu đặc tả Use Case chuẩn theo đúng định dạng mẫu của người dùng
    """
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=6, space_after=2)
    r = p_title.add_run(f"Đặc tả {uc_id} - {uc_name}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)

    # Table layout: 3 columns (Luồng/Nhãn, Tác nhân/Giá trị, Hệ thống/Giá trị)
    # Total rows = 1 (header title) + 4 (metadata: Tên, Actor, Mô tả, Pre, Post) + 1 (header basic) + len(basic_steps) + 1 (header alt) + len(alt_steps)
    rows_count = 1 + 5 + 1 + len(basic_steps) + 1 + len(alt_steps)
    tbl = doc.add_table(rows=rows_count, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    curr_row = 0
    # Row 0: Banner Title (merge cols 0, 1, 2)
    cell_banner = tbl.cell(curr_row, 0)
    cell_banner.merge(tbl.cell(curr_row, 1)).merge(tbl.cell(curr_row, 2))
    set_cell_background(cell_banner, PRIMARY_COLOR)
    set_cell_margins(cell_banner, top=120, bottom=120, left=140, right=140)
    p = cell_banner.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(f"MẪU ĐẶC TẢ USE CASE: {uc_id} - {uc_name.upper()}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    curr_row += 1

    # Metadata items
    meta_items = [
        ("Tên use case", uc_name),
        ("Actor", actor),
        ("Mô tả", desc),
        ("Tiền điều kiện (Precondition)", pre),
        ("Hậu điều kiện (Postcondition)", post)
    ]
    for lbl, val in meta_items:
        c_lbl = tbl.cell(curr_row, 0)
        c_val = tbl.cell(curr_row, 1)
        c_val.merge(tbl.cell(curr_row, 2))
        
        set_cell_background(c_lbl, "F1F8E9")
        set_cell_background(c_val, "FFFFFF")
        set_cell_margins(c_lbl, top=80, bottom=80, left=100, right=100)
        set_cell_margins(c_val, top=80, bottom=80, left=120, right=120)
        
        p1 = c_lbl.paragraphs[0]
        format_paragraph(p1, space_before=0, space_after=0)
        r1 = p1.add_run(lbl)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10)
        r1.font.bold = True
        
        p2 = c_val.paragraphs[0]
        format_paragraph(p2, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r2 = p2.add_run(val)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10)
        curr_row += 1

    # Basic Flow Header Banner
    c_bf_hdr = tbl.cell(curr_row, 0)
    c_bf_hdr.merge(tbl.cell(curr_row, 1)).merge(tbl.cell(curr_row, 2))
    set_cell_background(c_bf_hdr, "E8F5E9")
    set_cell_margins(c_bf_hdr, top=80, bottom=80, left=120, right=120)
    p = c_bf_hdr.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0)
    r = p.add_run("Luồng sự kiện chính (Basic flow)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    curr_row += 1

    # Basic Steps
    for step_col, act_col, sys_col in basic_steps:
        c0 = tbl.cell(curr_row, 0)
        c1 = tbl.cell(curr_row, 1)
        c2 = tbl.cell(curr_row, 2)
        
        set_cell_background(c0, "FAFAFA")
        set_cell_background(c1, "FFFFFF")
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=90, right=90)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c2, top=70, bottom=70, left=100, right=100)

        p0 = c0.paragraphs[0]
        format_paragraph(p0, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r0 = p0.add_run(step_col)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9.5)
        r0.font.bold = True

        p1 = c1.paragraphs[0]
        format_paragraph(p1, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r1 = p1.add_run(act_col)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5)

        p2 = c2.paragraphs[0]
        format_paragraph(p2, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r2 = p2.add_run(sys_col)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(9.5)
        curr_row += 1

    # Alternate Flow Header Banner
    c_af_hdr = tbl.cell(curr_row, 0)
    c_af_hdr.merge(tbl.cell(curr_row, 1)).merge(tbl.cell(curr_row, 2))
    set_cell_background(c_af_hdr, "FFF3E0")
    set_cell_margins(c_af_hdr, top=80, bottom=80, left=120, right=120)
    p = c_af_hdr.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0)
    r = p.add_run("Luồng sự kiện thay thế / Ngoại lệ (Alternate flow)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0xE6, 0x51, 0x00)
    curr_row += 1

    # Alternate Steps
    for branch_col, act_col, sys_col in alt_steps:
        c0 = tbl.cell(curr_row, 0)
        c1 = tbl.cell(curr_row, 1)
        c2 = tbl.cell(curr_row, 2)
        
        set_cell_background(c0, "FAFAFA")
        set_cell_background(c1, "FFFFFF")
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=90, right=90)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c2, top=70, bottom=70, left=100, right=100)

        p0 = c0.paragraphs[0]
        format_paragraph(p0, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r0 = p0.add_run(branch_col)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(0xC6, 0x28, 0x28)

        p1 = c1.paragraphs[0]
        format_paragraph(p1, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r1 = p1.add_run(act_col)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5)

        p2 = c2.paragraphs[0]
        format_paragraph(p2, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r2 = p2.add_run(sys_col)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(9.5)
        curr_row += 1

    # Set Column widths
    col_widths = [Inches(1.5), Inches(2.6), Inches(2.6)]
    for r in tbl.rows:
        if len(r.cells) == 3:
            r.cells[0].width = col_widths[0]
            r.cells[1].width = col_widths[1]
            r.cells[2].width = col_widths[2]

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

print("Helper functions ready.")
