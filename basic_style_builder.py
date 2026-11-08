# -*- coding: utf-8 -*-
"""
Script tái tạo toàn bộ các tài liệu Word:
1. Bao_Cao_Tien_Do_Do_An_Chuyen_Nganh_AgriXanh.docx
2. Bao_Cao_Do_An_Chuyen_Nganh_AgriXanh.docx
3. Tai_Lieu_So_Do_Thiet_Ke_He_Thong_AgriXanh.docx

Thông tin sinh viên:
- Tên: Trần Dương Phúc
- MSSV: 1250080149
- Lớp: 12_ĐH_THMT

Yêu cầu định dạng:
- Toàn bộ chữ đều ở định dạng MÀU ĐEN (RGB 0, 0, 0)
- Các bảng được thiết kế theo kiểu BASIC chuẩn học thuật như Hình 2:
  + Viền đen toàn bộ (khung ngoài và lưới trong: w:val="single" w:sz="4" w:color="000000")
  + Nền trắng sạch (FFFFFF), không đổ màu xanh hay màu mè
  + Chữ đen 100%, in đậm các tiêu đề
  + Dòng Sub-header phân cột rõ ràng: Luồng | Actor (Tác nhân) | Hệ thống (Controller / Services)
"""
import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from use_cases_data import AGRIXANH_USE_CASES

BASE_DIR = os.path.dirname(__file__)
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")

# Pure black color for all text
COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)

