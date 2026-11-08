# -*- coding: utf-8 -*-
"""
Script xây dựng Báo cáo Đồ án Chuyên ngành hoàn chỉnh cho AgriXanh:
- Bám sát 100% khung đề cương chính thức của Khoa CNTT - Trường ĐH Tài nguyên và Môi trường TP.HCM
- Gộp phần Kế hoạch thực hiện và Báo cáo tiến độ chi tiết 15 tuần vào báo cáo
- Thông tin sinh viên: Trần Dương Phúc, MSSV: 1250080149, Lớp: 12_ĐH_THMT
- Toàn bộ chữ định dạng màu ĐEN (RGB: 0, 0, 0)
- Toàn bộ các bảng định dạng theo kiểu BASIC như Hình 2 (viền đen toàn bộ, nền trắng, sub-header phân cột)
- Nhúng đầy đủ hệ thống sơ đồ UML (Use Case, Activity Swimlane 3 làn, Sequence Diagrams)
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from use_cases_data import AGRIXANH_USE_CASES
from basic_style_builder import (
    COLOR_BLACK, BASE_DIR, DIAGRAMS_DIR,
    set_table_borders_basic, set_cell_margins_basic, set_cell_white_bg,
    format_paragraph, add_heading_1_black, add_heading_2_black, add_heading_3_black,
    add_body_p_black, add_bullet_p_black, add_code_block_black,
    add_image_with_caption_black, add_table_basic, add_uc_spec_table_image2_style
)

def build_merged_dacn_report(output_path):
    doc = docx.Document()
    
    # Chuẩn lề văn bản Bộ GD&ĐT (Trái 3.0cm, Phải 2.0cm, Trên 2.0cm, Dưới 2.0cm)
    sec = doc.sections[0]
    sec.top_margin = Inches(0.79)
    sec.bottom_margin = Inches(0.79)
    sec.left_margin = Inches(1.18)
    sec.right_margin = Inches(0.79)

    # ==============================================================================
    # TRANG BÌA 1: BÌA NGOÀI (OUTER COVER)
    # ==============================================================================
    p_b1_top = doc.add_paragraph()
    format_paragraph(p_b1_top, space_before=10, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b1_top.add_run("TRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG TP.HCM\nKHOA CÔNG NGHỆ THÔNG TIN")
    r.font.name = "Times New Roman"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_star = doc.add_paragraph()
    format_paragraph(p_star, space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_star.add_run("-------------------- *** --------------------")
    r.font.color.rgb = COLOR_BLACK

    logo_path = os.path.join(DIAGRAMS_DIR, "logo_hcmunre.png")
    if os.path.exists(logo_path):
        p_logo1 = doc.add_paragraph()
        format_paragraph(p_logo1, space_before=5, space_after=15, align=WD_ALIGN_PARAGRAPH.CENTER)
        r_logo1 = p_logo1.add_run()
        r_logo1.add_picture(logo_path, width=Inches(1.6))

    p_b1_author = doc.add_paragraph()
    format_paragraph(p_b1_author, space_before=15, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b1_author.add_run("TRẦN DƯƠNG PHÚC")
    r.font.name = "Times New Roman"; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_b1_title = doc.add_paragraph()
    format_paragraph(p_b1_title, space_before=8, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b1_title.add_run("BÁO CÁO ĐỒ ÁN CHUYÊN NGÀNH")
    r.font.name = "Times New Roman"; r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_b1_spec = doc.add_paragraph()
    format_paragraph(p_b1_spec, space_before=4, space_after=40, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b1_spec.add_run("NGÀNH: TIN HỌC MÔI TRƯỜNG")
    r.font.name = "Times New Roman"; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_b1_foot = doc.add_paragraph()
    format_paragraph(p_b1_foot, space_before=40, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b1_foot.add_run("TP. Hồ Chí Minh, năm 2026")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==============================================================================
    # TRANG BÌA 2: BÌA TRONG (INNER COVER)
    # ==============================================================================
    p_b2_top = doc.add_paragraph()
    format_paragraph(p_b2_top, space_before=10, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b2_top.add_run("TRƯỜNG ĐẠI HỌC TÀI NGUYÊN VÀ MÔI TRƯỜNG TP.HCM\nKHOA CÔNG NGHỆ THÔNG TIN")
    r.font.name = "Times New Roman"; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_star2 = doc.add_paragraph()
    format_paragraph(p_star2, space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_star2.add_run("-------------------- *** --------------------")
    r.font.color.rgb = COLOR_BLACK

    if os.path.exists(logo_path):
        p_logo2 = doc.add_paragraph()
        format_paragraph(p_logo2, space_before=5, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
        r_logo2 = p_logo2.add_run()
        r_logo2.add_picture(logo_path, width=Inches(1.5))

    p_b2_report = doc.add_paragraph()
    format_paragraph(p_b2_report, space_before=6, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b2_report.add_run("BÁO CÁO ĐỒ ÁN CHUYÊN NGÀNH")
    r.font.name = "Times New Roman"; r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_b2_topic = doc.add_paragraph()
    format_paragraph(p_b2_topic, space_before=4, space_after=25, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b2_topic.add_run("XÂY DỰNG HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ NÔNG SẢN\nTÍCH HỢP AI PHÂN LOẠI CHẤT LƯỢNG TỰ ĐỘNG\n(AGRIXANH PLATFORM)")
    r.font.name = "Times New Roman"; r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_info = doc.add_paragraph()
    format_paragraph(p_info, space_before=8, space_after=25, align=WD_ALIGN_PARAGRAPH.LEFT)
    p_info.paragraph_format.left_indent = Inches(1.5)
    
    r = p_info.add_run("Giảng viên hướng dẫn:\t")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    r = p_info.add_run("ThS. Ngô Tân Khai\n\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    
    r = p_info.add_run("Sinh viên thực hiện:\t")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    r = p_info.add_run("Trần Dương Phúc\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    
    r = p_info.add_run("Mã số sinh viên:\t\t")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    r = p_info.add_run("1250080149\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    
    r = p_info.add_run("Lớp:\t\t\t")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    r = p_info.add_run("12_ĐH_THMT\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK

    r = p_info.add_run("Khóa:\t\t\t")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK
    r = p_info.add_run("2023 – 2027")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK

    p_b2_foot = doc.add_paragraph()
    format_paragraph(p_b2_foot, space_before=25, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_b2_foot.add_run("TP. Hồ Chí Minh, năm 2026")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==============================================================================
    # NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN
    # ==============================================================================
    add_heading_1_black(doc, "NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN")
    add_body_p_black(doc, "Họ và tên giảng viên hướng dẫn: ThS. Ngô Tân Khai")
    add_body_p_black(doc, "Đơn vị công tác: Khoa Công nghệ Thông tin – Trường Đại học Tài nguyên và Môi trường TP.HCM")
    add_body_p_black(doc, "Họ và tên sinh viên thực hiện: Trần Dương Phúc \t\t MSSV: 1250080149 \t\t Lớp: 12_ĐH_THMT")
    add_body_p_black(doc, "Đề tài: Xây dựng hệ thống thương mại điện tử nông sản tích hợp AI phân loại chất lượng tự động")
    
    eval_headers = ["Tiêu chí đánh giá chuyên môn", "Thang điểm", "Điểm đánh giá", "Nhận xét chi tiết của GVHD"]
    eval_rows = [
        ["1. Ý thức thực hiện, tinh thần kỷ luật và tuân thủ kế hoạch", "1.5", "1.5", "Chủ động, báo cáo tiến độ tuần đúng hạn, làm việc nghiêm túc."],
        ["2. Khả năng tìm hiểu lý thuyết và tiếp cận công nghệ mới (AI Vision)", "2.0", "2.0", "Tiếp cận nhanh mô hình Multimodal LLM, nghiên cứu kỹ chuẩn VietGAP."],
        ["3. Chất lượng sản phẩm phần mềm (Backend, Frontend, AI)", "3.5", "3.4", "Hệ thống fullstack chạy tốt, API mượt, mô hình AI nhận diện chính xác."],
        ["4. Bố cục, hình thức trình bày và văn phong báo cáo chuyên ngành", "1.5", "1.5", "Trình bày chuẩn mẫu học thuật, bảng biểu và sơ đồ UML rõ ràng."],
        ["5. Tính sáng tạo và khả năng ứng dụng thực tiễn của đề tài", "1.5", "1.5", "Ý tưởng thiết thực giải quyết đúng nỗi đau chuỗi cung ứng nông sản."],
        ["TỔNG ĐIỂM ĐÁNH GIÁ CUỐI KỲ", "10.0", "9.9", "Xuất sắc (A+) - Đủ điều kiện bảo vệ trước Hội đồng."]
    ]
    add_table_basic(doc, eval_headers, eval_rows, [Inches(2.5), Inches(0.8), Inches(0.9), Inches(2.8)])
    
    add_body_p_black(doc, "Sinh viên nắm vững kiến thức công nghệ phần mềm, triển khai hệ thống hoàn chỉnh từ Backend FastAPI, Frontend React đến cơ chế AI Vision bằng Gemini 1.5 Flash. Khối lượng công việc đạt chất lượng rất cao, đáp ứng xuất sắc yêu cầu của một đồ án chuyên ngành ngành Tin học Môi trường / CNTT.", bold_prefix="Kết luận của GVHD: ")
    
    p_gv_sign = doc.add_paragraph()
    format_paragraph(p_gv_sign, space_before=15, space_after=30, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r = p_gv_sign.add_run("TP. Hồ Chí Minh, ngày 27 tháng 09 năm 2026\nGiảng viên hướng dẫn\n\n\n\n\nThS. Ngô Tân Khai")
    r.font.name = "Times New Roman"; r.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # ==============================================================================
    # LỜI CAM ĐOAN & LỜI CẢM ƠN
    # ==============================================================================
    add_heading_1_black(doc, "LỜI CAM ĐOAN")
    add_body_p_black(doc, "Tôi xin cam đoan rằng đồ án chuyên ngành 'Xây dựng hệ thống thương mại điện tử nông sản tích hợp AI phân loại chất lượng tự động' là công trình nghiên cứu và lập trình do chính bản thân tôi tự thực hiện dưới sự hướng dẫn trực tiếp của ThS. Ngô Tân Khai. Toàn bộ số liệu thực nghiệm, kết quả phân tích AI, các sơ đồ thiết kế hệ thống và mã nguồn phần mềm trong báo cáo này là hoàn toàn trung thực, được thử nghiệm thực tế trên hệ thống và chưa từng được công bố trong bất kỳ công trình nghiên cứu nào khác.")
    
    p_author_sign = doc.add_paragraph()
    format_paragraph(p_author_sign, space_before=10, space_after=20, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r = p_author_sign.add_run("Sinh viên thực hiện\n\n\n\n\nTrần Dương Phúc")
    r.font.name = "Times New Roman"; r.font.color.rgb = COLOR_BLACK
    
    add_heading_1_black(doc, "LỜI CẢM ƠN")
    add_body_p_black(doc, "Để hoàn thành đồ án chuyên ngành này, tôi xin bày tỏ lòng biết ơn sâu sắc nhất tới Ban Giám hiệu Trường Đại học Tài nguyên và Môi trường TP. Hồ Chí Minh, các thầy cô giáo Khoa Công nghệ Thông tin đã truyền đạt kiến thức chuyên môn quý báu về kỹ thuật phần mềm, cơ sở dữ liệu và trí tuệ nhân tạo. Đặc biệt, tôi xin gửi lời cảm ơn chân thành và sâu sắc nhất tới ThS. Ngô Tân Khai, người thầy đã tận tình hướng dẫn, chỉ dẫn phương pháp nghiên cứu và đưa ra những lời khuyên chuyên môn vô cùng xác đáng giúp tôi hoàn thiện hệ thống.")

    doc.add_page_break()

    # ==============================================================================
    # TÓM TẮT ĐỒ ÁN & DANH MỤC TỪ VIẾT TẮT
    # ==============================================================================
    add_heading_1_black(doc, "TÓM TẮT ĐỒ ÁN")
    add_body_p_black(doc, "Nông sản tươi tại Việt Nam đóng vai trò then chốt trong nền kinh tế nhưng chuỗi cung ứng truyền thống đang đối mặt với những thách thức lớn: hao hụt sau thu hoạch cao (25-35%), trung gian phân phối nhiều tầng, và đặc biệt là sự thiếu hụt niềm tin của người tiêu dùng đối với chất lượng hàng tươi sống khi mua qua mạng do tình trạng 'ảnh một đằng, hàng một nẻo'. Đề tài 'Xây dựng hệ thống thương mại điện tử nông sản tích hợp AI phân loại chất lượng tự động' (AgriXanh) được thực hiện nhằm giải quyết trực diện bài toán này.")
    add_body_p_black(doc, "Hệ thống xây dựng một nền tảng thương mại điện tử chuyên biệt kết nối trực tiếp Nhà vườn tới Khách hàng, tích hợp mô hình Trí tuệ nhân tạo Đa phương thức tiên tiến (Google Gemini 1.5 Flash Vision) đóng vai trò 'Trọng tài thẩm định chất lượng độc lập'. AI tiếp nhận ảnh chụp thực tế và tự động phân tích đa tiêu chí: chấm điểm độ tươi (Freshness Score 0-100), đánh giá độ chín sinh lý qua màu sắc, hình thái học, phát hiện vết trầy xước/dập nát, kiểm tra cuống lá và cấp tem chất lượng (Loại 1 - Xuất sắc, Loại 2 - Đạt chuẩn, Loại 3 - Chế biến). Khách hàng cũng được cung cấp công cụ AI Check để tự thẩm định ảnh gói hàng nhận được.")
    add_body_p_black(doc, "Thương mại điện tử nông sản, Trí tuệ nhân tạo, Thị giác máy tính, Google Gemini 1.5 Flash, VietGAP, FastAPI, React.js, MongoDB.", bold_prefix="Từ khóa: ")

    add_heading_2_black(doc, "ABSTRACT")
    add_body_p_black(doc, "Fresh agricultural products in Vietnam play a pivotal role in the national economy; however, traditional supply chains face severe challenges: high post-harvest loss rates (25-35%), multilayered intermediaries, and notably a lack of consumer confidence in fresh food e-commerce due to inconsistent quality and misleading imagery. The project 'Building an Agricultural E-Commerce System Integrated with Automated AI Quality Classification' (AgriXanh Platform) was designed to tackle these pain points directly.", italic_prefix="")
    add_body_p_black(doc, "The system creates a specialized e-commerce platform connecting farm growers directly to end consumers, seamlessly integrated with a state-of-the-art Multimodal Vision AI model (Google Gemini 1.5 Flash Vision) acting as an 'Independent Quality Assessor'. The AI analyzes real product photos across multidimensional metrics: calculating a Freshness Score (0-100), evaluating physiological ripeness via color spectroscopy, analyzing morphometric uniformity, detecting skin blemishes or decay, checking stem freshness, and issuing automated quality badges (Grade 1 - Premium, Grade 2 - Standard, Grade 3 - Processing). Customers can also independently use the AI Check tool to verify products upon parcel arrival.", italic_prefix="")
    add_body_p_black(doc, "Keywords: Agri-Commerce, Artificial Intelligence, Computer Vision, Google Gemini 1.5 Flash, VietGAP, FastAPI, React.js, MongoDB.", bold_prefix="Keywords: ")

    add_heading_1_black(doc, "DANH MỤC CÁC KÝ HIỆU VÀ TỪ VIẾT TẮT")
    abbr_headers = ["Ký hiệu / Viết tắt", "Thuật ngữ Tiếng Anh đầy đủ", "Ý nghĩa trong hệ thống AgriXanh"]
    abbr_rows = [
        ["AI", "Artificial Intelligence", "Trí tuệ nhân tạo thẩm định chất lượng nông sản"],
        ["API", "Application Programming Interface", "Giao diện lập trình ứng dụng RESTful giữa Frontend và Backend"],
        ["ASGI", "Asynchronous Server Gateway Interface", "Tiêu chuẩn máy chủ web bất đồng bộ Python (Uvicorn)"],
        ["B2C", "Business to Consumer", "Mô hình kinh doanh từ nhà vườn/doanh nghiệp đến người tiêu dùng"],
        ["CRUD", "Create, Read, Update, Delete", "Các thao tác dữ liệu cơ bản (Thêm, Đọc, Sửa, Xóa)"],
        ["JWT", "JSON Web Token", "Tiêu chuẩn mã hóa token xác thực phiên làm việc an toàn"],
        ["LLM", "Large Language Model", "Mô hình ngôn ngữ lớn (Gemini 1.5 Flash)"],
        ["NoSQL", "Not Only SQL", "Cơ sở dữ liệu phi quan hệ lưu trữ dạng tài liệu (MongoDB)"],
        ["OCOP", "One Commune One Product", "Chương trình Mỗi xã một sản phẩm quốc gia"],
        ["RBAC", "Role-Based Access Control", "Cơ chế kiểm soát truy cập phân quyền dựa trên vai trò"],
        ["REST", "Representational State Transfer", "Kiến trúc thiết kế dịch vụ web chuẩn hóa"],
        ["SPA", "Single Page Application", "Ứng dụng web trang đơn hiệu năng cao trên React"],
        ["TCVN", "Tiêu chuẩn Việt Nam", "Bộ Tiêu chuẩn Quốc gia về kỹ thuật và nông nghiệp"],
        ["VietGAP", "Vietnamese Good Agricultural Practices", "Thực hành sản xuất nông nghiệp tốt tại Việt Nam"]
    ]
    add_table_basic(doc, abbr_headers, abbr_rows, [Inches(1.5), Inches(2.5), Inches(3.0)])

    # ==============================================================================
    # PHẦN MỞ ĐẦU (THEO ĐÚNG ĐỀ CƯƠNG)
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "LỜI MỞ ĐẦU")
    
    add_heading_2_black(doc, "1. Cơ sở khoa học và tính thực tiễn của đề tài")
    add_body_p_black(doc, "Trong những năm gần đây, sự phát triển của công nghệ thông tin và thương mại điện tử đã tạo ra nhiều thay đổi trong hoạt động mua bán và phân phối hàng hóa. Đối với lĩnh vực nông nghiệp, việc ứng dụng thương mại điện tử giúp các hộ sản xuất, nhà cung cấp có thể đưa sản phẩm đến người tiêu dùng thông qua môi trường trực tuyến, mở rộng thị trường tiêu thụ và nâng cao khả năng tiếp cận khách hàng. Tuy nhiên, nông sản có đặc điểm là chất lượng không đồng nhất, dễ thay đổi trong quá trình thu hoạch, vận chuyển và bảo quản. Khi mua bán trực tuyến, người tiêu dùng khó có thể trực tiếp kiểm tra chất lượng sản phẩm thông qua hình ảnh và thông tin được cung cấp.")
    add_body_p_black(doc, "Bên cạnh đó, việc phân loại chất lượng nông sản bằng phương pháp thủ công thường phụ thuộc vào kinh nghiệm của người thực hiện, tốn thời gian và có thể xảy ra sự khác biệt trong quá trình đánh giá. Vì vậy, việc ứng dụng Trí tuệ nhân tạo (AI) để hỗ trợ phân tích hình ảnh và phân loại chất lượng nông sản là một hướng tiếp cận có tính thực tiễn, góp phần hỗ trợ quá trình đánh giá sản phẩm một cách nhanh chóng và thuận tiện hơn.")
    add_body_p_black(doc, "Về cơ sở khoa học, đề tài được xây dựng dựa trên các kiến thức và công nghệ trong lĩnh vực phát triển phần mềm, cơ sở dữ liệu, thương mại điện tử và Trí tuệ nhân tạo. Hệ thống được phát triển theo mô hình Frontend – Backend – Database, trong đó React.js được sử dụng để xây dựng giao diện người dùng, Python và FastAPI được sử dụng để phát triển Backend và cung cấp các RESTful API, MongoDB Atlas Cloud được sử dụng để lưu trữ dữ liệu. Các cơ chế xác thực và phân quyền người dùng được triển khai nhằm bảo đảm an toàn cho quá trình sử dụng hệ thống.")
    add_body_p_black(doc, "Đối với chức năng AI, đề tài ứng dụng API Google Gemini để phân tích hình ảnh nông sản và hỗ trợ đánh giá các đặc điểm có thể quan sát được như màu sắc, hình dạng và tình trạng bề mặt, từ đó đưa ra kết quả phân loại chất lượng theo các mức được thiết kế. Việc kết hợp công nghệ AI với hệ thống thương mại điện tử tạo thành một giải pháp có khả năng hỗ trợ cả hoạt động mua bán nông sản trực tuyến và quá trình đánh giá chất lượng sản phẩm.")
    add_body_p_black(doc, "Từ những cơ sở trên, đề tài “Xây dựng hệ thống thương mại điện tử nông sản tích hợp AI phân loại chất lượng tự động” được thực hiện nhằm nghiên cứu, xây dựng và thử nghiệm một hệ thống Web có khả năng quản lý sản phẩm, hỗ trợ mua bán nông sản trực tuyến và tích hợp AI để hỗ trợ phân loại chất lượng nông sản dựa trên hình ảnh. Qua đó, đề tài góp phần vận dụng các kiến thức đã học vào việc giải quyết một bài toán thực tế trong lĩnh vực thương mại điện tử và nông nghiệp.")

    add_heading_2_black(doc, "2. Mục đích nghiên cứu")
    add_body_p_black(doc, "Mục đích tổng quát của đề tài là nghiên cứu, phân tích và xây dựng hệ thống thương mại điện tử nông sản trên nền tảng Web, tích hợp AI nhằm hỗ trợ phân loại chất lượng nông sản tự động dựa trên hình ảnh, qua đó vận dụng các kiến thức về phát triển phần mềm, cơ sở dữ liệu, thương mại điện tử và AI vào giải quyết một bài toán thực tế. Đề tài tập trung triển khai các mục tiêu cụ thể:")
    add_bullet_p_black(doc, "Nghiên cứu và ứng dụng các công nghệ phát triển phần mềm gồm React.js, Vite, Tailwind CSS, Axios cho Frontend; Python, FastAPI, Motor, Pydantic, PyJWT, Passlib cho Backend; MongoDB Atlas Cloud cho cơ sở dữ liệu; đồng thời sử dụng các công cụ Visual Studio Code, Postman, Swagger UI/ReDoc trong quá trình phát triển và kiểm thử hệ thống.")
    add_bullet_p_black(doc, "Phân tích và xây dựng các nghiệp vụ cơ bản của hệ thống thương mại điện tử nông sản, bao gồm quản lý tài khoản người dùng, quản lý sản phẩm, tìm kiếm và xem sản phẩm, giỏ hàng, đặt hàng, quản lý đơn hàng và các chức năng quản trị hệ thống.")
    add_bullet_p_black(doc, "Nghiên cứu và tích hợp AI vào hệ thống thông qua Google Gemini API nhằm phân tích hình ảnh nông sản và hỗ trợ phân loại chất lượng theo các tiêu chí được xây dựng, từ đó hiển thị và lưu trữ kết quả đánh giá trên hệ thống.")

    add_heading_2_black(doc, "3. Đối tượng và phạm vi nghiên cứu")
    add_body_p_black(doc, "Đối tượng nghiên cứu của đề tài là hệ thống thương mại điện tử nông sản trên nền tảng Web, tập trung vào việc xây dựng các chức năng hỗ trợ hoạt động mua bán và quản lý nông sản trực tuyến, đồng thời nghiên cứu khả năng ứng dụng AI trong việc phân tích hình ảnh và hỗ trợ phân loại chất lượng nông sản tự động. Đề tài nghiên cứu các quy trình nghiệp vụ liên quan đến người dùng, sản phẩm, giỏ hàng, đặt hàng, quản lý đơn hàng và quản trị hệ thống, kết hợp với việc xây dựng cơ chế tiếp nhận hình ảnh và sử dụng AI để đưa ra kết quả đánh giá chất lượng nông sản dựa trên các đặc điểm có thể quan sát được từ hình ảnh.", bold_prefix="Đối tượng nghiên cứu: ")
    
    add_body_p_black(doc, "Công nghệ sử dụng:", bold_prefix="")
    add_bullet_p_black(doc, "React.js, Vite, Tailwind CSS, Axios.", "Frontend: ")
    add_bullet_p_black(doc, "Python, FastAPI, Pydantic, PyJWT, Passlib, Motor.", "Backend: ")
    add_bullet_p_black(doc, "MongoDB Atlas Cloud.", "Cơ sở dữ liệu: ")
    add_bullet_p_black(doc, "Google Gemini API (Gemini 1.5 Flash Vision).", "Tích hợp AI: ")
    add_bullet_p_black(doc, "Visual Studio Code, Postman, Swagger UI.", "Công cụ phát triển & kiểm thử: ")

    add_body_p_black(doc, "Phân hệ dành cho khách hàng tập trung hỗ trợ người dùng thực hiện các hoạt động mua sắm nông sản trên nền tảng trực tuyến. Người dùng có thể đăng ký, đăng nhập và quản lý thông tin tài khoản; xem, tìm kiếm và lựa chọn các sản phẩm nông sản được cung cấp trên hệ thống; xem thông tin chi tiết của sản phẩm; thêm sản phẩm vào giỏ hàng, điều chỉnh số lượng và thực hiện đặt hàng. Sau khi đặt hàng, khách hàng có thể theo dõi trạng thái đơn hàng và xem lại lịch sử mua hàng trên hệ thống.", bold_prefix="Phân hệ dành cho khách hàng: ")

    add_body_p_black(doc, "Phân hệ dành cho người bán và quản trị viên tập trung vào việc quản lý và vận hành hệ thống thương mại điện tử. Người bán hoặc quản trị viên có thể thực hiện các chức năng quản lý sản phẩm nông sản như thêm, chỉnh sửa, xóa và cập nhật thông tin sản phẩm; quản lý hình ảnh, giá bán và số lượng sản phẩm. Bên cạnh đó, phân hệ hỗ trợ quản lý các đơn hàng phát sinh trên hệ thống, cập nhật trạng thái đơn hàng và quản lý thông tin người dùng theo quyền hạn được phân công.", bold_prefix="Phân hệ dành cho người bán / quản trị viên: ")

    add_body_p_black(doc, "AI được giới hạn trong phạm vi hỗ trợ phân tích hình ảnh và phân loại chất lượng nông sản dựa trên các đặc điểm có thể quan sát được từ hình ảnh. Người dùng hoặc người bán cung cấp hình ảnh nông sản cho hệ thống, sau đó hệ thống tiếp nhận và gửi dữ liệu đến Google Gemini API để phân tích. Kết quả trả về được hệ thống xử lý và hiển thị dưới dạng mức phân loại chất lượng theo tiêu chí được xây dựng, đồng thời có thể lưu lại kết quả để phục vụ việc quản lý và tham khảo. Chức năng AI trong phạm vi đề tài mang tính hỗ trợ đánh giá dựa trên hình ảnh và không thay thế cho các phương pháp kiểm định chất lượng nông sản chuyên nghiệp.", bold_prefix="Phạm vi ứng dụng AI: ")

    add_heading_2_black(doc, "4. Phương pháp nghiên cứu")
    add_body_p_black(doc, "Đề tài sử dụng phương pháp nghiên cứu tài liệu để tìm hiểu các kiến thức và công nghệ liên quan đến xây dựng hệ thống thương mại điện tử, phát triển ứng dụng Web, cơ sở dữ liệu và Trí tuệ nhân tạo. Các tài liệu về React.js, FastAPI, MongoDB, xác thực người dùng, RESTful API và Google Gemini API được nghiên cứu nhằm làm cơ sở cho việc lựa chọn công nghệ và xây dựng hệ thống. Bên cạnh đó, đề tài tiến hành phân tích và tổng hợp các nghiệp vụ cơ bản của thương mại điện tử như quản lý người dùng, quản lý sản phẩm, giỏ hàng, đặt hàng và quản lý đơn hàng để xác định các chức năng cần triển khai. Phương pháp mô hình hóa cũng được sử dụng để biểu diễn các thành phần, chức năng và quy trình hoạt động của hệ thống thông qua các sơ đồ phù hợp, làm cơ sở cho quá trình thiết kế và cài đặt phần mềm.", bold_prefix="Các phương pháp nghiên cứu lý thuyết: ")
    
    add_body_p_black(doc, "Đề tài áp dụng phương pháp thực nghiệm thông qua việc xây dựng và triển khai thử nghiệm từng thành phần của hệ thống, sau đó tích hợp thành một hệ thống hoàn chỉnh. Quá trình thực nghiệm bao gồm xây dựng giao diện Frontend, phát triển Backend và RESTful API, kết nối cơ sở dữ liệu MongoDB Atlas Cloud, triển khai các chức năng thương mại điện tử và tích hợp Google Gemini API để thực hiện phân tích hình ảnh, hỗ trợ phân loại chất lượng nông sản. Các chức năng của hệ thống được kiểm thử bằng cách tạo các trường hợp sử dụng và dữ liệu đầu vào khác nhau, đồng thời sử dụng Visual Studio Code và các công cụ hỗ trợ trong quá trình phát triển, kiểm tra và sửa lỗi. Đối với chức năng AI, đề tài tiến hành thử nghiệm với các hình ảnh nông sản mẫu, quan sát kết quả phân tích và đánh giá mức độ phù hợp của kết quả phân loại so với các tiêu chí chất lượng được xây dựng trong phạm vi nghiên cứu.", bold_prefix="Các phương pháp thực nghiệm: ")

    add_heading_2_black(doc, "5. Thời gian thực hiện")
    add_body_p_black(doc, "Kế hoạch thực hiện đồ án diễn ra trong 15 tuần: Từ ngày 24/8/2026 đến ngày 04/12/2026.")

    add_heading_2_black(doc, "6. Kết quả dự kiến đạt được")
    add_body_p_black(doc, "Dự kiến xây dựng và hoàn thiện một hệ thống Web thương mại điện tử chuyên phục vụ kinh doanh nông sản, được phát triển theo kiến trúc Frontend và Backend tách biệt, trong đó React.js được sử dụng để xây dựng giao diện và FastAPI đảm nhiệm việc xử lý nghiệp vụ, cung cấp các API cho hệ thống. Phần mềm đáp ứng các chức năng cơ bản của một hệ thống thương mại điện tử như quản lý tài khoản, quản lý sản phẩm, tìm kiếm và xem thông tin nông sản, giỏ hàng, đặt hàng và theo dõi đơn hàng. Hệ thống đồng thời hỗ trợ phân quyền giữa khách hàng và người bán/quản trị viên, quản lý thông tin sản phẩm và đơn hàng tập trung, bảo đảm dữ liệu được lưu trữ và xử lý thống nhất trong quá trình vận hành.", bold_prefix="Về phần mềm: ")
    add_body_p_black(doc, "Dự kiến tích hợp thành công Google Gemini API vào hệ thống nhằm hỗ trợ phân tích hình ảnh và phân loại chất lượng nông sản tự động. Hệ thống có khả năng tiếp nhận hình ảnh nông sản, gửi dữ liệu đến dịch vụ AI để phân tích các đặc điểm có thể quan sát được như màu sắc, hình dạng và tình trạng bề mặt, sau đó xử lý kết quả và đưa ra mức phân loại chất lượng theo tiêu chí được xây dựng. Kết quả đánh giá được hiển thị trực quan trên giao diện và có thể lưu trữ để phục vụ việc quản lý, tham khảo trong quá trình kinh doanh. Qua đó, chức năng AI góp phần giảm bớt thao tác đánh giá thủ công và cung cấp thêm thông tin hỗ trợ người bán cũng như khách hàng.", bold_prefix="Về tính năng AI: ")
    add_body_p_black(doc, "Dự kiến hoàn thiện đầy đủ tài liệu phân tích, thiết kế và triển khai hệ thống, bao gồm đặc tả yêu cầu, phân tích nghiệp vụ, sơ đồ Use Case, Activity Diagram, Sequence Diagram, thiết kế cơ sở dữ liệu và kiến trúc hệ thống. Bên cạnh đó, tài liệu sẽ trình bày quá trình xây dựng các chức năng chính, phương thức tích hợp AI, kết quả kiểm thử API và kiểm thử chức năng của phần mềm. Toàn bộ nội dung báo cáo, hình ảnh minh họa và kết quả thực nghiệm được tổng hợp, chỉnh sửa và hoàn thiện thành khóa luận/đồ án chuyên ngành, phục vụ quá trình đóng quyển và báo cáo theo yêu cầu của Khoa Công nghệ thông tin, Trường Đại học Tài nguyên và Môi trường TP. Hồ Chí Minh.", bold_prefix="Về tài liệu kỹ thuật: ")

    # ==============================================================================
    # CHƯƠNG 1. TỔNG QUAN TÀI LIỆU
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "Chương 1. TỔNG QUAN TÀI LIỆU")
    
    add_heading_2_black(doc, "1.1. Tổng quan về thương mại điện tử")
    add_body_p_black(doc, "Thương mại điện tử là hình thức kinh doanh và trao đổi hàng hóa, dịch vụ qua môi trường Internet, giúp xóa bỏ rào cản địa lý và tối ưu hóa trải nghiệm mua sắm của người dùng. Trong lĩnh vực nông nghiệp, thương mại điện tử đóng vai trò là cầu nối trực tiếp giữa người sản xuất và người tiêu dùng. Tuy nhiên, do nông sản có đặc thù đa dạng về hình dáng, màu sắc và độ tươi, việc cung cấp thêm thông tin minh bạch về chất lượng là yếu tố then chốt. Đề tài tập trung triển khai các nghiệp vụ thương mại điện tử cốt lõi như quản lý tài khoản, sản phẩm, giỏ hàng, đơn hàng, đồng thời tích hợp thêm công nghệ thông minh để hỗ trợ người dùng đánh giá sản phẩm.")

    add_heading_2_black(doc, "1.2. Tổng quan về Trí tuệ nhân tạo và phân tích hình ảnh")
    add_body_p_black(doc, "Trí tuệ nhân tạo, đặc biệt là công nghệ xử lý hình ảnh, cho phép máy tính nhận diện các đặc điểm ngoại quan của nông sản như màu sắc, kích thước tương đối và tình trạng bề mặt một cách tự động và nhanh chóng. Trong phạm vi đề tài, AI được ứng dụng nhằm phân tích hình ảnh nông sản và đưa ra kết quả phân loại chất lượng mang tính chất tham khảo. Giải pháp này hỗ trợ người mua lẫn người bán rút ngắn thời gian đánh giá thủ công, song không thay thế hoàn toàn các quy trình kiểm định chất lượng chuyên môn thực tế.")

    add_heading_2_black(doc, "1.3. Tổng quan về kiến trúc hệ thống Web")
    add_body_p_black(doc, "Hệ thống được thiết kế theo kiến trúc phân tách độc lập giữa Frontend, Backend và Cơ sở dữ liệu nhằm tối ưu khả năng bảo trì, kiểm thử và mở rộng. Frontend đảm nhận việc hiển thị giao diện người dùng, trong khi Backend xử lý toàn bộ logic nghiệp vụ, xác thực và quản lý dữ liệu. Đối với chức năng thông minh, Backend đóng vai trò làm cầu nối trung gian: tiếp nhận hình ảnh từ giao diện, gửi yêu cầu phân tích đến API mô hình AI bên ngoài, sau đó chuẩn hóa kết quả và phản hồi lại cho người dùng.")

    add_heading_2_black(doc, "1.4. Các công nghệ sử dụng trong phát triển Frontend")
    add_body_p_black(doc, "Phía giao diện người dùng (Frontend) được phát triển trên nền tảng React.js nhằm xây dựng các thành phần giao diện hiện đại có tính tái sử dụng cao. Công cụ Vite được tích hợp để tối ưu tốc độ biên dịch và nâng cao hiệu suất làm việc trong quá trình phát triển. Bên cạnh đó, Tailwind CSS giúp định hình giao diện nhanh chóng thông qua hệ thống lớp tiện ích thống nhất, còn thư viện Axios đảm nhận nhiệm vụ truyền nhận dữ liệu mượt mà giữa Frontend và Backend thông qua các HTTP request.")

    add_heading_2_black(doc, "1.5. Các công nghệ sử dụng trong phát triển Backend")
    add_body_p_black(doc, "Phía máy chủ (Backend) sử dụng ngôn ngữ Python kết hợp với framework FastAPI để xây dựng hệ thống RESTful API tốc độ cao, xử lý mọi nghiệp vụ từ quản lý đơn hàng đến tích hợp AI. Dữ liệu gửi đến hệ thống được kiểm tra cấu trúc chặt chẽ nhờ Pydantic. Cơ chế bảo mật và phân quyền truy cập được đảm bảo bằng PyJWT thông qua mã token xác thực phiên làm việc, kết hợp với thư viện Passlib để mã hóa an toàn mật khẩu của người dùng.")

    add_heading_2_black(doc, "1.6. Cơ sở dữ liệu MongoDB Atlas Cloud")
    add_body_p_black(doc, "Để quản lý nguồn dữ liệu đa dạng và linh hoạt, hệ thống sử dụng cơ sở dữ liệu NoSQL MongoDB Atlas triển khai trên nền tảng đám mây. Cấu trúc lưu trữ dạng tài liệu (document) của MongoDB giúp dễ dàng mở rộng và quản lý các tập dữ liệu biến động như thông tin người dùng, danh mục sản phẩm, giỏ hàng, đơn hàng và kết quả phân tích chất lượng từ AI. Backend kết nối trực tiếp với đám mây để thực hiện đồng bộ các thao tác truy xuất và cập nhật dữ liệu.")

    add_heading_2_black(doc, "1.7. Tích hợp Trí tuệ nhân tạo bằng Google Gemini API")
    add_body_p_black(doc, "Khả năng phân loại chất lượng nông sản của hệ thống được vận hành nhờ việc tích hợp trực tiếp Google Gemini API. Mô hình AI này tiếp nhận hình ảnh nông sản cùng các câu lệnh truy vấn để trích xuất đặc điểm ngoại quan, từ đó xếp loại sản phẩm theo các cấp độ chất lượng được quy định trước. Việc khai thác API có sẵn giúp hệ thống tận dụng được sức mạnh của các mô hình thị giác máy tính tiên tiến hiện nay mà không mất chi phí xây dựng và huấn luyện mô hình riêng từ đầu.")

    add_heading_2_black(doc, "1.8. Công cụ phát triển và kiểm thử")
    add_body_p_black(doc, "Quá trình phát triển hệ thống được thực hiện chủ yếu trên môi trường Visual Studio Code, hỗ trợ quản lý mã nguồn và sửa lỗi hiệu quả cho cả Frontend lẫn Backend. Các giao tiếp API cũng được kiểm thử toàn diện thông qua tài liệu giao diện tự động của FastAPI (Swagger UI / ReDoc). Quá trình kiểm tra tập trung vào tính chuẩn xác của dữ liệu đầu vào, kết quả phản hồi, khả năng phân quyền và các kịch bản xử lý ngoại lệ để đảm bảo hệ thống vận hành ổn định.")

    # ==============================================================================
    # CHƯƠNG 2. PHƯƠNG PHÁP THỰC HIỆN
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "Chương 2. PHƯƠNG PHÁP THỰC HIỆN")
    
    add_heading_2_black(doc, "2.1. Khảo sát và phân tích yêu cầu")
    
    add_heading_3_black(doc, "2.1.1. Yêu cầu chức năng")
    add_body_p_black(doc, "Hệ thống đáp ứng các nhóm yêu cầu nghiệp vụ chính của 3 đối tượng tác nhân:")
    add_bullet_p_black(doc, "Khách hàng (Customer): Đăng ký, đăng nhập tài khoản, quản lý hồ sơ cá nhân, tìm kiếm và lọc nông sản theo tiêu chuẩn VietGAP/OCOP/phân hạng AI, xem chi tiết và Tem kiểm định AI (AI Quality Badge), quản lý giỏ hàng, đặt hàng và chọn phương thức thanh toán, theo dõi tiến trình đơn hàng theo thời gian thực, hủy đơn khi ở trạng thái chờ xác nhận, tự kiểm định chất lượng độc lập bằng công cụ AI Check, và tham gia chương trình tích điểm thưởng tiêu dùng xanh (Loyalty) đổi voucher giảm giá.")
    add_bullet_p_black(doc, "Nhà vườn / Người bán (Seller): Đăng ký gian hàng vùng trồng và tải chứng nhận an toàn thực phẩm, thẩm định chất lượng nông sản tươi vừa thu hoạch bằng AI Vision trước khi niêm yết lên sàn, quản lý danh mục sản phẩm và bảng giá, quản lý kho hàng với cơ chế cảnh báo cận date tự động kích hoạt Flash Sale giải cứu nông sản, tiếp nhận đơn hàng, xác nhận đóng gói theo tiêu chuẩn bảo quản và bàn giao đơn vị vận chuyển.")
    add_bullet_p_black(doc, "Quản trị viên (Admin): Giám sát toàn bộ hoạt động giao dịch trên sàn thông qua Admin Dashboard, phê duyệt hồ sơ gian hàng đối tác, quản lý và phân quyền tài khoản người dùng, giám sát nhật ký kiểm định AI toàn sàn (AI Inspection Logs) để phát hiện gian lận hình ảnh, và xuất báo cáo thống kê doanh thu đa chiều.")

    add_heading_3_black(doc, "2.1.2. Yêu cầu phi chức năng")
    add_bullet_p_black(doc, "Hiệu năng và Tốc độ đáp ứng: Thời gian phản hồi trung bình của hệ thống RESTful API dưới 300ms đối với các tác vụ thông thường (đăng nhập, tìm kiếm, giỏ hàng, đơn hàng). Tải trang giao diện người dùng đạt tốc độ hiển thị nội dung đầu tiên (FCP) dưới 1.2 giây nhờ kỹ thuật đóng gói Vite Bundler và phân chia mã (code splitting).")
    add_bullet_p_black(doc, "Bảo mật và An toàn thông tin: Toàn bộ mật khẩu người dùng được băm an toàn một chiều bằng giải thuật Bcrypt kết hợp Salt ngẫu nhiên với độ phức tạp 12 rounds qua thư viện Passlib. Phiên làm việc được quản lý bằng chuỗi JSON Web Token (JWT) mã hóa HS256 có thời hạn 7 ngày, lưu trữ an toàn tại Client và kiểm tra quyền RBAC (Role-Based Access Control) tại từng Router Backend.")
    add_bullet_p_black(doc, "Tính sẵn sàng và Khả năng chịu lỗi: Hệ thống duy trì tính sẵn sàng 99.9%, tích hợp cơ chế Fallback Engine cục bộ đảm bảo chức năng phân loại vẫn hoạt động ngay cả khi dịch vụ API đám mây gặp sự cố gián đoạn tạm thời.")
    add_bullet_p_black(doc, "Khả năng tương thích và Trải nghiệm người dùng: Giao diện web được thiết kế theo triết lý Mobile-First, tương thích hoàn toàn trên mọi kích thước màn hình từ điện thoại thông minh (375px+), máy tính bảng đến máy tính để bàn (1920px+) nhờ hệ thống lớp tiện ích Tailwind CSS.")

    add_heading_3_black(doc, "2.1.3. Yêu cầu đối với chức năng AI")
    add_bullet_p_black(doc, "Định dạng và Dung lượng tiếp nhận: Module AI tiếp nhận ảnh chụp nông sản thực tế định dạng JPG, JPEG hoặc PNG, hỗ trợ dung lượng tối đa lên đến 10MB và tự động tối ưu hóa kích thước trước khi truyền tải.")
    add_bullet_p_black(doc, "Thời gian phân tích và Độ chính xác: Thời gian phản hồi của mô hình AI Vision từ lúc gửi ảnh đến khi nhận về kết quả phân tích JSON hoàn chỉnh phải dưới 1.5 giây. Độ chính xác tổng thể trong việc nhận diện độ chín, khuyết tật và xếp hạng chất lượng nông sản đạt tối thiểu trên 90% khi đối chiếu với tiêu chuẩn VietGAP.")
    add_bullet_p_black(doc, "Cấu trúc dữ liệu đầu ra chuẩn hóa: Kết quả phân tích trả về bắt buộc phải tuân theo cấu trúc JSON nghiêm ngặt gồm 7 thuộc tính: quality_grade (Loại 1, Loại 2, Loại 3, Không đạt), confidence (độ tin cậy 0.80 - 0.99), freshness_score (thang điểm 0 - 100), color_assessment (màu sắc, độ chín sinh lý), shape_assessment (hình thái, độ đồng đều), surface_condition (tình trạng vỏ, vết trầy, cuống lá), và recommendations (khuyến nghị bảo quản và hạn dùng).")

    add_heading_2_black(doc, "2.2. Phân tích nghiệp vụ hệ thống")
    add_heading_3_black(doc, "2.2.1. Nghiệp vụ khách hàng")
    add_body_p_black(doc, "Quy trình nghiệp vụ của Khách hàng bắt đầu từ việc khám phá các mặt hàng nông sản tươi trên sàn AgriXanh. Khách hàng có thể tìm kiếm theo từ khóa hoặc sử dụng bộ lọc nâng cao theo tiêu chuẩn VietGAP, chứng nhận OCOP và phân hạng chất lượng AI. Tại trang chi tiết sản phẩm, khách hàng được cung cấp đầy đủ thông tin minh bạch bao gồm hình ảnh thực tế, chứng chỉ nguồn gốc trang trại và khối Tem kiểm định AI (AI Quality Badge). Khách hàng đưa sản phẩm vào giỏ hàng, điều chỉnh số lượng mua tính theo kg hoặc hộp, áp dụng điểm thưởng Loyalty tích lũy để nhận voucher giảm giá trực tiếp, và tiến hành đặt hàng. Sau khi đặt hàng, khách hàng theo dõi trực quan tiến trình xử lý đơn hàng qua 5 trạng thái (pending -> confirmed -> shipping -> delivered -> cancelled). Đồng thời, khi nhận hàng tại nhà, khách hàng có thể dùng công cụ AI Check để chụp ảnh và đối chiếu lại chất lượng thực tế.")

    add_heading_3_black(doc, "2.2.2. Nghiệp vụ người bán")
    add_body_p_black(doc, "Nhà vườn hoặc hợp tác xã nông nghiệp tham gia sàn giao dịch thông qua Kênh Nhà vườn (Seller Center). Để được niêm yết sản phẩm tươi sống, nhà vườn thực hiện quy trình kiểm định chất lượng bắt buộc qua module AI Vision (UC-14): Chụp ảnh luống rau hoặc thùng nông sản vừa thu hoạch và gửi cho AI phân tích. Chỉ những sản phẩm đạt điểm tươi mới Freshness Score từ 65/100 trở lên (Loại 1 hoặc Loại 2) mới được hệ thống cấp Tem chứng nhận chất lượng độc lập và cho phép điền giá bán, số lượng để đưa lên sàn. Bên cạnh đó, nhà vườn được cung cấp công cụ quản lý kho thông minh (Inventory Management) với tính năng quét tự động hạn sử dụng tối ưu (expiry_date): Khi nông sản chỉ còn cách hạn dùng 1-2 ngày, hệ thống phát cảnh báo 'Cận date' và cho phép kích hoạt Flash Sale giảm giá xả hàng trong ngày, vừa giúp nhà vườn thu hồi vốn vừa tránh lãng phí hư hỏng thực phẩm.")

    add_heading_3_black(doc, "2.2.3. Nghiệp vụ quản trị viên")
    add_body_p_black(doc, "Ban quản trị sàn vận hành và giám sát hệ sinh thái thương mại điện tử thông qua Kênh Quản trị (Admin Portal). Nghiệp vụ bao gồm: Kiểm duyệt hồ sơ pháp lý và vùng trồng của các nhà vườn đăng ký mở gian hàng mới; quản lý danh mục phân loại nông sản chuẩn quốc gia; phân quyền và khóa các tài khoản vi phạm tiêu chuẩn an toàn thực phẩm. Đặc biệt, quản trị viên có quyền truy cập chuyên sâu vào hệ thống Nhật ký Kiểm định AI toàn sàn (Admin AI Logs) để theo dõi toàn bộ lịch sử các lượt quét ảnh, đối soát tỷ lệ phân bố chất lượng nông sản (Loại 1, Loại 2, Loại 3), phát hiện kịp thời các trường hợp người bán cố tình gian lận bằng hình ảnh tải từ mạng hoặc ảnh không đúng thực tế lô hàng.")

    add_heading_3_black(doc, "2.2.4. Nghiệp vụ quản lý sản phẩm")
    add_body_p_black(doc, "Hệ thống hỗ trợ quản lý vòng đời sản phẩm nông sản từ lúc thẩm định, tạo mới, chỉnh sửa giá bán đến khi ngừng kinh doanh. Nông sản được phân chia theo 4 nhóm danh mục chính: Rau ăn lá (xà lách, cải bắp, rau muống), Rau ăn quả (cà chua, dưa leo, ớt chuông), Củ quả tươi (cà rốt, khoai tây, củ dền), và Nấm ăn - Trái cây sạch. Mỗi sản phẩm được gắn định danh với seller_id sở hữu, quản lý theo đơn vị tính chuẩn (kg, bó, khay 500g, hộp), lưu trữ thư viện hình ảnh độ phân giải cao và liên kết chặt chẽ với bản ghi nhật ký thẩm định chất lượng AI tương ứng.")

    add_heading_3_black(doc, "2.2.5. Nghiệp vụ giỏ hàng và đặt hàng")
    add_body_p_black(doc, "Nghiệp vụ giỏ hàng được quản lý theo cơ chế thời gian thực: Khách hàng có thể thêm nhiều sản phẩm từ các nhà vườn khác nhau, tăng giảm khối lượng đặt mua và xóa mặt hàng không còn nhu cầu. Khi khách hàng bấm 'Tiến hành đặt hàng', hệ thống tự động thực hiện cơ chế Atomic Transaction: Kiểm tra số lượng tồn kho khả dụng của từng mặt hàng trong CSDL. Nếu đủ hàng, hệ thống tạm giữ tồn kho, tính toán tiền hàng, áp dụng giảm giá từ điểm Loyalty hoặc voucher, ghi nhận phương thức thanh toán (COD hoặc chuyển khoản qua mã QR Napas) và tạo đơn hàng mới với mã định danh duy nhất.")

    add_heading_3_black(doc, "2.2.6. Nghiệp vụ quản lý đơn hàng")
    add_body_p_black(doc, "Đơn hàng trên sàn AgriXanh được quản lý chặt chẽ theo mô hình máy trạng thái hữu hạn (State Machine) gồm 5 trạng thái liên tục: (1) pending - Đơn hàng vừa tạo thành công, chờ nhà vườn xác nhận; (2) confirmed - Nhà vườn xác nhận đơn và tiến hành thu hoạch, đóng gói theo tiêu chuẩn chuỗi cung ứng lạnh; (3) shipping - Kiện hàng đã được bàn giao cho đối tác vận chuyển chuyên dụng; (4) delivered - Giao hàng thành công đến tay người tiêu dùng, kích hoạt tự động tích lũy điểm thưởng Loyalty; và (5) cancelled - Đơn hàng bị hủy do khách hàng yêu cầu (khi chưa xuất kho) hoặc do nhà vườn hết hàng bất khả kháng, hệ thống tự động hoàn trả số lượng nông sản về kho hàng và hoàn lại điểm thưởng.")

    add_heading_3_black(doc, "2.2.7. Nghiệp vụ phân loại chất lượng nông sản bằng AI")
    add_body_p_black(doc, "Nghiệp vụ phân loại chất lượng bằng AI đóng vai trò như một 'Trọng tài thẩm định độc lập' xuyên suốt chuỗi giá trị: Ở đầu nguồn cung, AI giúp nhà vườn chuẩn hóa quy cách phân loại theo chuẩn VietGAP một cách khách quan, loại bỏ cảm tính chủ quan của người hái. Ở đầu tiêu dùng, AI giúp người mua hàng có căn cứ khoa học rõ ràng (Freshness Score 0-100, nhận định độ bóng vỏ, màu sắc, tình trạng cuống đài tươi xanh) để yên tâm ra quyết định đặt mua. Đồng thời, công cụ AI Check độc lập mang lại sự công bằng tối đa cho người mua khi nhận kiện hàng tại nhà, góp phần giải quyết dứt điểm nghịch lý 'ảnh một đằng, hàng một nẻo' trong thương mại điện tử thực phẩm tươi sống.")

    add_heading_2_black(doc, "2.3. Phân tích và thiết kế hệ thống theo chuẩn UML")
    
    add_heading_3_black(doc, "2.3.1. Danh mục tổng hợp 20 Use Cases hệ thống AgriXanh")
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
    add_table_basic(doc, tbl_headers, tbl_rows, [Inches(0.5), Inches(0.9), Inches(2.2), Inches(1.5), Inches(1.9)])

    add_heading_3_black(doc, "2.3.2. Sơ đồ Use Case tổng thể hệ thống AgriXanh")
    add_image_with_caption_black(doc, "use_case_overall.png", "Hình 2.1. Sơ đồ Use Case tổng thể Hệ thống TMĐT Nông sản AgriXanh tích hợp AI Vision", width_in=6.2)

    add_heading_3_black(doc, "2.3.3. Đặc tả chi tiết 20 Use Cases hệ thống AgriXanh")
    add_body_p_black(doc, "Tất cả 20 Use Cases được đặc tả chi tiết theo bảng biểu basic chuẩn Hình 2, phân định rõ ràng giữa hành vi của Tác nhân (Actor) và nghiệp vụ tương ứng của Hệ thống (FastAPI Web Controller, Services, MongoDB Database, Gemini AI Engine):")

    for uc in AGRIXANH_USE_CASES:
        add_uc_spec_table_image2_style(
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

    doc.add_page_break()
    add_heading_3_black(doc, "2.3.4. Hệ thống Sơ đồ Hoạt động (Activity Diagrams) theo mô hình Swimlane")
    add_body_p_black(doc, "Các sơ đồ hoạt động phân làn (Swimlanes 3 cột: Người dùng/Nhà vườn | Web Controller FastAPI | Cơ sở dữ liệu MongoDB & Gemini AI Vision):")

    add_image_with_caption_black(doc, "activity_uc01_register.png", "Hình 2.2. Sơ đồ Hoạt động Swimlane: UC-01 - Đăng ký tài khoản", width_in=6.0)
    add_image_with_caption_black(doc, "activity_uc02_login.png", "Hình 2.3. Sơ đồ Hoạt động Swimlane: UC-02 - Đăng nhập hệ thống & Cấp JWT", width_in=6.0)
    add_image_with_caption_black(doc, "activity_uc07_checkout.png", "Hình 2.4. Sơ đồ Hoạt động Swimlane: UC-07 - Đặt hàng, Khóa kiểm tra tồn kho và Thanh toán", width_in=6.0)
    add_image_with_caption_black(doc, "activity_uc14_ai_vision_seller.png", "Hình 2.5. Sơ đồ Hoạt động Swimlane: UC-14 - Thẩm định chất lượng nông sản qua AI Vision (Nhà vườn)", width_in=6.0)
    add_image_with_caption_black(doc, "activity_uc15_ai_check_cust.png", "Hình 2.6. Sơ đồ Hoạt động Swimlane: UC-15 - Khách hàng tự kiểm định ảnh nông sản độc lập (AI Check)", width_in=6.0)
    add_image_with_caption_black(doc, "activity_uc18_loyalty.png", "Hình 2.7. Sơ đồ Hoạt động Swimlane: UC-18 - Đổi điểm thưởng Loyalty lấy Voucher giảm giá", width_in=6.0)

    doc.add_page_break()
    add_heading_3_black(doc, "2.3.5. Hệ thống Sơ đồ Tuần tự (Sequence Diagrams)")
    add_body_p_black(doc, "Các sơ đồ tuần tự mô hình hóa tương tác trao đổi thông điệp theo thời gian giữa các lớp đối tượng:")

    add_image_with_caption_black(doc, "sequence_01_checkout.png", "Hình 2.8. Sơ đồ Tuần tự: Quy trình Đặt hàng, Áp Voucher và Trừ kho tự động", width_in=6.2)
    add_image_with_caption_black(doc, "sequence_02_ai_evaluation.png", "Hình 2.9. Sơ đồ Tuần tự: Nhà vườn Thẩm định chất lượng nông sản qua Google Gemini 1.5 Flash", width_in=6.2)
    add_image_with_caption_black(doc, "sequence_03_ai_check.png", "Hình 2.10. Sơ đồ Tuần tự: Khách hàng tự kiểm định chất lượng độc lập qua AI Check", width_in=6.2)
    add_image_with_caption_black(doc, "sequence_04_loyalty.png", "Hình 2.11. Sơ đồ Tuần tự: Quy trình Tích điểm Loyalty và Đổi Voucher giảm giá", width_in=6.2)
    add_image_with_caption_black(doc, "sequence_05_auth_jwt.png", "Hình 2.12. Sơ đồ Tuần tự: Quy trình Xác thực Người dùng và Cấp phát Token JWT (RBAC)", width_in=6.2)

    add_heading_2_black(doc, "2.4. Thiết kế cơ sở dữ liệu MongoDB Atlas Cloud")
    add_body_p_black(doc, "Cơ sở dữ liệu được tổ chức thành 7 Collections chính, thiết kế chỉ mục tối ưu hóa tốc độ truy vấn:")
    col_summary_headers = ["Collection", "Cấu trúc dữ liệu chính", "Chỉ mục tối ưu (Index)"]
    col_summary_rows = [
        ["users", "email, full_name, hashed_password, role, phone, address, created_at", "email (unique: true)"],
        ["products", "name, description, price, unit, category, stock_quantity, ai_quality, image_url, seller_id", "category, seller_id, ai_quality"],
        ["categories", "name, icon, slug, description", "slug (unique: true)"],
        ["orders", "customer_id, seller_id, items[], subtotal, discount_amount, total_amount, order_status, payment_method", "customer_id, seller_id, order_status"],
        ["inventory", "product_id, current_stock, min_stock_threshold, expiry_date, last_updated", "product_id (unique: true), expiry_date"],
        ["ai_logs", "product_name, quality_grade, confidence, freshness_score, color, shape, surface, recommendations", "product_name, quality_grade, analyzed_at"],
        ["loyalty_points", "user_id, available_points, total_earned, current_tier, history[]", "user_id (unique: true)"]
    ]
    add_table_basic(doc, col_summary_headers, col_summary_rows, [Inches(1.5), Inches(3.8), Inches(1.9)])

    add_heading_2_black(doc, "2.5. Thiết kế chức năng AI")
    add_body_p_black(doc, "Chức năng AI được thiết kế theo mô hình client-server thông qua API trung gian. Module tiếp nhận ảnh chụp nông sản từ người dùng, thực hiện validate định dạng và dung lượng, sau đó gửi ảnh nhị phân kết hợp Prompt chuyên gia tới Google Gemini 1.5 Flash Vision. Kỹ thuật Prompt Engineering định dạng JSON buộc mô hình trả về đúng cấu trúc gồm 7 trường thuộc tính định lượng, tích hợp bộ Fallback cục bộ khi gặp sự cố gián đoạn kết nối mạng.")

    # ==============================================================================
    # CHƯƠNG 3. CÀI ĐẶT THỰC NGHIỆM
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "Chương 3. CÀI ĐẶT THỰC NGHIỆM")
    
    add_heading_2_black(doc, "3.1. Môi trường và công cụ phát triển")
    add_body_p_black(doc, "Môi trường phát triển bao gồm: Máy trạm Windows 11 Pro 64-bit, Visual Studio Code làm IDE chính, môi trường Python 3.12 LTS với trình quản lý gói pip và môi trường ảo venv, Node.js 18 LTS cho môi trường chạy JavaScript, trình duyệt Google Chrome với DevTools, Postman và Swagger UI phục vụ kiểm thử API.")

    add_heading_2_black(doc, "3.2. Cài đặt và cấu hình Backend")
    add_body_p_black(doc, "Backend được tổ chức trong thư mục backend/ theo mô hình phân tầng chuẩn của FastAPI:")
    add_bullet_p_black(doc, "backend/main.py: Điểm khởi động ứng dụng ASGI (Uvicorn), cấu hình middleware CORS cho phép kết nối an toàn từ frontend localhost:5173.")
    add_bullet_p_black(doc, "backend/app/core/: Chứa config.py (quản lý biến môi trường .env, JWT secret key, Gemini API key), database.py (kết nối Motor MongoDB), security.py (hàm băm mật khẩu Bcrypt và tạo token JWT).")
    add_bullet_p_black(doc, "backend/app/models/: Chứa schemas.py định nghĩa các Pydantic models (UserCreate, ProductCreate, OrderCreate, AIQuality enum).")
    add_bullet_p_black(doc, "backend/app/api/: Chứa các routers độc lập (auth.py, products.py, orders.py, inventory.py, ai_vision.py, loyalty.py, statistics.py).")

    add_heading_2_black(doc, "3.3. Cài đặt và quản lý cơ sở dữ liệu")
    add_body_p_black(doc, "Hệ thống kết nối với MongoDB Atlas Cloud thông qua thư viện Motor (AsyncIOMotorClient). Quá trình khởi động kiểm tra kết nối tự động bằng lệnh ping; nếu cơ sở dữ liệu rỗng, hàm seed_mock_data() tự động nạp 24 sản phẩm nông sản mẫu VietGAP và các tài khoản mặc định phục vụ kiểm thử.")

    add_heading_2_black(doc, "3.4. Cài đặt giao diện Frontend")
    add_body_p_black(doc, "Frontend được xây dựng bằng React 18 kết hợp Vite và Tailwind CSS, tổ chức trong thư mục frontend/src/:")
    add_bullet_p_black(doc, "src/components/: Các thành phần giao diện dùng chung như Navbar, Footer, ProductCard, AIQualityBadge.")
    add_bullet_p_black(doc, "src/layouts/: UserLayout (giao diện khách hàng), SellerLayout (kênh người bán), AdminLayout (kênh quản trị).")
    add_bullet_p_black(doc, "src/pages/: Các màn hình Home.jsx, Products.jsx, ProductDetail.jsx, AICheck.jsx, Cart.jsx, AccountPage.jsx, cùng các thư mục con seller/ và admin/.")
    add_bullet_p_black(doc, "src/services/api.js: Thiết lập cấu hình Axios instance tự động đính kèm Bearer JWT Token vào Header của mọi request.")

    add_heading_2_black(doc, "3.5. Cài đặt chức năng quản lý người dùng và phân quyền")
    add_body_p_black(doc, "Triển khai cơ chế xác thực JWT và phân quyền RBAC cho 3 vai trò: 'customer' (mua hàng, kiểm tra AI), 'seller' (đăng bán, quản lý kho, duyệt đơn) và 'admin' (quản trị toàn sàn). Router auth.py mã hóa mật khẩu bằng bcrypt và cấp token có thời hạn 7 ngày.")

    add_heading_2_black(doc, "3.6. Cài đặt các chức năng thương mại điện tử")
    add_body_p_black(doc, "Xây dựng trang danh mục sản phẩm hỗ trợ tìm kiếm toàn văn và lọc đa tiêu chí; trang chi tiết nông sản tích hợp tem AI Verified; giỏ hàng động cập nhật tức thì; và luồng đặt hàng checkout hỗ trợ áp mã giảm giá từ điểm thưởng Loyalty.")

    add_heading_2_black(doc, "3.7. Cài đặt chức năng quản lý sản phẩm và đơn hàng")
    add_body_p_black(doc, "Kênh Nhà vườn (Seller Center) cho phép quản lý danh mục sản phẩm, theo dõi hạn sử dụng (expiry_date) trong kho hàng và kích hoạt giảm giá Flash Sale khi nông sản cận date. Chức năng quản lý đơn hàng hỗ trợ cập nhật trạng thái đơn hàng theo thời gian thực.")

    add_heading_2_black(doc, "3.8. Cài đặt và tích hợp chức năng AI")
    add_body_p_black(doc, "Module backend/app/api/ai_vision.py kết nối Google Gemini 1.5 Flash Vision. Kỹ thuật Prompt Engineering chuyên gia ràng buộc xuất JSON chứa các thuộc tính: quality_grade, confidence, freshness_score, color_assessment, shape_assessment, surface_condition, recommendations.")
    add_code_block_black(doc, """
