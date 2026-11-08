# -*- coding: utf-8 -*-
"""
Script vẽ toàn bộ các sơ đồ UML (Use Case, Activity Swimlane, Sequence) cho AgriXanh
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors
C_PRIMARY = "#1B5E20"     # Deep Green
C_SECONDARY = "#2E7D32"   # Medium Green
C_LIGHT_BG = "#F4FBF5"    # Soft green background
C_LANE_BG = "#FFFFFF"     # White lane
C_GRID = "#E0E0E0"        # Subtle grid
C_BOX_BG = "#FFFFFF"      # White box
C_BOX_BORDER = "#000000"  # Black border for boxes
C_ACTOR = "#283593"       # Deep blue for actors
C_DIAMOND = "#FFFFFF"     # White for decision
C_TEXT = "#000000"

def draw_activity_swimlane(title, lane1_title, lane2_title, lane3_title, steps, filename):
    """
    Vẽ sơ đồ hoạt động dạng Swimlane 3 làn chuẩn theo mẫu
    steps: list of dicts describing nodes and connections
    """
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=180)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Background Grid
    for x in range(0, 101, 2):
        ax.axvline(x, color='#F0F0F0', linewidth=0.5, zorder=0)
    for y in range(0, 101, 2):
        ax.axhline(y, color='#F0F0F0', linewidth=0.5, zorder=0)

    # Outer Frame
    outer_box = patches.Rectangle((2, 2), 96, 94, linewidth=1.5, edgecolor='#000000', facecolor='none', zorder=1)
    ax.add_patch(outer_box)
    
    # Title Header Bar
    title_box = patches.Rectangle((2, 91), 96, 5, linewidth=1, edgecolor='#000000', facecolor='#FFFFFF', zorder=2)
    ax.add_patch(title_box)
    ax.text(50, 93.5, title.upper(), fontsize=11, fontweight='bold', ha='center', va='center', fontname='Arial')

    # Swimlanes Header Bars
    col_w = 96 / 3.0
    lanes = [lane1_title, lane2_title, lane3_title]
    for i, l_text in enumerate(lanes):
        lx = 2 + i * col_w
        # Header cell
        h_box = patches.Rectangle((lx, 86), col_w, 5, linewidth=1, edgecolor='#000000', facecolor='#FFFFFF', zorder=2)
        ax.add_patch(h_box)
        ax.text(lx + col_w/2.0, 88.5, l_text, fontsize=9.5, fontweight='bold', ha='center', va='center', fontname='Arial')
        # Vertical divider line
        if i > 0:
            ax.plot([lx, lx], [2, 91], color='#000000', linewidth=1, zorder=2)

    # Render Nodes and Arrows based on steps
    for s in steps:
        stype = s.get('type', 'box')
        x, y = s['x'], s['y']
        
        if stype == 'start':
            circle = plt.Circle((x, y), 1.5, color='#000000', zorder=5)
            ax.add_patch(circle)
        elif stype == 'end':
            c_out = plt.Circle((x, y), 1.6, color='#000000', fill=False, linewidth=1.5, zorder=5)
            c_in = plt.Circle((x, y), 1.0, color='#000000', zorder=5)
            ax.add_patch(c_out)
            ax.add_patch(c_in)
        elif stype == 'box':
            bw, bh = s.get('w', 24), s.get('h', 6)
            bbox = FancyBboxPatch((x - bw/2.0, y - bh/2.0), bw, bh,
                                  boxstyle="round,pad=0.3,rounding_size=1.2",
                                  ec="#000000", fc="#FFFFFF", linewidth=1.2, zorder=4)
            ax.add_patch(bbox)
            text = s.get('text', '')
            ax.text(x, y, text, fontsize=8.5, ha='center', va='center', fontname='Arial', zorder=5, wrap=True)
        elif stype == 'diamond':
            dw, dh = s.get('w', 12), s.get('h', 5)
            pts = [[x, y + dh/2.0], [x + dw/2.0, y], [x, y - dh/2.0], [x - dw/2.0, y]]
            diamond = Polygon(pts, closed=True, ec="#000000", fc="#FFFFFF", linewidth=1.2, zorder=4)
            ax.add_patch(diamond)
            text = s.get('text', '')
            ax.text(x, y, text, fontsize=8, ha='center', va='center', fontname='Arial', zorder=5)

    # Draw Arrows
    for s in steps:
        for arrow in s.get('arrows', []):
            tx, ty = arrow['to']
            fx, fy = arrow.get('from', (s['x'], s['y']))
            label = arrow.get('label', None)
            
            # Direct arrow or dogleg
            path = arrow.get('path', None)
            if path:
                # polyline
                xs = [fx] + [p[0] for p in path] + [tx]
                ys = [fy] + [p[1] for p in path] + [ty]
                ax.plot(xs, ys, color='#000000', linewidth=1.1, zorder=3)
                # draw arrow head at last segment
                p_last = (xs[-2], ys[-2])
                dx = tx - p_last[0]
                dy = ty - p_last[1]
                ax.annotate('', xy=(tx, ty), xytext=p_last,
                            arrowprops=dict(arrowstyle="-|>", color="#000000", lw=1.1, mutation_scale=10),
                            zorder=3)
            else:
                ax.annotate('', xy=(tx, ty), xytext=(fx, fy),
                            arrowprops=dict(arrowstyle="-|>", color="#000000", lw=1.1, mutation_scale=10),
                            zorder=3)
                
            if label:
                lx = arrow.get('lx', (fx + tx)/2.0)
                ly = arrow.get('ly', (fy + ty)/2.0)
                ax.text(lx, ly, label, fontsize=7.5, ha='center', va='center', fontname='Arial',
                        bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none'), zorder=6)

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Rendered: {filename}")

def draw_sequence_diagram(title, lifelines, messages, filename, alt_boxes=None):
    """
    Vẽ sơ đồ tuần tự chuẩn với Lifelines, messages, và alt boxes
    """
    fig, ax = plt.subplots(figsize=(11.5, 7.8), dpi=180)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Outer frame
    outer_box = patches.Rectangle((2, 2), 96, 94, linewidth=1.5, edgecolor='#000000', facecolor='none', zorder=1)
    ax.add_patch(outer_box)
    
    # Title
    ax.text(50, 93, title.upper(), fontsize=11, fontweight='bold', ha='center', va='center', fontname='Arial')

    # Lifelines
    num_l = len(lifelines)
    span = 92 / (num_l - 1) if num_l > 1 else 50
    xs = [4 + i * span for i in range(num_l)]
    top_y = 86
    bot_y = 6
    
    for i, name in enumerate(lifelines):
        x = xs[i]
        # Box header
        hw = min(span * 0.85, 18)
        hh = 5.5
        h_box = patches.Rectangle((x - hw/2.0, top_y - hh/2.0), hw, hh, linewidth=1.2, edgecolor='#000000', facecolor='#FFFFFF', zorder=4)
        ax.add_patch(h_box)
        ax.text(x, top_y, name, fontsize=8.5, fontweight='bold', ha='center', va='center', fontname='Arial', zorder=5, wrap=True)
        # Dashed lifeline
        ax.plot([x, x], [top_y - hh/2.0, bot_y], color='#000000', linestyle='--', linewidth=1, zorder=2)

    # Alt Boxes
    if alt_boxes:
        for b in alt_boxes:
            bx, by, bw, bh = b['x'], b['y'], b['w'], b['h']
            box_patch = patches.Rectangle((bx, by), bw, bh, linewidth=1.1, edgecolor='#000000', facecolor='none', zorder=2)
            ax.add_patch(box_patch)
            # Tag label
            ax.text(bx + 1, by + bh - 1.5, b.get('tag', 'alt'), fontsize=8, fontweight='bold', ha='left', va='center', fontname='Arial')
            if 'condition' in b:
                ax.text(bx + 1, by + bh - 3.5, b['condition'], fontsize=7.5, ha='left', va='center', fontname='Arial')
            if 'else_y' in b:
                ax.plot([bx, bx + bw], [b['else_y'], b['else_y']], color='#000000', linestyle='--', linewidth=1, zorder=2)
                ax.text(bx + 1, b['else_y'] - 1.5, 'else', fontsize=8, fontweight='bold', ha='left', va='center', fontname='Arial')
                if 'else_condition' in b:
                    ax.text(bx + 1, b['else_y'] - 3.5, b['else_condition'], fontsize=7.5, ha='left', va='center', fontname='Arial')

    # Messages
    for m in messages:
        f_idx, t_idx = m['from'], m['to']
        fx, tx = xs[f_idx], xs[t_idx]
        y = m['y']
        text = m['text']
        is_reply = m.get('reply', False)
        
        style = "-|>"
        ls = "--" if is_reply else "-"
        
        ax.annotate('', xy=(tx, y), xytext=(fx, y),
                    arrowprops=dict(arrowstyle=style, linestyle=ls, color="#000000", lw=1.0, mutation_scale=9),
                    zorder=3)
        
        # Text above line
        mid_x = (fx + tx) / 2.0
        ax.text(mid_x, y + 1.2, text, fontsize=7.5, ha='center', va='bottom', fontname='Arial',
                bbox=dict(boxstyle='square,pad=0.08', fc='white', ec='none'), zorder=4)

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Rendered: {filename}")

def draw_use_case_overall(filename):
    """Vẽ Sơ đồ Use Case tổng thể toàn hệ thống AgriXanh"""
    fig, ax = plt.subplots(figsize=(12, 13), dpi=180)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Boundary box
    sys_box = FancyBboxPatch((16, 2), 68, 95, boxstyle="round,pad=0.5,rounding_size=1.5",
                             ec="#000000", fc="#FAFAFA", lw=1.5, zorder=1)
    ax.add_patch(sys_box)
    ax.text(50, 95, "HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ NÔNG SẢN TÍCH HỢP AI VISION (AGRIXANH)",
            fontsize=10.5, fontweight='bold', ha='center', va='center', fontname='Arial')

    # Actors
    def draw_actor(x, y, label):
        # Head
        head = plt.Circle((x, y + 2.5), 1.2, color='#000000', fill=False, lw=1.2, zorder=5)
        ax.add_patch(head)
        # Body
        ax.plot([x, x], [y + 1.3, y - 1.2], color='#000000', lw=1.2, zorder=5)
        # Arms
        ax.plot([x - 2, x + 2], [y + 0.6, y + 0.6], color='#000000', lw=1.2, zorder=5)
        # Legs
        ax.plot([x, x - 1.8], [y - 1.2, y - 3.2], color='#000000', lw=1.2, zorder=5)
        ax.plot([x, x + 1.8], [y - 1.2, y - 3.2], color='#000000', lw=1.2, zorder=5)
        # Label
        ax.text(x, y - 4.5, label, fontsize=9, fontweight='bold', ha='center', va='top', fontname='Arial')

    # Draw 4 Actors
    draw_actor(8, 70, "Khách hàng\n(Customer)")
    draw_actor(8, 30, "Nhà vườn / Người bán\n(Seller)")
    draw_actor(92, 72, "Quản trị viên\n(Admin)")
    draw_actor(92, 28, "Google Gemini 1.5\n(AI Vision Engine)")

    # Use Cases list
    use_cases = [
        {"id": "UC01", "name": "UC01: Đăng ký tài khoản", "x": 35, "y": 90, "w": 24, "h": 3.8, "c": "#E8F5E9"},
        {"id": "UC02", "name": "UC02: Đăng nhập & Xác thực JWT", "x": 50, "y": 85, "w": 26, "h": 3.8, "c": "#C8E6C9"},
        {"id": "UC03", "name": "UC03: Quản lý hồ sơ & Địa chỉ nhận", "x": 35, "y": 79, "w": 26, "h": 3.8, "c": "#E8F5E9"},
        {"id": "UC04", "name": "UC04: Tìm kiếm & Lọc VietGAP", "x": 35, "y": 73, "w": 25, "h": 3.8, "c": "#E8F5E9"},
        {"id": "UC05", "name": "UC05: Xem chi tiết & Tem AI", "x": 35, "y": 67, "w": 25, "h": 3.8, "c": "#E8F5E9"},
        {"id": "UC06", "name": "UC06: Quản lý giỏ hàng", "x": 35, "y": 61, "w": 22, "h": 3.8, "c": "#E8F5E9"},
        {"id": "UC07", "name": "UC07: Đặt hàng & Thanh toán", "x": 35, "y": 55, "w": 24, "h": 3.8, "c": "#E8F5E9"},
        {"id": "UC08", "name": "UC08: Theo dõi & Lịch sử đơn", "x": 35, "y": 49, "w": 24, "h": 3.8, "c": "#E8F5E9"},
        {"id": "UC09", "name": "UC09: Hủy đơn & Hoàn tồn kho", "x": 35, "y": 43, "w": 25, "h": 3.8, "c": "#E8F5E9"},

        {"id": "UC10", "name": "UC10: Đăng ký gian hàng nhà vườn", "x": 35, "y": 35, "w": 27, "h": 3.8, "c": "#FFF3E0"},
        {"id": "UC11", "name": "UC11: Quản lý sản phẩm đăng bán", "x": 35, "y": 29, "w": 27, "h": 3.8, "c": "#FFF3E0"},
        {"id": "UC12", "name": "UC12: Quản lý kho & Cảnh báo date", "x": 35, "y": 23, "w": 27, "h": 3.8, "c": "#FFF3E0"},
        {"id": "UC13", "name": "UC13: Tiếp nhận & Duyệt giao đơn", "x": 35, "y": 17, "w": 27, "h": 3.8, "c": "#FFF3E0"},

        {"id": "UC14", "name": "UC14: Thẩm định AI trước khi đăng", "x": 55, "y": 32, "w": 27, "h": 3.8, "c": "#E1F5FE"},
        {"id": "UC15", "name": "UC15: Kiểm định ảnh AI độc lập", "x": 48, "y": 40, "w": 25, "h": 3.8, "c": "#E1F5FE"},
        {"id": "UC16", "name": "UC16: Giám sát nhật ký AI Logs", "x": 65, "y": 46, "w": 24, "h": 3.8, "c": "#E1F5FE"},

        {"id": "UC17", "name": "UC17: Tích lũy điểm Loyalty xanh", "x": 48, "y": 11, "w": 25, "h": 3.8, "c": "#F3E5F5"},
        {"id": "UC18", "name": "UC18: Đổi điểm thưởng lấy Voucher", "x": 48, "y": 5.5, "w": 26, "h": 3.8, "c": "#F3E5F5"},

        {"id": "UC19", "name": "UC19: Quản lý người dùng & Gian hàng", "x": 68, "y": 78, "w": 27, "h": 3.8, "c": "#FFEBEE"},
        {"id": "UC20", "name": "UC20: Báo cáo thống kê doanh thu", "x": 68, "y": 66, "w": 26, "h": 3.8, "c": "#FFEBEE"},
    ]

    for u in use_cases:
        ellipse = Ellipse((u['x'], u['y']), u['w'], u['h'], ec="#000000", fc=u['c'], lw=1.1, zorder=3)
        ax.add_patch(ellipse)
        ax.text(u['x'], u['y'], u['name'], fontsize=7.5, ha='center', va='center', fontname='Arial', zorder=4)

    # Actor associations (Lines)
    # Khách hàng lines
    for u_id in ["UC01", "UC02", "UC03", "UC04", "UC05", "UC06", "UC07", "UC08", "UC09", "UC15", "UC17", "UC18"]:
        u = next(x for x in use_cases if x['id'] == u_id)
        ax.plot([10, u['x'] - u['w']/2.0], [70, u['y']], color='#000000', lw=0.8, zorder=2)

    # Nhà vườn lines
    for u_id in ["UC02", "UC10", "UC11", "UC12", "UC13", "UC14"]:
        u = next(x for x in use_cases if x['id'] == u_id)
        ax.plot([10, u['x'] - u['w']/2.0], [30, u['y']], color='#000000', lw=0.8, zorder=2)

    # Admin lines
    for u_id in ["UC02", "UC16", "UC19", "UC20"]:
        u = next(x for x in use_cases if x['id'] == u_id)
        ax.plot([90, u['x'] + u['w']/2.0], [72, u['y']], color='#000000', lw=0.8, zorder=2)

    # AI lines
    for u_id in ["UC14", "UC15"]:
        u = next(x for x in use_cases if x['id'] == u_id)
        ax.plot([90, u['x'] + u['w']/2.0], [28, u['y']], color='#000000', lw=0.8, zorder=2)

    # <<include>> dashed lines
    # UC07 include UC02
    u7 = next(x for x in use_cases if x['id'] == "UC07")
    u2 = next(x for x in use_cases if x['id'] == "UC02")
    ax.annotate('', xy=(u2['x'] - 2, u2['y'] - 1.8), xytext=(u7['x'] + 5, u7['y'] + 1.8),
                arrowprops=dict(arrowstyle="-|>", linestyle="--", color="#000000", lw=0.9), zorder=2)
    ax.text(50, 70, "<<include>>", fontsize=7, ha='center', va='center', fontname='Arial')

    # UC11 include UC14
    u11 = next(x for x in use_cases if x['id'] == "UC11")
    u14 = next(x for x in use_cases if x['id'] == "UC14")
    ax.annotate('', xy=(u14['x'] - u14['w']/2.0, u14['y']), xytext=(u11['x'] + u11['w']/2.0, u11['y']),
                arrowprops=dict(arrowstyle="-|>", linestyle="--", color="#000000", lw=0.9), zorder=2)
    ax.text(48, 31.5, "<<include>>", fontsize=7, ha='center', va='center', fontname='Arial')

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()
    print(f"Rendered: {filename}")

def generate_all():
    print("Generating all diagrams...")
    # 1. Use Case Diagram
    draw_use_case_overall("use_case_overall.png")

    # 2. Activity UC01 - Register
    draw_activity_swimlane(
        title="SƠ ĐỒ HOẠT ĐỘNG: UC-01 - ĐĂNG KÝ TÀI KHOẢN (REGISTER)",
        lane1_title="Người dùng / Tác nhân",
        lane2_title="Web Controller (FastAPI)",
        lane3_title="Cơ sở dữ liệu (MongoDB)",
        steps=[
            {"type": "start", "x": 18, "y": 80, "arrows": [{"to": (18, 72)}]},
            {"type": "box", "x": 18, "y": 68, "text": "1. Điền form đăng ký\n& Bấm 'Đăng ký'", "arrows": [{"to": (50, 68)}]},
            {"type": "box", "x": 50, "y": 68, "text": "2. Tiếp nhận POST /register\n& Validate dữ liệu", "arrows": [{"to": (82, 68)}]},
            {"type": "box", "x": 82, "y": 68, "text": "3. db.users.find_one\n({'email': email})", "arrows": [{"to": (50, 52), "path": [(82, 52)]}]},
            {"type": "diamond", "x": 50, "y": 52, "text": "Email\ntồn tại?", "arrows": [
                {"to": (18, 52), "label": "Có"},
                {"to": (50, 36), "label": "Không"}
            ]},
            {"type": "box", "x": 18, "y": 52, "text": "Báo lỗi 'Email này\nđã được sử dụng'"},
            {"type": "box", "x": 50, "y": 36, "text": "4. Mã hóa mật khẩu\n(Bcrypt Hash)", "arrows": [{"to": (82, 36)}]},
            {"type": "box", "x": 82, "y": 36, "text": "5. db.users.insert_one\n(role=ROLE_CUSTOMER)", "arrows": [{"to": (50, 22), "path": [(82, 22)]}]},
            {"type": "box", "x": 50, "y": 22, "text": "6. Điều hướng trang\nĐăng nhập thành công", "arrows": [{"to": (50, 10)}]},
            {"type": "end", "x": 50, "y": 10}
        ],
        filename="activity_uc01_register.png"
    )

    # 3. Activity UC02 - Login & JWT
    draw_activity_swimlane(
        title="SƠ ĐỒ HOẠT ĐỘNG: UC-02 - ĐĂNG NHẬP HỆ THỐNG & CẤP PHÁT JWT",
        lane1_title="Người dùng / Tác nhân",
        lane2_title="Web Controller (FastAPI)",
        lane3_title="Cơ sở dữ liệu (MongoDB)",
        steps=[
            {"type": "start", "x": 18, "y": 80, "arrows": [{"to": (18, 72)}]},
            {"type": "box", "x": 18, "y": 68, "text": "1. Nhập Email & Mật khẩu,\nbấm 'Đăng nhập'", "arrows": [{"to": (50, 68)}]},
            {"type": "box", "x": 50, "y": 68, "text": "2. Tiếp nhận POST /login\n(UserLogin schema)", "arrows": [{"to": (82, 68)}]},
            {"type": "box", "x": 82, "y": 68, "text": "3. Truy vấn User theo email\n& Lấy hashed_password", "arrows": [{"to": (50, 52), "path": [(82, 52)]}]},
            {"type": "diamond", "x": 50, "y": 52, "text": "Mật khẩu\nhợp lệ?", "arrows": [
                {"to": (18, 52), "label": "Sai"},
                {"to": (50, 36), "label": "Đúng"}
            ]},
            {"type": "box", "x": 18, "y": 52, "text": "Báo lỗi 'Sai email\nhoặc mật khẩu'"},
            {"type": "box", "x": 50, "y": 36, "text": "4. Sinh chuỗi JWT Token\n& Lưu phiên đăng nhập", "arrows": [{"to": (18, 22), "path": [(50, 22)]}]},
            {"type": "box", "x": 18, "y": 22, "text": "5. Điều hướng Dashboard\ntương ứng vai trò (Role)", "arrows": [{"to": (18, 10)}]},
            {"type": "end", "x": 18, "y": 10}
        ],
        filename="activity_uc02_login.png"
    )

    # 4. Activity UC07 - Checkout
    draw_activity_swimlane(
        title="SƠ ĐỒ HOẠT ĐỘNG: UC-07 - ĐẶT HÀNG VÀ THANH TOÁN (CHECKOUT)",
        lane1_title="Khách hàng (Customer)",
        lane2_title="Web Controller (FastAPI)",
        lane3_title="Cơ sở dữ liệu (MongoDB)",
        steps=[
            {"type": "start", "x": 18, "y": 82, "arrows": [{"to": (18, 74)}]},
            {"type": "box", "x": 18, "y": 70, "text": "1. Nhấn 'Tiến hành Đặt hàng'\ntại Giỏ hàng", "arrows": [{"to": (18, 58)}]},
            {"type": "box", "x": 18, "y": 54, "text": "2. Điền địa chỉ nhận hàng,\náp voucher Loyalty & Chọn PTTT", "arrows": [{"to": (18, 42)}]},
            {"type": "box", "x": 18, "y": 38, "text": "3. Nhấn 'Xác nhận Đặt hàng'", "arrows": [{"to": (50, 38)}]},
            {"type": "box", "x": 50, "y": 38, "text": "4. Kiểm tra khóa tồn kho\n(Atomic stock check)", "arrows": [{"to": (82, 38)}]},
            {"type": "box", "x": 82, "y": 38, "text": "5. db.products.find_one\n({_id, stock >= qty})", "arrows": [{"to": (50, 24), "path": [(82, 24)]}]},
            {"type": "diamond", "x": 50, "y": 24, "text": "Đủ tồn\nkho?", "arrows": [
                {"to": (18, 24), "label": "Không"},
                {"to": (82, 12), "label": "Đủ", "path": [(50, 12)]}
            ]},
            {"type": "box", "x": 18, "y": 24, "text": "Báo lỗi 'Sản phẩm hết hàng'\nRollback giỏ hàng"},
            {"type": "box", "x": 82, "y": 12, "text": "6. db.orders.insert_one()\nTrừ stock, khấu trừ điểm Loyalty", "arrows": [{"to": (50, 6), "path": [(82, 6)]}]},
            {"type": "box", "x": 50, "y": 6, "text": "7. Gửi thông báo đặt thành công\nkèm mã đơn hàng", "arrows": [{"to": (18, 6)}]},
            {"type": "end", "x": 18, "y": 6}
        ],
        filename="activity_uc07_checkout.png"
    )

    # 5. Activity UC14 - AI Vision Seller
    draw_activity_swimlane(
        title="SƠ ĐỒ HOẠT ĐỘNG: UC-14 - THẨM ĐỊNH NÔNG SẢN BẰNG AI VISION (SELLER)",
        lane1_title="Nhà vườn (Seller)",
        lane2_title="Web Controller (FastAPI)",
        lane3_title="AI Vision Engine (Gemini 1.5)",
        steps=[
            {"type": "start", "x": 18, "y": 82, "arrows": [{"to": (18, 74)}]},
            {"type": "box", "x": 18, "y": 70, "text": "1. Chụp ảnh nông sản tại vườn\n& Tải lên hệ thống", "arrows": [{"to": (50, 70)}]},
            {"type": "box", "x": 50, "y": 70, "text": "2. Nhận file multipart/form-data\nValidate dung lượng (< 10MB)", "arrows": [{"to": (82, 70)}]},
            {"type": "box", "x": 82, "y": 70, "text": "3. Gemini 1.5 Flash Vision:\nPhân tích màu, cuống, khuyết tật", "arrows": [{"to": (82, 54)}]},
            {"type": "box", "x": 82, "y": 50, "text": "4. Trả về JSON kết quả:\nFreshness Score, Quality Grade", "arrows": [{"to": (50, 50)}]},
            {"type": "diamond", "x": 50, "y": 50, "text": "Điểm >=\n65/100?", "arrows": [
                {"to": (18, 50), "label": "Không"},
                {"to": (50, 32), "label": "Có"}
            ]},
            {"type": "box", "x": 18, "y": 50, "text": "Từ chối niêm yết lên sàn\nKhuyến nghị xử lý dập héo"},
            {"type": "box", "x": 50, "y": 32, "text": "5. Cấp tem 'AI Quality Badge'\n(Loại 1 / Loại 2 / VietGAP)", "arrows": [{"to": (18, 32)}]},
            {"type": "box", "x": 18, "y": 32, "text": "6. Nhập giá bán & Số lượng\nBấm 'Niêm yết sản phẩm'", "arrows": [{"to": (50, 16), "path": [(18, 16)]}]},
            {"type": "box", "x": 50, "y": 16, "text": "7. Lưu vào db.products\n& Ghi nhật ký vào db.ai_logs", "arrows": [{"to": (50, 6)}]},
            {"type": "end", "x": 50, "y": 6}
        ],
        filename="activity_uc14_ai_vision_seller.png"
    )

    # 6. Activity UC15 - AI Check Customer
    draw_activity_swimlane(
        title="SƠ ĐỒ HOẠT ĐỘNG: UC-15 - KHÁCH HÀNG KIỂM ĐỊNH AI ĐỘC LẬP (AI CHECK)",
        lane1_title="Khách hàng (Customer)",
        lane2_title="Web Controller (FastAPI)",
        lane3_title="AI Vision Engine (Gemini 1.5)",
        steps=[
            {"type": "start", "x": 18, "y": 80, "arrows": [{"to": (18, 72)}]},
            {"type": "box", "x": 18, "y": 68, "text": "1. Mở trang AI Check,\ntải ảnh gói nông sản nhận được", "arrows": [{"to": (50, 68)}]},
            {"type": "box", "x": 50, "y": 68, "text": "2. Tiếp nhận POST /ai/analyze\nChuyển luồng sang Gemini API", "arrows": [{"to": (82, 68)}]},
            {"type": "box", "x": 82, "y": 68, "text": "3. Phân tích quang phổ màu sắc,\nchấm điểm độ tươi tế bào", "arrows": [{"to": (82, 52)}]},
            {"type": "box", "x": 82, "y": 50, "text": "4. Trích xuất JSON: Đánh giá vỏ,\ncuống lá, độ giòn và khuyến nghị", "arrows": [{"to": (50, 50)}]},
            {"type": "box", "x": 50, "y": 50, "text": "5. Format dữ liệu trực quan,\ntrả HTTP 200 OK về Client", "arrows": [{"to": (18, 50)}]},
            {"type": "box", "x": 18, "y": 50, "text": "6. Hiển thị tia quét AI Scanning,\nThẻ điểm độ tươi & Lời khuyên", "arrows": [{"to": (18, 32)}]},
            {"type": "box", "x": 18, "y": 28, "text": "7. (Tùy chọn) Khách hàng bấm\n'Thêm vào giỏ hàng' nếu hài lòng", "arrows": [{"to": (18, 14)}]},
            {"type": "end", "x": 18, "y": 14}
        ],
        filename="activity_uc15_ai_check_cust.png"
    )

    # 7. Activity UC18 - Loyalty
    draw_activity_swimlane(
        title="SƠ ĐỒ HOẠT ĐỘNG: UC-18 - ĐỔI ĐIỂM THƯỞNG LOYALTY LẤY VOUCHER",
        lane1_title="Khách hàng (Customer)",
        lane2_title="Web Controller (FastAPI)",
        lane3_title="Cơ sở dữ liệu (MongoDB)",
        steps=[
            {"type": "start", "x": 18, "y": 80, "arrows": [{"to": (18, 72)}]},
            {"type": "box", "x": 18, "y": 68, "text": "1. Vào mục 'Ví điểm thưởng',\nchọn gói Voucher muốn đổi", "arrows": [{"to": (50, 68)}]},
            {"type": "box", "x": 50, "y": 68, "text": "2. Tiếp nhận POST /loyalty/redeem\nKiểm tra số dư điểm khả dụng", "arrows": [{"to": (82, 68)}]},
            {"type": "box", "x": 82, "y": 68, "text": "3. db.loyalty_points.find_one\n({user_id: user_id})", "arrows": [{"to": (50, 52), "path": [(82, 52)]}]},
            {"type": "diamond", "x": 50, "y": 52, "text": "Số điểm >=\nyêu cầu?", "arrows": [
                {"to": (18, 52), "label": "Không"},
                {"to": (82, 36), "label": "Đủ", "path": [(50, 36)]}
            ]},
            {"type": "box", "x": 18, "y": 52, "text": "Báo lỗi 'Số dư điểm không đủ\nđể đổi voucher này'"},
            {"type": "box", "x": 82, "y": 36, "text": "4. Trừ số dư điểm tích lũy\n& Ghi nhật ký lịch sử đổi", "arrows": [{"to": (50, 22), "path": [(82, 22)]}]},
            {"type": "box", "x": 50, "y": 22, "text": "5. Tạo mã Voucher mới\nvào ví voucher của người dùng", "arrows": [{"to": (18, 22)}]},
            {"type": "box", "x": 18, "y": 22, "text": "6. Hiển thị thông báo đổi thành công\nkèm mã Voucher sẵn sàng dùng", "arrows": [{"to": (18, 10)}]},
            {"type": "end", "x": 18, "y": 10}
        ],
        filename="activity_uc18_loyalty.png"
    )

    # 8. Sequence 1 - Checkout
    draw_sequence_diagram(
        title="SƠ ĐỒ TUẦN TỰ: 1. QUY TRÌNH ĐẶT HÀNG, ÁP VOUCHER VÀ TRỪ TỒN KHO TỰ ĐỘNG",
        lifelines=["Khách hàng\n(Customer)", "CartView\n(Checkout UI)", "OrderController\n(FastAPI)", "OrderService\n(Nghiệp vụ)", "InventoryService\n(Kho hàng)", "MongoDB\n(Database)"],
        messages=[
            {"from": 0, "to": 1, "y": 78, "text": "1. Nhấn 'Tiến hành Đặt hàng' tại Giỏ hàng"},
            {"from": 1, "to": 2, "y": 74, "text": "2. POST /api/v1/orders/checkout (OrderCreate)"},
            {"from": 2, "to": 3, "y": 70, "text": "3. create_order(user_id, order_data)"},
            {"from": 3, "to": 4, "y": 66, "text": "4. check_stock_and_reserve(items)"},
            {"from": 4, "to": 5, "y": 62, "text": "5. db.products.find({_id: item.id})"},
            {"from": 5, "to": 4, "y": 58, "text": "6. Trả về stock_quantity khả dụng", "reply": True},
            {"from": 4, "to": 3, "y": 48, "text": "7. [Đủ hàng] Xác nhận kho hợp lệ", "reply": True},
            {"from": 3, "to": 5, "y": 42, "text": "8. db.orders.insert_one(order_doc, status='pending')"},
            {"from": 3, "to": 5, "y": 36, "text": "9. db.products.update_one({$inc: {stock: -qty}})"},
            {"from": 3, "to": 5, "y": 30, "text": "10. db.loyalty.update_one({$inc: {points: -used}})"},
            {"from": 5, "to": 3, "y": 24, "text": "11. Transaction Commit thành công", "reply": True},
            {"from": 3, "to": 2, "y": 18, "text": "12. Trả về OrderResponse DTO", "reply": True},
            {"from": 2, "to": 1, "y": 14, "text": "13. HTTP 201 Created (Order Code, Total)", "reply": True},
            {"from": 1, "to": 0, "y": 10, "text": "14. Hiển thị màn hình 'Đặt hàng thành công'", "reply": True}
        ],
        alt_boxes=[
            {"x": 3, "y": 50, "w": 94, "h": 26, "tag": "alt", "condition": "[Không đủ tồn kho]",
             "else_y": 52, "else_condition": "[Đủ tồn kho khả dụng]"}
        ],
        filename="sequence_01_checkout.png"
    )

    # 9. Sequence 2 - AI Vision Seller
    draw_sequence_diagram(
        title="SƠ ĐỒ TUẦN TỰ: 2. QUY TRÌNH NHÀ VƯỜN THẨM ĐỊNH NÔNG SẢN QUA GEMINI 1.5 FLASH",
        lifelines=["Nhà vườn\n(Seller)", "SellerAIEvaluate\n(Giao diện)", "AIVisionCtrl\n(FastAPI)", "GeminiVisionSrv\n(Google AI)", "ProductService\n(Nghiệp vụ)", "MongoDB\n(Database)"],
        messages=[
            {"from": 0, "to": 1, "y": 80, "text": "1. Chọn ảnh nông sản vừa thu hoạch & Bấm 'Thẩm định AI'"},
            {"from": 1, "to": 2, "y": 74, "text": "2. POST /api/v1/ai/analyze (image bytes, product_name)"},
            {"from": 2, "to": 3, "y": 68, "text": "3. model.generate_content([system_prompt, pil_image])"},
            {"from": 3, "to": 3, "y": 62, "text": "4. Phân tích màu, cuống, vết trầy & tính Freshness Score"},
            {"from": 3, "to": 2, "y": 54, "text": "5. Trả về JSON (Grade, Score, Details, Recs)", "reply": True},
            {"from": 2, "to": 5, "y": 42, "text": "6. db.ai_logs.insert_one(ai_log_record)"},
            {"from": 2, "to": 1, "y": 36, "text": "7. HTTP 200 OK (Cấp tem AI Verified Badge)", "reply": True},
            {"from": 1, "to": 0, "y": 30, "text": "8. Hiển thị kết quả thẩm định trực quan trên màn hình", "reply": True},
            {"from": 0, "to": 1, "y": 24, "text": "9. Điền đơn giá, số lượng tồn kho & Bấm 'Niêm yết bán'"},
            {"from": 1, "to": 4, "y": 18, "text": "10. POST /api/v1/products (ProductCreate + AIQuality)"},
            {"from": 4, "to": 5, "y": 12, "text": "11. db.products.insert_one(product_doc)"},
            {"from": 4, "to": 1, "y": 7, "text": "12. HTTP 201 Created (Nông sản hiển thị trên sàn)", "reply": True}
        ],
        alt_boxes=[
            {"x": 3, "y": 44, "w": 94, "h": 22, "tag": "alt", "condition": "[API Rate Limit / Timeout]",
             "else_y": 47, "else_condition": "[Kích hoạt Rule-based Fallback Engine]"}
        ],
        filename="sequence_02_ai_evaluation.png"
    )

    # 10. Sequence 3 - AI Check Customer
    draw_sequence_diagram(
        title="SƠ ĐỒ TUẦN TỰ: 3. KHÁCH HÀNG TỰ KIỂM ĐỊNH CHẤT LƯỢNG ĐỘC LẬP (AI CHECK)",
        lifelines=["Khách hàng\n(Customer)", "AICheckView\n(Trình duyệt)", "AIVisionCtrl\n(FastAPI)", "GeminiVisionSrv\n(Google AI)", "ProductService\n(Nghiệp vụ)", "MongoDB\n(Database)"],
        messages=[
            {"from": 0, "to": 1, "y": 80, "text": "1. Tải ảnh nông sản mua về để kiểm tra độ tươi"},
            {"from": 1, "to": 2, "y": 74, "text": "2. POST /api/v1/ai/analyze (image, product_name)"},
            {"from": 2, "to": 3, "y": 68, "text": "3. generate_content([prompt, image])"},
            {"from": 3, "to": 2, "y": 58, "text": "4. Trả về kết quả JSON thẩm định chi tiết", "reply": True},
            {"from": 2, "to": 5, "y": 50, "text": "5. db.ai_logs.insert_one(log_entry)"},
            {"from": 2, "to": 1, "y": 42, "text": "6. HTTP 200 OK (Freshness Score, Color, Shape, Surface)", "reply": True},
            {"from": 1, "to": 0, "y": 34, "text": "7. Kích hoạt hiệu ứng quét AI Scanner & Báo điểm tươi", "reply": True},
            {"from": 0, "to": 1, "y": 24, "text": "8. (Tùy chọn) Bấm 'Thêm vào giỏ hàng' nông sản đã test"},
            {"from": 1, "to": 4, "y": 16, "text": "9. POST /api/v1/cart/items (product_id, quantity)"},
            {"from": 4, "to": 1, "y": 8, "text": "10. Cập nhật số lượng giỏ hàng trên Header", "reply": True}
        ],
        filename="sequence_03_ai_check.png"
    )

    # 11. Sequence 4 - Loyalty
    draw_sequence_diagram(
        title="SƠ ĐỒ TUẦN TỰ: 4. QUY TRÌNH TÍCH ĐIỂM TIÊU DÙNG XANH VÀ ĐỔI VOUCHER GIẢM GIÁ",
        lifelines=["Khách hàng\n(Customer)", "AccountView\n(Giao diện Ví)", "LoyaltyCtrl\n(FastAPI)", "LoyaltyService\n(Nghiệp vụ)", "OrderService\n(Đơn hàng)", "MongoDB\n(Database)"],
        messages=[
            {"from": 4, "to": 3, "y": 80, "text": "1. [Đơn hàng Delivered] on_order_completed(order_id)"},
            {"from": 3, "to": 5, "y": 74, "text": "2. db.loyalty.update_one({$inc: {points: +earned}})"},
            {"from": 5, "to": 3, "y": 68, "text": "3. Xác nhận cộng 1% giá trị đơn hàng", "reply": True},
            {"from": 0, "to": 1, "y": 60, "text": "4. Vào mục 'Ví điểm Loyalty' xem số dư & Hạng thẻ"},
            {"from": 1, "to": 2, "y": 54, "text": "5. GET /api/v1/loyalty/balance"},
            {"from": 2, "to": 5, "y": 48, "text": "6. db.loyalty.find_one({user_id: user_id})"},
            {"from": 5, "to": 2, "y": 42, "text": "7. Trả về balance, current_tier, history[]", "reply": True},
            {"from": 2, "to": 1, "y": 36, "text": "8. HTTP 200 OK (Hiển thị điểm & Hạng Vàng/Bạc)", "reply": True},
            {"from": 0, "to": 1, "y": 28, "text": "9. Chọn Voucher 50.000đ & Bấm 'Đổi mã giảm giá'"},
            {"from": 1, "to": 2, "y": 22, "text": "10. POST /api/v1/loyalty/redeem (voucher_id)"},
            {"from": 2, "to": 3, "y": 16, "text": "11. deduct_points_and_issue_voucher(user_id)"},
            {"from": 3, "to": 5, "y": 10, "text": "12. db.users.update({$push: {vouchers: new_voucher}})"},
            {"from": 3, "to": 1, "y": 5, "text": "13. HTTP 200 OK (Mã Voucher sẵn sàng áp dụng)", "reply": True}
        ],
        filename="sequence_04_loyalty.png"
    )

    # 12. Sequence 5 - Auth JWT
    draw_sequence_diagram(
        title="SƠ ĐỒ TUẦN TỰ: 5. QUY TRÌNH ĐĂNG NHẬP VÀ PHÂN QUYỀN TRUY CẬP (JWT & RBAC)",
        lifelines=["Người dùng\n(User)", "LoginView\n(Giao diện)", "AuthController\n(FastAPI)", "SecurityService\n(Bcrypt / JWT)", "UserService\n(Nghiệp vụ)", "MongoDB\n(Database)"],
        messages=[
            {"from": 0, "to": 1, "y": 80, "text": "1. Nhập email, mật khẩu và bấm 'Đăng nhập'"},
            {"from": 1, "to": 2, "y": 74, "text": "2. POST /api/v1/auth/login (UserLogin)"},
            {"from": 2, "to": 4, "y": 68, "text": "3. authenticate_user(email, password)"},
            {"from": 4, "to": 5, "y": 62, "text": "4. db.users.find_one({'email': email})"},
            {"from": 5, "to": 4, "y": 56, "text": "5. Trả về user record & hashed_password", "reply": True},
            {"from": 4, "to": 3, "y": 48, "text": "6. verify_password(plain_pwd, hashed_pwd)"},
            {"from": 3, "to": 4, "y": 42, "text": "7. [Hợp lệ] Mật khẩu chính xác", "reply": True},
            {"from": 4, "to": 3, "y": 34, "text": "8. create_access_token(data={'sub': email, 'role': role})"},
            {"from": 3, "to": 4, "y": 28, "text": "9. Trả về chuỗi JWT Token có thời hạn", "reply": True},
            {"from": 4, "to": 2, "y": 20, "text": "10. Trả về Token DTO kèm UserProfile", "reply": True},
            {"from": 2, "to": 1, "y": 14, "text": "11. HTTP 200 OK (access_token, token_type, user)", "reply": True},
            {"from": 1, "to": 0, "y": 8, "text": "12. Lưu token LocalStorage & Chuyển hướng Dashboard", "reply": True}
        ],
        alt_boxes=[
            {"x": 3, "y": 38, "w": 94, "h": 22, "tag": "alt", "condition": "[Sai mật khẩu]",
             "else_y": 40, "else_condition": "[Mật khẩu hợp lệ]"}
        ],
        filename="sequence_05_auth_jwt.png"
    )

    print("All diagrams generated successfully!")

if __name__ == "__main__":
    generate_all()