def set_table_borders_basic(table, border_color="000000", sz="4"):
    """Thiết lập viền đen cơ bản cho toàn bộ bảng theo kiểu basic như Hình 2"""
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>'
        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{border_color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def set_cell_margins_basic(cell, top=80, bottom=80, left=100, right=100):
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

def set_cell_white_bg(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="FFFFFF"/>'))

def format_paragraph(p, space_before=0, space_after=4, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.LEFT):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_heading_1_black(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=16, space_after=6)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="0"/>'))
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_BLACK
    return p

def add_heading_2_black(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=12, space_after=4)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="1"/>'))
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_BLACK
    return p

def add_heading_3_black(doc, text):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=8, space_after=3)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:outlineLvl {nsdecls("w")} w:val="2"/>'))
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_BLACK
    return p

def add_body_p_black(doc, text, bold_prefix="", italic_prefix=""):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=4, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(11.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_BLACK
    if italic_prefix:
        r_it = p.add_run(italic_prefix)
        r_it.font.name = "Times New Roman"
        r_it.font.size = Pt(11.5)
        r_it.font.italic = True
        r_it.font.color.rgb = COLOR_BLACK
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11.5)
    run.font.color.rgb = COLOR_BLACK
    return p

def add_bullet_p_black(doc, text, bold_title=""):
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=3, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_title:
        r_title = p.add_run(bold_title)
        r_title.font.name = "Times New Roman"
        r_title.font.size = Pt(11.5)
        r_title.font.bold = True
        r_title.font.color.rgb = COLOR_BLACK
    r_body = p.add_run(text)
    r_body.font.name = "Times New Roman"
    r_body.font.size = Pt(11.5)
    r_body.font.color.rgb = COLOR_BLACK
    return p

def add_code_block_black(doc, code_str, title=None):
    if title:
        p_title = doc.add_paragraph()
        format_paragraph(p_title, space_before=4, space_after=2)
        r = p_title.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_BLACK
        
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_white_bg(cell)
    set_cell_margins_basic(cell, top=100, bottom=100, left=140, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0, line_spacing=1.15)
    r = p.add_run(code_str.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(9.0)
    r.font.color.rgb = COLOR_BLACK
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_with_caption_black(doc, filename, caption_text, width_in=6.0):
    img_path = os.path.join(DIAGRAMS_DIR, filename)
    if not os.path.exists(img_path):
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
    r_cap.font.color.rgb = COLOR_BLACK

def add_table_basic(doc, headers, rows_data, col_widths=None):
    """Bảng kiểu basic viền đen nền trắng chữ đen như Hình 2"""
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_basic(tbl)
    
    # Header row
    hdr_row = tbl.rows[0]
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        set_cell_white_bg(cell)
        set_cell_margins_basic(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        run = p.add_run(heading)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = COLOR_BLACK
        
    # Data rows
    for r_idx, r_data in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            set_cell_white_bg(cell)
            set_cell_margins_basic(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            align = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 0 or len(str(val)) < 8) else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, space_before=0, space_after=0, line_spacing=1.15, align=align)
            run = p.add_run(str(val))
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            run.font.color.rgb = COLOR_BLACK
            
    if col_widths and len(col_widths) == len(headers):
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl

def add_uc_spec_table_image2_style(doc, uc_id, uc_name, actor, desc, pre, post, basic_steps, alt_steps):
    """
    Bảng đặc tả Use Case chuẩn xác 100% theo kiểu basic như Hình 2:
    - Viền đen toàn bộ (khung ngoài và ô trong)
    - Nền trắng (không màu)
    - Toàn bộ chữ đen
    - Đầy đủ dòng banner tiêu đề Use Case
    - Các dòng metadata
    - Dòng tiêu đề 'Luồng sự kiện chính (Basic flow)'
    - Dòng sub-header: Luồng | Actor (Tác nhân) | Hệ thống (Controller / Services)
    - Các bước luồng chính
    - Dòng tiêu đề 'Luồng sự kiện thay thế / Ngoại lệ (Alternate flow)'
    - Dòng sub-header: Rẽ nhánh / Ngoại lệ | Actor (Tác nhân) | Hệ thống (Phản hồi & Xử lý lỗi)
    - Các bước luồng ngoại lệ
    """
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=6, space_after=2)
    r = p_title.add_run(f"{uc_id} - {uc_name}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK

    # Rows count:
    # 1 (Banner) + 5 (Metadata) + 1 (Basic flow banner) + 1 (Basic subheader) + len(basic_steps) + 1 (Alt flow banner) + 1 (Alt subheader) + len(alt_steps)
    total_rows = 1 + 5 + 1 + 1 + len(basic_steps) + 1 + 1 + len(alt_steps)
    tbl = doc.add_table(rows=total_rows, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_basic(tbl)

    curr_row = 0

    # Row 0: Banner MẪU ĐẶC TẢ USE CASE
    c0 = tbl.cell(curr_row, 0)
    c0.merge(tbl.cell(curr_row, 1)).merge(tbl.cell(curr_row, 2))
    set_cell_white_bg(c0)
    set_cell_margins_basic(c0, top=100, bottom=100, left=100, right=100)
    p = c0.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(f"MẪU ĐẶC TẢ USE CASE: {uc_id} - {uc_name.upper()}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK
    curr_row += 1

    # Metadata rows
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
        
        set_cell_white_bg(c_lbl)
        set_cell_white_bg(c_val)
        set_cell_margins_basic(c_lbl, top=70, bottom=70, left=90, right=90)
        set_cell_margins_basic(c_val, top=70, bottom=70, left=90, right=90)
        
        p1 = c_lbl.paragraphs[0]
        format_paragraph(p1, space_before=0, space_after=0)
        r1 = p1.add_run(lbl)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_BLACK
        
        p2 = c_val.paragraphs[0]
        format_paragraph(p2, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r2 = p2.add_run(val)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_BLACK
        curr_row += 1

    # Basic Flow Header Banner
    c_bf = tbl.cell(curr_row, 0)
    c_bf.merge(tbl.cell(curr_row, 1)).merge(tbl.cell(curr_row, 2))
    set_cell_white_bg(c_bf)
    set_cell_margins_basic(c_bf, top=80, bottom=80, left=90, right=90)
    p = c_bf.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0)
    r = p.add_run("Luồng sự kiện chính (Basic flow)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK
    curr_row += 1

    # Basic Flow Sub-headers (như Hình 2)
    sub_headers_bf = ["Luồng", "Actor (Tác nhân)", "Hệ thống (Controller / Services)"]
    for idx, sh in enumerate(sub_headers_bf):
        c = tbl.cell(curr_row, idx)
        set_cell_white_bg(c)
        set_cell_margins_basic(c, top=70, bottom=70, left=80, right=80)
        p = c.paragraphs[0]
        format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(sh)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_BLACK
    curr_row += 1

    # Basic Flow Data Steps
    for step_col, act_col, sys_col in basic_steps:
        c0 = tbl.cell(curr_row, 0)
        c1 = tbl.cell(curr_row, 1)
        c2 = tbl.cell(curr_row, 2)
        
        set_cell_white_bg(c0)
        set_cell_white_bg(c1)
        set_cell_white_bg(c2)
        set_cell_margins_basic(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins_basic(c1, top=60, bottom=60, left=90, right=90)
        set_cell_margins_basic(c2, top=60, bottom=60, left=90, right=90)

        p0 = c0.paragraphs[0]
        format_paragraph(p0, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r0 = p0.add_run(step_col)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_BLACK

        p1 = c1.paragraphs[0]
        format_paragraph(p1, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r1 = p1.add_run(act_col)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_BLACK

        p2 = c2.paragraphs[0]
        format_paragraph(p2, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r2 = p2.add_run(sys_col)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_BLACK
        curr_row += 1

    # Alternate Flow Header Banner
    c_af = tbl.cell(curr_row, 0)
    c_af.merge(tbl.cell(curr_row, 1)).merge(tbl.cell(curr_row, 2))
    set_cell_white_bg(c_af)
    set_cell_margins_basic(c_af, top=80, bottom=80, left=90, right=90)
    p = c_af.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0)
    r = p.add_run("Luồng sự kiện thay thế / Ngoại lệ (Alternate flow)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK
    curr_row += 1

    # Alternate Flow Sub-headers (như Hình 2)
    sub_headers_af = ["Rẽ nhánh / Ngoại lệ", "Actor (Tác nhân)", "Hệ thống (Phản hồi & Xử lý lỗi)"]
    for idx, sh in enumerate(sub_headers_af):
        c = tbl.cell(curr_row, idx)
        set_cell_white_bg(c)
        set_cell_margins_basic(c, top=70, bottom=70, left=80, right=80)
        p = c.paragraphs[0]
        format_paragraph(p, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(sh)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_BLACK
    curr_row += 1

    # Alternate Flow Data Steps
    for branch_col, act_col, sys_col in alt_steps:
        c0 = tbl.cell(curr_row, 0)
        c1 = tbl.cell(curr_row, 1)
        c2 = tbl.cell(curr_row, 2)
        
        set_cell_white_bg(c0)
        set_cell_white_bg(c1)
        set_cell_white_bg(c2)
        set_cell_margins_basic(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins_basic(c1, top=60, bottom=60, left=90, right=90)
        set_cell_margins_basic(c2, top=60, bottom=60, left=90, right=90)

        p0 = c0.paragraphs[0]
        format_paragraph(p0, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r0 = p0.add_run(branch_col)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_BLACK

        p1 = c1.paragraphs[0]
        format_paragraph(p1, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r1 = p1.add_run(act_col)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_BLACK

        p2 = c2.paragraphs[0]
        format_paragraph(p2, space_before=0, space_after=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r2 = p2.add_run(sys_col)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_BLACK
        curr_row += 1

    col_widths = [Inches(1.5), Inches(2.6), Inches(2.6)]
    for r in tbl.rows:
        if len(r.cells) == 3:
            r.cells[0].width = col_widths[0]
            r.cells[1].width = col_widths[1]
            r.cells[2].width = col_widths[2]

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

print("Basic table builder ready.")