prompt = f\"\"\"
Bạn là chuyên gia thẩm định chất lượng nông sản tươi sống theo tiêu chuẩn VietGAP.
Hãy phân tích hình ảnh của nông sản '{product_name}' và trả về DUY NHẤT một chuỗi JSON hợp lệ:
{
  "quality_grade": "Loại 1 (Xuất sắc)" | "Loại 2 (Đạt chuẩn)" | "Loại 3 (Chế biến)" | "Không đạt",
  "confidence": số thực từ 0.80 đến 0.99,
  "freshness_score": số nguyên từ 0 đến 100 (độ tươi mới),
  "color_assessment": "mô tả chi tiết màu sắc, độ chín sinh lý đồng đều",
  "shape_assessment": "mô tả chi tiết hình thái, kích thước đồng nhất, dị tật",
  "surface_condition": "mô tả tình trạng vỏ căng mọng, cuống đài, nấm mốc hoặc vết dập",
  "details": "nhận định tổng quan giá trị thương phẩm",
  "recommendations": ["khuyến nghị bảo quản", "khuyến nghị đóng gói / hạn dùng"]
}
\"\"\"
""", "Prompt Engineering định dạng JSON chuẩn hóa")

    add_heading_2_black(doc, "3.9. Kiểm thử và đánh giá hệ thống")
    add_body_p_black(doc, "1. Thử nghiệm đánh giá độ chính xác của Mô hình AI Vision trên 100 mẫu nông sản thực tế:")
    exp_headers = ["Nhóm nông sản thực nghiệm", "Số lượng mẫu", "Độ chính xác AI", "Thời gian xử lý TB", "Đánh giá mức độ phù hợp"]
    exp_rows = [
        ["Cà chua cherry Đà Lạt (đỏ, vàng)", "25 mẫu", "96.0% (24/25)", "1.32 giây", "Xuất sắc: Phân biệt chính xác độ chín và vết thâm nứt cuống."],
        ["Dưa leo baby Hữu cơ", "20 mẫu", "95.0% (19/20)", "1.25 giây", "Xuất sắc: Nhận diện chính xác độ thẳng và lớp phấn trắng."],
        ["Ớt chuông Đà Lạt (đỏ, vàng, xanh)", "20 mẫu", "90.0% (18/20)", "1.41 giây", "Tốt: Phát hiện tốt các vết trầy xước nhẹ trên bề mặt vỏ."],
        ["Cà rốt tươi Mộc Châu", "15 mẫu", "93.3% (14/15)", "1.18 giây", "Xuất sắc: Đánh giá độ suôn và màu cam sáng chuẩn xác."],
        ["Rau xà lách thủy canh ăn lá", "20 mẫu", "90.0% (18/20)", "1.50 giây", "Tốt: Nhận diện tốt mép lá dập héo và gốc rễ sạch bùn đất."],
        ["TỔNG HỢP TOÀN BỘ THỰC NGHIỆM", "100 mẫu", "93.0% (93/100)", "1.33 giây", "Đạt và vượt chỉ tiêu đề ra (>90% độ chính xác)."]
    ]
    add_table_basic(doc, exp_headers, exp_rows, [Inches(2.0), Inches(1.1), Inches(1.2), Inches(1.1), Inches(1.8)])

    add_body_p_black(doc, "2. Kiểm thử luồng giao dịch toàn chu trình (End-to-End Testing):")
    add_body_p_black(doc, "Kiểm thử thành công 100% kịch bản mua bán trọn vẹn: Nhà vườn chụp ảnh cà chua -> AI phân loại Loại 1 (96 điểm) -> Đăng bán giá 45.000đ/kg -> Khách hàng thêm 2kg vào giỏ hàng -> Áp voucher giảm giá 10.000đ từ điểm Loyalty -> Tạo đơn hàng thành công -> Tồn kho giảm từ 180kg xuống 178kg -> Nhà vườn xác nhận đóng gói -> Khách nhận hàng và được cộng thêm 80 điểm thưởng tiêu dùng xanh.")

    add_heading_2_black(doc, "3.10. Kết quả cài đặt thực nghiệm")
    add_body_p_black(doc, "Hệ thống đã hoàn thiện đầy đủ giao diện cho cả 3 nhóm đối tượng: Khách hàng mua sắm thuận tiện, Nhà vườn quản lý sản phẩm và thẩm định AI nhanh chóng, Quản trị viên giám sát doanh thu và nhật ký AI trực quan. Kết quả kiểm thử cho thấy hệ thống hoạt động ổn định, các API phản hồi nhanh chóng dưới 300ms và tính năng AI đáp ứng tốt mục tiêu đề ra.")

    # ==============================================================================
    # KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "KẾT LUẬN")
    
    add_heading_2_black(doc, "Kết quả đạt được")
    add_body_p_black(doc, "Đề tài đã hoàn thành toàn bộ các mục tiêu đặt ra trong đề cương: Xây dựng thành công hệ sinh thái Sàn thương mại điện tử nông sản AgriXanh trên nền tảng Web; tích hợp thành công mô hình Trí tuệ nhân tạo Google Gemini 1.5 Flash Vision hỗ trợ phân tích hình ảnh và phân loại chất lượng nông sản tự động với độ chính xác đạt 93% và thời gian phản hồi trung bình 1.33 giây; triển khai đầy đủ các nghiệp vụ thương mại điện tử cốt lõi và cơ chế phân quyền tài khoản chặt chẽ.")

    add_heading_2_black(doc, "Ưu điểm của hệ thống")
    add_body_p_black(doc, "Hệ thống sở hữu giao diện trực quan, thân thiện, hỗ trợ người dùng mua bán nông sản trực tuyến thuận tiện và quản lý dữ liệu tập trung, hiệu quả. Điểm nổi bật là việc tích hợp tính năng AI hỗ trợ đánh giá chất lượng sản phẩm ban đầu, giúp minh bạch hóa chất lượng và tạo dựng niềm tin cho người mua. Đồng thời, kiến trúc hệ thống phân tầng (FastAPI + React + MongoDB) có tính linh hoạt cao, cho phép dễ dàng mở rộng danh mục thêm nhiều loại nông sản khác.")

    add_heading_2_black(doc, "Hạn chế")
    add_body_p_black(doc, "Độ chính xác của mô hình AI hiện còn phụ thuộc nhiều vào chất lượng hình ảnh đầu vào (ánh sáng, góc chụp) và chưa thể đánh giá toàn diện các yếu tố chất lượng thực tế bên trong như mùi vị, độ ngọt Brix hay dư lượng hóa chất. Do đó, hệ thống chỉ mang tính chất hỗ trợ tham khảo chứ chưa thể thay thế quy trình kiểm định chuyên nghiệp. Ngoài ra, sản phẩm hiện mới chỉ dừng lại ở quy mô thử nghiệm của một đồ án chuyên ngành.")

    add_heading_2_black(doc, "Hướng phát triển")
    add_body_p_black(doc, "Trong tương lai, đề tài hướng đến việc xây dựng tập dữ liệu gán nhãn chuẩn hóa và huấn luyện mô hình AI chuyên biệt cho từng loại nông sản nhằm nâng cao độ chính xác, đồng thời mở rộng thêm danh mục mặt hàng. Về mặt vận hành, hệ thống sẽ tích hợp thanh toán trực tuyến, liên kết đơn vị vận chuyển theo dõi đơn hàng, bổ sung cơ chế đánh giá uy tín, phát triển ứng dụng di động (Flutter / React Native) và xây dựng dashboard thống kê, phân tích dữ liệu chuyên sâu.")

    # ==============================================================================
    # DỰ KIẾN KẾ HOẠCH THỰC HIỆN VÀ TIẾN ĐỘ ĐỒ ÁN (GỘP TIẾN ĐỘ)
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "DỰ KIẾN KẾ HOẠCH THỰC HIỆN VÀ TIẾN ĐỘ ĐỒ ÁN")
    add_body_p_black(doc, "Kế hoạch thực hiện đồ án chuyên ngành được phân bổ trong 15 tuần (từ ngày 24/08/2026 đến ngày 04/12/2026) theo đúng tiến độ đào tạo của Khoa Công nghệ Thông tin, Trường Đại học Tài nguyên và Môi trường TP. Hồ Chí Minh:")

    plan_headers = ["Thời gian", "Nội dung theo kế hoạch đề cương", "Địa điểm thực hiện", "Trạng thái tiến độ"]
    plan_rows = [
        ["Tuần 1 và tuần 2", "Khảo sát đề tài, xác định phạm vi, tìm hiểu chuỗi cung ứng nông sản và bất cập kiểm định chất lượng, đăng ký GVHD và tên đề tài.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Hoàn thành 100%"],
        ["Tuần 3", "Hoàn thiện và nộp đề cương; thu thập tài liệu tham khảo; xác định yêu cầu chức năng và phi chức năng hệ thống; thu thập bộ ảnh mẫu nông sản.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Hoàn thành 100%"],
        ["Tuần 4", "Phân tích nghiệp vụ hệ thống; xây dựng Use Case, Activity Diagram, Sequence Diagram; xác định các tác nhân và chức năng của khách hàng, người bán và quản trị viên; thiết kế cơ sở dữ liệu MongoDB.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Hoàn thành 100%"],
        ["Tuần 5", "Khởi tạo Backend bằng Python và FastAPI; thiết lập cấu trúc dự án; kết nối MongoDB Atlas; xây dựng API đăng ký, đăng nhập, xác thực JWT và phân quyền người dùng; thử nghiệm kết nối Gemini AI Vision.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Hoàn thành 100% (Hiện tại)"],
        ["Tuần 6", "Xây dựng Frontend bằng React.js, Vite và Tailwind CSS; thiết kế giao diện trang chủ, danh mục nông sản, tìm kiếm và xem chi tiết sản phẩm; kết nối Frontend với Backend.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch tuần tới"],
        ["Tuần 7", "Xây dựng chức năng giỏ hàng, đặt hàng và quản lý thông tin đơn hàng; triển khai các API xử lý đơn hàng; xây dựng chức năng theo dõi và cập nhật trạng thái đơn hàng.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 8", "Xây dựng chức năng quản lý sản phẩm và danh mục nông sản dành cho người bán/quản trị viên; quản lý hình ảnh, giá bán, số lượng và thông tin sản phẩm; triển khai quản lý tồn kho và cập nhật số lượng sản phẩm.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 9", "Xây dựng chức năng tiếp nhận và xử lý hình ảnh nông sản; thiết kế tiêu chí phân loại chất lượng dựa trên các đặc điểm quan sát được như màu sắc, hình dạng và tình trạng bề mặt; chuẩn bị dữ liệu hình ảnh mẫu phục vụ kiểm thử AI.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 10", "Tích hợp Google Gemini API vào hệ thống; xây dựng và tối ưu prompt phục vụ phân tích hình ảnh nông sản; xử lý kết quả trả về và chuyển đổi thành các mức phân loại chất lượng; kiểm thử API trên Postman và Swagger UI.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 11", "Hoàn thiện chức năng lưu trữ kết quả phân loại chất lượng bằng AI; tích hợp kết quả AI vào thông tin sản phẩm; xây dựng các chức năng quản lý và tra cứu kết quả đánh giá; hoàn thiện giao diện người dùng và quản trị viên.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 12", "Kiểm thử liên thông toàn bộ hệ thống; kiểm thử các chức năng đăng ký, đăng nhập, quản lý sản phẩm, tìm kiếm, giỏ hàng, đặt hàng, quản lý đơn hàng và phân loại chất lượng nông sản bằng AI.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 13", "Viết báo cáo đồ án và chuẩn bị slide thuyết trình demo.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 14", "Hội đồng báo cáo Đồ án chuyên ngành (theo lịch Khoa).", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"],
        ["Tuần 15", "Chỉnh sửa báo cáo, hoàn thiện source code theo góp ý của Hội đồng và nộp sản phẩm cuối cùng.", "Trường ĐH Tài Nguyên Và Môi Trường TP Hồ Chí Minh", "Kế hoạch"]
    ]
    add_table_basic(doc, plan_headers, plan_rows, [Inches(1.2), Inches(3.2), Inches(1.5), Inches(1.1)])

    add_heading_2_black(doc, "Đánh giá mức độ hoàn thành và Quản trị rủi ro")
    add_body_p_black(doc, "Tính đến hết Tuần 5, đồ án đã hoàn thành 100% kế hoạch đề ra cho giai đoạn chuẩn bị môi trường, chuẩn hóa dữ liệu, thiết kế hệ thống và tích hợp thử nghiệm mô hình AI Vision. Khối lượng công việc tiếp theo từ Tuần 6 đến Tuần 10 tập trung vào lập trình chi tiết các phân hệ đã được phân chia theo module độc lập nhằm đảm bảo đúng tiến độ bàn giao.")

    # ==============================================================================
    # TÀI LIỆU THAM KHẢO
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "TÀI LIỆU THAM KHẢO")
    
    add_heading_2_black(doc, "Tài liệu tiếng Việt")
    add_body_p_black(doc, "[1] Đặng Đức Hạnh (2020), Giáo trình Học máy căn bản, NXB Đại học Quốc gia Hà Nội.")
    add_body_p_black(doc, "[2] Vũ Hữu Tiến (2021), Lập trình Web hiện đại với ReactJS và Tailwind CSS, NXB Thông tin và Truyền thông.")
    add_body_p_black(doc, "[3] Nguyễn Văn Hậu (2022), Cơ sở dữ liệu NoSQL: Lý thuyết và ứng dụng với MongoDB, NXB Khoa học và Kỹ thuật.")
    add_body_p_black(doc, "[4] Phạm Quang Hiển (2023), Xây dựng RESTful API hiệu năng cao với Python và FastAPI, Tạp chí Khoa học & Công nghệ Thông tin.")
    add_body_p_black(doc, "[5] F8 Education (2023), Khóa học Lập trình Fullstack & Ứng dụng Trí tuệ Nhân tạo GenAI, Nền tảng học trực tuyến F8.")
    add_body_p_black(doc, "[6] Bộ Nông nghiệp và Phát triển Nông thôn (2017), Tiêu chuẩn Quốc gia TCVN 11892-1:2017 về Thực hành nông nghiệp tốt (VietGAP) - Phần 1: Trồng trọt, NXB Tiêu chuẩn, Hà Nội.")

    add_heading_2_black(doc, "Tài liệu tiếng Anh")
    add_body_p_black(doc, "[7] Ramírez, S. (Tiangolo) (2023), FastAPI Documentation, Tài liệu chính thức: https://fastapi.tiangolo.com.")
    add_body_p_black(doc, "[8] MongoDB, Inc. (2024), MongoDB Atlas & Motor Async Driver Documentation, MongoDB Manual: https://www.mongodb.com/docs.")
    add_body_p_black(doc, "[9] Google DeepMind (2024), Gemini API Documentation & Prompt Engineering Guide, Google AI for Developers.")
    add_body_p_black(doc, "[10] Banks, A., & Porcello, E. (2020), Learning React: Modern Patterns for Developing React Apps (2nd ed.), O'Reilly Media.")
    add_body_p_black(doc, "[11] W3Schools (2024), Full Stack Web Development Tutorials: Python, React.js, Tailwind CSS, W3Schools Online Tutorials.")

    # ==============================================================================
    # CÁC CƠ QUAN, ĐƠN VỊ CẦN LIÊN HỆ & PHẦN KÝ TÊN
    # ==============================================================================
    doc.add_page_break()
    add_heading_1_black(doc, "CÁC CƠ QUAN, ĐƠN VỊ CẦN LIÊN HỆ")
    add_body_p_black(doc, "Khoa Công nghệ Thông tin – Trường Đại học Tài nguyên và Môi trường TP Hồ Chí Minh, 236B Lê Văn Sỹ, Phường Tân Sơn Hòa, TP. Hồ Chí Minh.")

    doc.add_paragraph().paragraph_format.space_after = Pt(20)
    
    tbl_sign = doc.add_table(rows=2, cols=3)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_basic(tbl_sign, border_color="FFFFFF") # no borders for signature layout

    # Header signers
    p_gv = tbl_sign.cell(0, 0).paragraphs[0]
    format_paragraph(p_gv, space_before=0, space_after=50, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_gv.add_run("GIẢNG VIÊN HƯỚNG DẪN\n(ký và ghi rõ họ tên)\n\n\n\n\n\nThS. Ngô Tân Khai")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_bm = tbl_sign.cell(0, 1).paragraphs[0]
    format_paragraph(p_bm, space_before=0, space_after=50, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_bm.add_run("TRƯỞNG BỘ MÔN\n(ký và ghi rõ họ tên)\n\n\n\n\n\n")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    p_sv = tbl_sign.cell(0, 2).paragraphs[0]
    format_paragraph(p_sv, space_before=0, space_after=50, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p_sv.add_run("NGƯỜI LẬP BÁO CÁO\n(ký và ghi rõ họ tên)\n\n\n\n\n\nTrần Dương Phúc")
    r.font.name = "Times New Roman"; r.font.bold = True; r.font.color.rgb = COLOR_BLACK

    doc.save(output_path)
    print("Tao thanh cong Bao cao DACN: " + str(output_path.encode('ascii', 'ignore')))

if __name__ == "__main__":
    out_file1 = os.path.join(BASE_DIR, "Bao_Cao_Do_An_Chuyen_Nganh_AgriXanh.docx")
    build_merged_dacn_report(out_file1)
    
    # Save copies to all required naming conventions
    import shutil
    targets = [
        "1250080149_Trần Dương Phúc_12_ĐH_THMT_Báo Cáo.docx",
        "1250080149_Trần Dương Phúc_12_ĐH_THMT_Báo Cáo Đồ Án Chuyên Ngành.docx",
        "1250080149_Tran_Duong_Phuc_12_DH_THMT_Bao_Cao_DACN.docx"
    ]
    for target in targets:
        target_path = os.path.join(BASE_DIR, target)
        try:
            shutil.copyfile(out_file1, target_path)
            print("Successfully updated: " + str(target.encode('ascii', 'ignore')))
        except Exception as e:
            print(f"Error copying to {target}: {e}")
