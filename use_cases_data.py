# -*- coding: utf-8 -*-
"""
Dữ liệu đặc tả chi tiết 20 Use Cases cho hệ thống AgriXanh
"""

AGRIXANH_USE_CASES = [
    {
        "id": "UC-01",
        "name": "Đăng ký tài khoản",
        "actor": "Khách hàng, Nhà vườn (Người bán)",
        "desc": "Cho phép người dùng mới tạo tài khoản trên sàn AgriXanh để mua sắm nông sản sạch hoặc đăng ký làm đối tác nhà vườn cung cấp nông sản.",
        "pre": "Người dùng chưa đăng nhập vào hệ thống.",
        "post": "Bản ghi người dùng mới được tạo trong Collection 'users' của MongoDB với vai trò ROLE_CUSTOMER hoặc ROLE_SELLER, mật khẩu được băm bằng Bcrypt, ví điểm Loyalty được khởi tạo.",
        "basic": [
            ("Bước 1 - 2", "1. Tại giao diện chính, người dùng chọn 'Đăng ký' và chọn loại tài khoản (Khách hàng hoặc Nhà vườn).", "2. Hệ thống hiển thị form đăng ký (Họ tên, Email, Số điện thoại, Mật khẩu, Xác nhận mật khẩu, Địa chỉ)."),
            ("Bước 3 - 4", "3. Người dùng điền đầy đủ các trường thông tin hợp lệ và nhấn nút 'Đăng ký tài khoản'.", "4. Backend FastAPI (AuthController) tiếp nhận POST /api/v1/auth/register, kiểm tra trùng lặp email trong CSDL MongoDB."),
            ("Bước 5 - 6", "5. Người dùng nhận thông báo thành công và chuyển hướng đến trang Đăng nhập.", "6. Hệ thống mã hóa mật khẩu bằng Bcrypt (12 rounds), lưu document vào db.users, khởi tạo ví điểm db.loyalty_points và trả về mã HTTP 201 Created.")
        ],
        "alt": [
            ("Email đã tồn tại", "4.a.1 Người dùng nhập email khác hoặc chọn 'Quên mật khẩu'.", "4.a.2 MongoDB phát hiện email đã tồn tại (index unique); hệ thống giữ nguyên form và báo lỗi: 'Email này đã được sử dụng trên AgriXanh'."),
            ("Mật khẩu không khớp", "4.b.1 Người dùng nhập lại mật khẩu xác nhận chính xác.", "4.b.2 Pydantic validator phát hiện password != confirm_password hoặc độ dài < 8 ký tự; hệ thống báo lỗi đỏ tại trường mật khẩu.")
        ]
    },
    {
        "id": "UC-02",
        "name": "Đăng nhập hệ thống & Cấp phát JWT",
        "actor": "Khách hàng, Nhà vườn, Quản trị viên (Admin)",
        "desc": "Xác thực danh tính người dùng và cấp phát mã JSON Web Token (JWT) kèm vai trò tương ứng để bảo mật các phiên làm việc tiếp theo.",
        "pre": "Tài khoản người dùng đã được kích hoạt trong CSDL.",
        "post": "Hệ thống cấp token JWT có thời hạn 7 ngày, lưu vào LocalStorage trình duyệt và điều hướng vào Dashboard phân hệ tương ứng.",
        "basic": [
            ("Bước 1 - 2", "1. Người dùng chọn 'Đăng nhập' trên Header.", "2. Hệ thống hiển thị modal/trang đăng nhập gồm Email và Mật khẩu."),
            ("Bước 3 - 4", "3. Người dùng nhập thông tin xác thực và bấm nút 'Đăng nhập'.", "4. Backend tiếp nhận POST /api/v1/auth/login, đối chiếu email trong db.users, dùng passlib.verify kiểm tra băm mật khẩu."),
            ("Bước 5 - 6", "5. Người dùng được chuyển hướng vào giao diện tương ứng với vai trò.", "6. Mật khẩu đúng: Hệ thống sinh JWT Token chứa payload (user_id, role, sub), trả về HTTP 200 OK. Frontend lưu token và điều hướng: Admin -> /admin, Seller -> /seller, Customer -> Trang chủ.")
        ],
        "alt": [
            ("Sai thông tin xác thực", "4.a.1 Người dùng kiểm tra lại email/mật khẩu và bấm đăng nhập lại.", "4.a.2 Mật khẩu sai hoặc email không tồn tại; hệ thống trả mã HTTP 401 Unauthorized và báo lỗi: 'Email hoặc mật khẩu không chính xác'."),
            ("Tài khoản bị khóa", "4.b.1 Người dùng liên hệ hotline hỗ trợ kỹ thuật của sàn.", "4.b.2 Hệ thống phát hiện cờ is_active = False (do vi phạm tiêu chuẩn nông sản); từ chối đăng nhập và báo: 'Tài khoản của bạn đã bị tạm khóa'.")
        ]
    },
    {
        "id": "UC-03",
        "name": "Quản lý hồ sơ cá nhân & Địa chỉ nhận hàng",
        "actor": "Khách hàng",
        "desc": "Cho phép khách hàng xem và cập nhật thông tin cá nhân, số điện thoại liên lạc, và danh sách địa chỉ giao hàng để thuận tiện khi đặt nông sản tươi.",
        "pre": "Khách hàng đã đăng nhập thành công vào hệ thống.",
        "post": "Dữ liệu hồ sơ và địa chỉ mặc định được cập nhật trong CSDL MongoDB.",
        "basic": [
            ("Bước 1 - 2", "1. Khách hàng vào mục 'Tài khoản của tôi' (/account).", "2. Hệ thống gọi GET /api/v1/auth/me và hiển thị thông tin: Họ tên, Email, Số điện thoại, Địa chỉ nhận hàng mặc định, Hạng thành viên Loyalty."),
            ("Bước 3 - 4", "3. Khách hàng chỉnh sửa số điện thoại, địa chỉ cụ thể (Số nhà, Phường/Xã, Quận/Huyện, Tỉnh/TP) và nhấn 'Lưu thay đổi'.", "4. Backend gọi PUT /api/v1/auth/profile, kiểm tra định dạng dữ liệu và cập nhật document trong db.users."),
            ("Bước 5", "5. Khách hàng nhận thông báo xác nhận thành công trên giao diện.", "5. Hệ thống hiển thị thông báo Toast: 'Cập nhật hồ sơ thành công'.")
        ],
        "alt": [
            ("Số điện thoại sai chuẩn", "4.a.1 Khách hàng nhập lại số điện thoại 10 chữ số.", "4.a.2 Regex validator phát hiện số điện thoại không hợp lệ (không bắt đầu bằng 0 hoặc không đủ 10 số); hệ thống báo lỗi không cho phép lưu.")
        ]
    },
    {
        "id": "UC-04",
        "name": "Tìm kiếm và lọc nông sản VietGAP",
        "actor": "Khách hàng",
        "desc": "Tìm kiếm nông sản theo từ khóa hoặc bộ lọc đa tiêu chí: Danh mục (Rau lá, Củ quả, Trái cây), Khoảng giá, Nơi xuất xứ (Đà Lạt, Mộc Châu...), Chứng nhận (VietGAP, OCOP, Hữu cơ) và Tem xếp hạng AI.",
        "pre": "Không yêu cầu.",
        "post": "Danh sách nông sản thỏa mãn bộ lọc được kết xuất trực quan kèm phân trang trên giao diện.",
        "basic": [
            ("Bước 1 - 2", "1. Khách hàng nhập từ khóa tìm kiếm trên thanh tìm kiếm hoặc chọn danh mục rau củ trên menu navigation.", "2. Frontend gửi request GET /api/v1/products kèm các query parameters (category, search, min_price, max_price, cert)."),
            ("Bước 3 - 4", "3. Khách hàng tích chọn các tiêu chí lọc: 'Chứng nhận VietGAP', phân hạng 'AI Loại 1 (Xuất sắc)', sắp xếp theo 'Giá tăng dần'.", "4. Backend FastAPI thực thi truy vấn MongoDB với $match và $text search, áp dụng phân trang (skip, limit)."),
            ("Bước 5", "5. Khách hàng duyệt danh sách các thẻ sản phẩm nông sản khớp tiêu chí kèm ảnh sắc nét và tem chất lượng AI.", "5. Hệ thống trả về mảng JSON sản phẩm kèm tổng số lượng (total_count) và render giao diện trong thời gian dưới 100ms.")
        ],
        "alt": [
            ("Không tìm thấy nông sản phù hợp", "4.a.1 Khách hàng bấm 'Xóa bộ lọc' hoặc nhập từ khóa tìm kiếm khác.", "4.a.2 Không có sản phẩm nào khớp điều kiện; hệ thống hiển thị thông báo: 'Không tìm thấy nông sản phù hợp' và gợi ý các mặt hàng rau củ sạch bán chạy nhất.")
        ]
    },
    {
        "id": "UC-05",
        "name": "Xem chi tiết nông sản & Tem chất lượng AI",
        "actor": "Khách hàng",
        "desc": "Xem toàn bộ hình ảnh độ phân giải cao, giá bán niêm yết, quy cách đóng gói, thông tin trang trại canh tác và đặc biệt là thẻ kết quả phân tích chất lượng AI (Điểm độ tươi Freshness Score, nhận định màu sắc vỏ, cuống và khuyết tật).",
        "pre": "Khách hàng chọn một sản phẩm từ trang danh mục hoặc từ kết quả tìm kiếm.",
        "post": "Trang chi tiết nông sản (/products/{id}) được tải đầy đủ thông tin.",
        "basic": [
            ("Bước 1 - 2", "1. Khách hàng nhấp vào thẻ của một nông sản (Ví dụ: Cà chua cherry Đà Lạt).", "2. Hệ thống gọi GET /api/v1/products/{id} truy xuất dữ liệu từ db.products và db.ai_logs."),
            ("Bước 3 - 4", "3. Khách hàng quan sát: Hình ảnh thực tế, giá/kg, số lượng còn lại trong kho, chứng chỉ VietGAP, nguồn gốc trang trại.", "4. Hệ thống hiển thị Khối Tem Kiểm Định AI (AI Quality Badge): Điểm số tươi mới (96/100), Màu sắc vỏ bóng đỏ mọng, cuống đài tươi xanh, khuyến nghị bảo quản."),
            ("Bước 5", "5. Khách hàng chọn số lượng cần mua (kg/hộp) và chọn 'Thêm vào giỏ hàng' hoặc 'Mua ngay'.", "5. Hệ thống đồng thời gợi ý các loại rau củ thường được mua kèm theo đơn.")
        ],
        "alt": [
            ("Sản phẩm đã hết hàng", "3.a.1 Khách hàng bấm 'Nhận thông báo khi có hàng' hoặc chọn mặt hàng khác.", "3.a.2 Số lượng tồn kho bằng 0; hệ thống hiển thị nhãn 'Tạm hết hàng' màu đỏ và làm mờ nút Thêm giỏ hàng.")
        ]
    },
    {
        "id": "UC-06",
        "name": "Quản lý giỏ hàng",
        "actor": "Khách hàng",
        "desc": "Cho phép thêm nông sản vào giỏ hàng, tùy chỉnh tăng giảm khối lượng đặt mua (kg), xóa mặt hàng và tự động cập nhật tạm tính tổng tiền theo thời gian thực.",
        "pre": "Khách hàng đang ở trang danh mục hoặc trang chi tiết nông sản.",
        "post": "Giỏ hàng trong bộ nhớ Client (LocalStorage / State) và CSDL được đồng bộ hóa.",
        "basic": [
            ("Bước 1 - 2", "1. Tại trang sản phẩm, khách hàng chọn số lượng (ví dụ: 2 kg) và nhấn 'Thêm vào giỏ hàng'.", "2. Hệ thống kiểm tra số lượng tồn kho khả dụng của sản phẩm đó. Nếu đủ hàng, thêm vào giỏ và cập nhật số lượng trên icon Giỏ hàng."),
            ("Bước 3 - 4", "3. Khách hàng truy cập trang Giỏ hàng (/cart) để rà soát danh sách: đơn giá, số lượng, quy đổi thành tiền.", "4. Khách hàng bấm nút '+' hoặc '-' để điều chỉnh số lượng; hệ thống tự động tính toán lại tổng tiền hàng (Subtotal)."),
            ("Bước 5", "5. Khách hàng nhấn nút 'Tiến hành Đặt hàng'.", "5. Hệ thống chuyển hướng sang màn hình thanh toán Checkout.")
        ],
        "alt": [
            ("Số lượng vượt tồn kho thực tế", "2.a.1 Khách hàng giảm số lượng đặt mua bằng số lượng tồn kho còn lại.", "2.a.2 Số lượng chọn mua lớn hơn số lượng tồn kho thực tế; hệ thống báo Toast: 'Số lượng trong kho không đủ (chỉ còn X kg)'."),
            ("Giỏ hàng rỗng", "3.a.1 Khách hàng bấm nút 'Khám phá nông sản ngay'.", "3.a.2 Giỏ hàng chưa có sản phẩm; hệ thống hiển thị hình minh họa giỏ rỗng và điều hướng về trang danh mục sản phẩm.")
        ]
    },
    {
        "id": "UC-07",
        "name": "Đặt hàng và Thanh toán",
        "actor": "Khách hàng",
        "desc": "Xác nhận địa chỉ nhận rau củ quả tươi, chọn phương thức thanh toán (COD hoặc chuyển khoản ngân hàng/ví điện tử), áp dụng điểm thưởng Loyalty để trừ tiền trực tiếp và hoàn tất đơn hàng.",
        "pre": "Khách hàng đã đăng nhập và giỏ hàng có ít nhất 01 sản phẩm.",
        "post": "Đơn hàng mới được tạo với trạng thái 'pending' trong db.orders, số lượng nông sản trong kho bị trừ ngay lập tức, điểm thưởng được khấu trừ.",
        "basic": [
            ("Bước 1 - 2", "1. Tại giỏ hàng, khách hàng nhấn 'Tiến hành Đặt hàng'.", "2. Hệ thống chuyển sang màn hình Checkout, hiển thị tóm tắt giỏ hàng, tiền ship và số dư điểm Loyalty hiện có."),
            ("Bước 3 - 4", "3. Khách hàng kiểm tra địa chỉ nhận hàng, số điện thoại, nhập số điểm thưởng muốn dùng (1 điểm = 100đ giảm giá), chọn hình thức thanh toán (COD / Chuyển khoản QR).", "4. Khách hàng nhấn nút 'Xác nhận Đặt hàng'."),
            ("Bước 5 - 6", "5. Khách hàng nhận thông báo đặt thành công kèm Mã đơn hàng và hướng dẫn nhận hàng.", "6. Backend thực hiện giao dịch (Atomic Transaction): Khóa dòng kiểm tra tồn kho -> Ghi document vào db.orders -> Khấu trừ stock_quantity trong db.products -> Khấu trừ số điểm đã dùng trong db.loyalty_points -> Xóa giỏ hàng -> Gửi thông báo đến Nhà vườn.")
        ],
        "alt": [
            ("Sản phẩm hết hàng trong lúc Checkout", "4.a.1 Khách hàng quay lại giỏ hàng cập nhật lại danh mục.", "4.a.2 Trong quá trình thanh toán, có khách hàng khác đã mua hết tồn kho; hệ thống rollback giao dịch và báo: 'Rất tiếc, sản phẩm X vừa hết hàng'."),
            ("Điểm thưởng dùng vượt quá số dư", "3.a.1 Khách hàng nhập lại số điểm thưởng hợp lệ.", "3.a.2 Số điểm nhập vào lớn hơn available_points; hệ thống báo lỗi: 'Số điểm sử dụng vượt quá số dư hiện có'.")
        ]
    },
    {
        "id": "UC-08",
        "name": "Theo dõi trạng thái và Lịch sử đơn hàng",
        "actor": "Khách hàng",
        "desc": "Cho phép khách hàng theo dõi trực quan vòng đời đơn hàng nông sản qua 5 trạng thái (Chờ xác nhận, Chuẩn bị hàng, Đang vận chuyển, Giao thành công, Đã hủy) và xem lại chi tiết các lần mua hàng trước đó.",
        "pre": "Khách hàng đã đăng nhập vào hệ thống.",
        "post": "Toàn bộ tiến trình và lịch sử giao dịch được hiển thị chính xác theo thời gian thực.",
        "basic": [
            ("Bước 1 - 2", "1. Khách hàng truy cập mục 'Đơn hàng của tôi' (/account?tab=orders).", "2. Hệ thống gọi GET /api/v1/orders/my-orders, truy vấn CSDL MongoDB lấy danh sách đơn của user_id sắp xếp mới nhất lên đầu."),
            ("Bước 3 - 4", "3. Khách hàng bấm 'Xem chi tiết' một đơn hàng cụ thể.", "4. Hệ thống hiển thị thanh tiến trình (Order Tracker), danh sách rau củ đã mua, tổng tiền, số điểm Loyalty được tích lũy (1% giá trị đơn)."),
            ("Bước 5", "5. Khách hàng có thể bấm 'Hủy đơn hàng' nếu đơn hàng vẫn đang ở trạng thái 'pending'.", "5. Hệ thống cập nhật trạng thái đơn thành 'cancelled', hoàn trả số lượng nông sản về kho hàng và hoàn lại điểm thưởng.")
        ],
        "alt": [
            ("Hủy đơn không hợp lệ", "5.a.1 Khách hàng xem tiến trình vận chuyển và liên hệ nhà vườn nếu cần hỗ trợ.", "5.a.2 Đơn hàng đã chuyển sang 'shipping' (nhà vườn đã gửi cho đơn vị vận chuyển mát); hệ thống ẩn nút Hủy và báo: 'Đơn hàng đang trên đường giao, không thể hủy tự động'.")
        ]
    },
    {
        "id": "UC-09",
        "name": "Hủy đơn hàng và Hoàn tồn kho",
        "actor": "Khách hàng, Quản trị viên",
        "desc": "Thực hiện hủy đơn hàng khi khách đổi ý hoặc có sự cố, tự động phục hồi số lượng tồn kho của nông sản và hoàn trả điểm thưởng đã sử dụng.",
        "pre": "Đơn hàng đang ở trạng thái 'pending' hoặc 'confirmed' (chưa bàn giao vận chuyển).",
        "post": "Trạng thái đơn đổi thành 'cancelled', tồn kho trong db.products được cộng hoàn lại, điểm loyalty được khôi phục.",
        "basic": [
            ("Bước 1 - 2", "1. Tại màn hình chi tiết đơn hàng, khách hàng bấm nút 'Hủy đơn hàng' và chọn lý do hủy.", "2. Frontend gửi yêu cầu PUT /api/v1/orders/{id}/cancel kèm lý do hủy."),
            ("Bước 3 - 4", "3. Backend kiểm tra điều kiện trạng thái đơn hàng.", "4. Hệ thống thực hiện hoàn kho: Với mỗi mặt hàng trong đơn, thực hiện $inc: {stock_quantity: +item.qty} trong db.products."),
            ("Bước 5 - 6", "5. Khách hàng nhận thông báo hủy đơn thành công.", "6. Hệ thống cộng lại số điểm Loyalty đã dùng vào db.loyalty_points, cập nhật order_status = 'cancelled' và gửi thông báo cho Nhà vườn.")
        ],
        "alt": [
            ("Đơn đã xuất kho vận chuyển", "2.a.1 Khách hàng gọi điện hotline hỗ trợ xử lý đặc biệt.", "2.a.2 Trạng thái đơn là 'shipping'; hệ thống từ chối hủy và trả mã HTTP 400 Bad Request.")
        ]
    },
    {
        "id": "UC-10",
        "name": "Đăng ký gian hàng & Thông tin trang trại",
        "actor": "Nhà vườn / Người bán (Seller)",
        "desc": "Cho phép chủ trang trại hoặc hợp tác xã đăng ký thông tin vùng trồng, vị trí địa lý, các chứng nhận tiêu chuẩn nông nghiệp (VietGAP, GlobalGAP, OCOP) để trở thành đối tác bán hàng chính thức.",
        "pre": "Tài khoản đã đăng ký vai trò Seller hoặc Customer muốn nâng cấp lên Seller.",
        "post": "Hồ sơ gian hàng được tạo và lưu ở trạng thái chờ Admin phê duyệt.",
        "basic": [
            ("Bước 1 - 2", "1. Người dùng chọn 'Kênh Nhà vườn / Trở thành Người bán' trên thanh điều hướng.", "2. Hệ thống hiển thị form đăng ký gian hàng (Tên trang trại, Chủ hộ kinh doanh, Địa chỉ vùng trồng, Tải ảnh giấy chứng nhận VietGAP/OCOP)."),
            ("Bước 3 - 4", "3. Nhà vườn điền thông tin và đính kèm bản scan chứng nhận, nhấn 'Gửi hồ sơ đăng ký'.", "4. Backend lưu thông tin vào db.seller_profiles với trạng thái 'pending_approval' và gửi thông báo tới Admin."),
            ("Bước 5", "5. Nhà vườn nhận thông báo hồ sơ đang được ban quản trị xét duyệt trong vòng 24 giờ.", "5. Hệ thống hiển thị trạng thái hồ sơ trên giao diện cá nhân.")
        ],
        "alt": [
            ("Thiếu chứng nhận bắt buộc", "3.a.1 Nhà vườn bổ sung file đính kèm chứng nhận vùng trồng an toàn.", "3.a.2 Bỏ trống file chứng nhận; hệ thống cảnh báo: 'Vui lòng đính kèm chứng nhận VietGAP hoặc cam kết an toàn thực phẩm để đảm bảo tiêu chuẩn sàn'.")
        ]
    },
    {
        "id": "UC-11",
        "name": "Quản lý sản phẩm đăng bán & Bảng giá",
        "actor": "Nhà vườn (Seller)",
        "desc": "Cho phép nhà vườn thêm mới mặt hàng nông sản (đã được thẩm định qua AI), cập nhật mô tả, điều chỉnh giá bán theo biến động thị trường và cập nhật số lượng thu hoạch hàng ngày.",
        "pre": "Đăng nhập với quyền ROLE_SELLER và nông sản đã vượt qua bước kiểm định AI (UC-14).",
        "post": "Thông tin sản phẩm trong db.products được cập nhật và hiển thị đồng bộ trên sàn.",
        "basic": [
            ("Bước 1 - 2", "1. Nhà vườn truy cập Kênh Người bán -> 'Danh sách sản phẩm' (/seller/products).", "2. Hệ thống hiển thị bảng danh sách các mặt hàng nông sản của nhà vườn kèm số lượng tồn và tem AI."),
            ("Bước 3 - 4", "3. Nhà vườn bấm 'Chỉnh sửa' hoặc 'Thêm nông sản mới', cập nhật giá bán niêm yết (VNĐ/kg) và số lượng tồn mới thu hoạch.", "4. Backend FastAPI tiếp nhận PUT /api/v1/products/{id}, kiểm tra quyền sở hữu seller_id và cập nhật document."),
            ("Bước 5", "5. Nhà vườn nhận thông báo cập nhật thành công.", "5. Hệ thống lưu thay đổi và đồng bộ giá mới lên giao diện mua sắm của Khách hàng tức thì.")
        ],
        "alt": [
            ("Giá bán âm hoặc không hợp lệ", "3.a.1 Nhà vườn chỉnh sửa lại mức giá dương hợp lý.", "3.a.2 Pydantic schema phát hiện price <= 0; hệ thống báo lỗi không cho phép lưu.")
        ]
    },
    {
        "id": "UC-12",
        "name": "Quản lý kho hàng & Cảnh báo date nông sản",
        "actor": "Nhà vườn (Seller)",
        "desc": "Theo dõi số lượng tồn kho thực tế, hạn sử dụng tối ưu của rau củ quả tươi, nhận cảnh báo tự động khi nông sản cận date để kích hoạt giảm giá xả hàng, tránh lãng phí hư hỏng.",
        "pre": "Đăng nhập với quyền ROLE_SELLER.",
        "post": "Bảng db.inventory được cập nhật; sản phẩm cận date được gắn nhãn Flash Sale nếu người bán đồng ý.",
        "basic": [
            ("Bước 1 - 2", "1. Nhà vườn truy cập mục 'Quản lý kho nông sản' (/seller/inventory).", "2. Hệ thống hiển thị danh sách tồn kho, ngày thu hoạch, hạn dùng tối ưu (Best before date), ngưỡng cảnh báo tồn tối thiểu."),
            ("Bước 3 - 4", "3. Hệ thống quét tự động: Nếu ngày hiện tại chỉ còn cách expiry_date <= 2 ngày, hiển thị thẻ cảnh báo màu cam 'Cận date' kèm nút 'Kích hoạt Flash Sale giảm 30%'.", "4. Nhà vườn chọn các lô hàng cận date và bấm 'Áp dụng giảm giá xả hàng'."),
            ("Bước 5", "5. Nhà vườn quan sát giá bán mới được cập nhật trên sàn.", "5. Backend cập nhật giá khuyến mãi và đưa sản phẩm lên mục 'Nông sản giải cứu trong ngày' tại trang chủ.")
        ],
        "alt": [
            ("Nông sản đã quá hạn sử dụng", "3.a.1 Nhà vườn xác nhận tiêu hủy lô hàng hỏng.", "3.a.2 Hệ thống phát hiện ngày hiện tại > expiry_date; tự động chuyển trạng thái sản phẩm thành 'Ẩn khỏi sàn' và cảnh báo nhà vườn thu hồi sản phẩm.")
        ]
    },
    {
        "id": "UC-13",
        "name": "Tiếp nhận, xác nhận đóng gói và duyệt đơn hàng",
        "actor": "Nhà vườn (Seller)",
        "desc": "Nhà vườn theo dõi các đơn hàng mới từ khách, kiểm tra khả năng đáp ứng, xác nhận đơn, thực hiện đóng gói theo tiêu chuẩn bảo quản nông sản và bàn giao cho đơn vị vận chuyển.",
        "pre": "Đăng nhập với quyền ROLE_SELLER và có đơn hàng mới phát sinh.",
        "post": "Trạng thái đơn hàng chuyển từ 'pending' sang 'confirmed' và 'shipping'.",
        "basic": [
            ("Bước 1 - 2", "1. Nhà vườn vào mục 'Quản lý đơn hàng' (/seller/orders).", "2. Hệ thống hiển thị danh sách đơn phân loại: Chờ xác nhận, Đang chuẩn bị hàng, Đang giao, Đã hoàn thành."),
            ("Bước 3 - 4", "3. Nhà vườn bấm vào đơn hàng 'Chờ xác nhận', kiểm tra khối lượng rau củ khách đặt và địa chỉ giao hàng.", "4. Nhà vườn bấm nút 'Xác nhận đơn & Chuẩn bị đóng gói'."),
            ("Bước 5 - 6", "5. Sau khi đóng gói thùng xốp/hộp carton thoáng khí, nhà vườn bấm 'Bàn giao vận chuyển'.", "6. Backend gọi PUT /api/v1/orders/{id}/status cập nhật trạng thái 'shipping', tự động gửi email/thông báo thông báo cho Khách hàng.")
        ],
        "alt": [
            ("Không đủ hàng do thời tiết thất thường", "4.a.1 Nhà vườn bấm 'Từ chối đơn' kèm lý do cụ thể và liên hệ khách.", "4.a.2 Hệ thống cập nhật trạng thái đơn thành 'cancelled', tự động hoàn tiền/điểm cho khách hàng và hoàn trả các sản phẩm khác.")
        ]
    },
    {
        "id": "UC-14",
        "name": "Thẩm định chất lượng nông sản qua AI Vision (Seller)",
        "actor": "Nhà vườn (Seller), Google Gemini 1.5 Flash (AI Engine)",
        "desc": "Quy trình cốt lõi mang tính đột phá của hệ thống: Nhà vườn chụp ảnh nông sản thực tế vừa thu hoạch, AI Vision tự động phân tích đa tiêu chí ngoại quan (độ chín, màu sắc, độ tươi cuống lá, khuyết tật) và chấm điểm tươi mới (Freshness Score). Sản phẩm đạt chuẩn mới được cấp tem AI Verified để đăng bán.",
        "pre": "Nhà vườn đăng nhập Kênh Người bán và truy cập chức năng 'Thẩm định AI & Đăng sản phẩm' (/seller/ai-evaluate).",
        "post": "Kết quả thẩm định được trả về dạng JSON trực quan; nếu đạt chuẩn (Score >= 65), sản phẩm được cấp tem 'AI Quality Badge' và ghi bản ghi vào db.ai_logs.",
        "basic": [
            ("Bước 1 - 2", "1. Nhà vườn chụp ảnh hoặc tải file ảnh nông sản thực tế (định dạng JPG/PNG), nhập tên nông sản (Ví dụ: Cà chua cherry Đà Lạt).", "2. Frontend gửi request POST /api/v1/ai/analyze (multipart/form-data) đến Backend FastAPI."),
            ("Bước 3 - 4", "3. Backend nhận luồng nhị phân của ảnh, nạp vào thư viện PIL.Image, gắn kèm System Prompt Chuyên gia thẩm định VietGAP và gọi Google Gemini 1.5 Flash API.", "4. Mô hình Gemini Vision phân tích quang phổ màu sắc, hình thái và cấu trúc bề mặt, trả về chuỗi JSON chuẩn chứa: quality_grade, freshness_score, color_assessment, shape_assessment, surface_condition, recommendations."),
            ("Bước 5 - 6", "5. Nhà vườn quan sát kết quả trực quan: Điểm tươi mới 96/100, Phân hạng Loại 1 (Xuất sắc), Vỏ bóng đỏ mọng không vết nám, Cuống đài xanh tươi.", "6. Hệ thống lưu kết quả vào db.ai_logs và tự động điền sẵn thuộc tính ai_quality = 'Loại 1 (Xuất sắc)' vào form đăng sản phẩm."),
            ("Bước 7", "7. Nhà vườn nhập giá bán, số lượng và bấm 'Đăng bán nông sản'.", "7. Nông sản chính thức xuất hiện trên sàn với Tem AI chứng nhận chất lượng độc lập.")
        ],
        "alt": [
            ("Nông sản không đạt tiêu chuẩn (Dập nát, héo úa)", "5.a.1 Nhà vườn xem khuyến nghị xử lý và không thể niêm yết làm hàng tươi sống.", "5.a.2 AI chấm Freshness Score < 65 và xếp hạng 'Không đạt'; hệ thống hiển thị cảnh báo đỏ, từ chối cấp tem và khóa nút đăng bán để bảo vệ người tiêu dùng."),
            ("Sự cố mạng hoặc gián đoạn API Gemini", "3.a.1 Hệ thống tự động chuyển đổi luồng xử lý trong suốt đối với người dùng.", "3.a.2 Backend kích hoạt Rule-based Fallback Engine; phân tích ảnh bằng thuật toán mô phỏng cục bộ để đảm bảo hệ thống không bao giờ bị tê liệt.")
        ]
    },
    {
        "id": "UC-15",
        "name": "Kiểm định ảnh nông sản độc lập (AI Check cho Khách)",
        "actor": "Khách hàng, Google Gemini 1.5 Flash (AI Engine)",
        "desc": "Cung cấp công cụ AI Check minh bạch cho Khách hàng: Người mua có thể chụp ảnh gói rau củ nhận được để kiểm tra độ tươi thực tế, hoặc tải ảnh nông sản bất kỳ để nhận phân tích chất lượng tức thì trước khi quyết định mua hàng.",
        "pre": "Người dùng truy cập trang /ai-check trên ứng dụng web.",
        "post": "Giao diện mô phỏng tia quét AI (Scanning Beam) và kết xuất bảng đánh giá đa tiêu chí cho khách hàng.",
        "basic": [
            ("Bước 1 - 2", "1. Khách hàng vào mục 'Kiểm tra chất lượng AI' (/ai-check) và tải lên ảnh nông sản cần thẩm định (hoặc chọn ảnh mẫu có sẵn).", "2. Khách hàng bấm nút 'Bắt đầu phân tích AI'."),
            ("Bước 3 - 4", "3. Frontend hiển thị hiệu ứng quét tia laser xanh (Scanning Effect).", "4. Backend FastAPI gọi Gemini 1.5 Flash phân tích và trả về điểm số tươi mới, đánh giá màu sắc, độ giòn mọng nước và lời khuyên bảo quản tủ lạnh."),
            ("Bước 5", "5. Khách hàng xem bảng kết quả chi tiết và có thể bấm 'Thêm vào giỏ hàng' nông sản cùng loại đang bán trên sàn.", "5. Hệ thống liên kết kết quả thẩm định với các gian hàng đang bán loại nông sản tương ứng.")
        ],
        "alt": [
            ("File tải lên không phải ảnh", "1.a.1 Khách hàng chọn lại file ảnh định dạng PNG/JPG.", "1.a.2 Hệ thống kiểm tra mime-type; nếu không phải file ảnh, báo lỗi Toast: 'Vui lòng chọn tệp hình ảnh hợp lệ'.")
        ]
    },
    {
        "id": "UC-16",
        "name": "Giám sát nhật ký kiểm định AI toàn sàn (Admin AI Logs)",
        "actor": "Quản trị viên (Admin)",
        "desc": "Cho phép Admin tra cứu lịch sử toàn bộ các lượt thẩm định chất lượng nông sản đã diễn ra trên sàn (cả từ phía Nhà vườn và Khách hàng), xem hình ảnh đã phân tích, điểm số tươi mới và tỷ lệ phân bố chất lượng toàn sàn.",
        "pre": "Đăng nhập với quyền ROLE_ADMIN.",
        "post": "Dữ liệu lịch sử kiểm định được truy xuất từ db.ai_logs và hiển thị trực quan.",
        "basic": [
            ("Bước 1 - 2", "1. Admin truy cập Kênh Quản trị -> 'Nhật ký Kiểm định AI' (/admin/ai-logs).", "2. Hệ thống gọi GET /api/v1/ai/logs, hiển thị bảng dữ liệu phân trang: Mã lượt quét, Tên nông sản, Ảnh thu nhỏ, Phân hạng, Điểm tươi, Thời điểm phân tích, Mô hình sử dụng (Gemini 1.5 Flash)."),
            ("Bước 3 - 4", "3. Admin có thể tìm kiếm theo tên sản phẩm hoặc lọc theo phân hạng (Loại 1, Loại 2, VietGAP, Không đạt).", "4. Hệ thống lọc dữ liệu tức thì và hiển thị tổng số lượt thẩm định đã thực hiện."),
            ("Bước 5", "5. Admin nhấp vào một dòng để xem chi tiết toàn văn nhận xét sinh học của AI.", "5. Hệ thống mở modal hiển thị đầy đủ các đánh giá về màu sắc, hình thái và bề mặt.")
        ],
        "alt": [
            ("Phát hiện nhà vườn đăng ảnh giả mạo", "5.a.1 Admin bấm nút 'Khóa gian hàng cảnh cáo'.", "5.a.2 Admin phát hiện ảnh chụp sai lệch nghiêm trọng với hàng giao; kích hoạt lệnh hạ sản phẩm và khóa quyền đăng bán của gian hàng vi phạm.")
        ]
    },
    {
        "id": "UC-17",
        "name": "Tích lũy điểm thưởng tiêu dùng xanh (Loyalty)",
        "actor": "Khách hàng, Hệ thống (Order Service)",
        "desc": "Tự động tích lũy điểm thưởng khi khách hàng hoàn tất mua sắm nông sản sạch (Tỷ lệ: 10.000 VNĐ tiền hàng = 1 điểm tích lũy, tương đương hoàn tiền 1% giá trị giao dịch).",
        "pre": "Khách hàng đã nhận hàng và đơn hàng chuyển sang trạng thái 'delivered'.",
        "post": "Số dư điểm thưởng trong db.loyalty_points được cộng tự động, lịch sử tích điểm được ghi nhận.",
        "basic": [
            ("Bước 1 - 2", "1. Đơn vị vận chuyển hoặc Nhà vườn cập nhật trạng thái đơn hàng thành 'Giao hàng thành công' (Delivered).", "2. Backend FastAPI kích hoạt sự kiện on_order_completed(order_id)."),
            ("Bước 3 - 4", "3. Hệ thống tính toán số điểm thưởng được nhận: points_earned = int(total_amount / 10000).", "4. Hệ thống thực hiện $inc: {available_points: +points_earned, total_earned: +points_earned} trong db.loyalty_points."),
            ("Bước 5", "5. Hệ thống ghi nhật ký giao dịch: 'Tích điểm đơn hàng #{order_id}'.", "5. Khách hàng nhận thông báo Toast / In-app: 'Bạn vừa được cộng X điểm thưởng tiêu dùng xanh!'.")
        ],
        "alt": [
            ("Đơn hàng bị trả lại / Hoàn tiền", "1.a.1 Khách hàng nhận tiền hoàn trả.", "1.a.2 Nếu đơn hàng bị hoàn trả, hệ thống không kích hoạt cộng điểm hoặc thu hồi điểm thưởng tương ứng nếu đã tạm cộng.")
        ]
    },
    {
        "id": "UC-18",
        "name": "Đổi điểm thưởng lấy Voucher giảm giá",
        "actor": "Khách hàng, Loyalty Service",
        "desc": "Cho phép khách hàng quy đổi số điểm tích lũy trong ví để nhận các Voucher giảm giá (Ví dụ: 100 điểm = Voucher 10.000đ; 300 điểm = Voucher 30.000đ; 500 điểm = Voucher Miễn phí vận chuyển 50.000đ).",
        "pre": "Khách hàng đã đăng nhập và số dư điểm khả dụng >= số điểm của gói voucher.",
        "post": "Số điểm tích lũy bị trừ tương ứng; mã Voucher mới được thêm vào danh sách voucher khả dụng của khách hàng.",
        "basic": [
            ("Bước 1 - 2", "1. Khách hàng truy cập 'Ví điểm thưởng & Đổi quà' (/account?tab=loyalty).", "2. Hệ thống gọi GET /api/v1/loyalty/balance, hiển thị số dư điểm hiện có và danh sách các gói Voucher sẵn sàng đổi."),
            ("Bước 3 - 4", "3. Khách hàng chọn gói Voucher 30.000đ (Yêu cầu 300 điểm) và bấm 'Đổi mã ngay'.", "4. Backend tiếp nhận POST /api/v1/loyalty/redeem, kiểm tra available_points >= 300."),
            ("Bước 5 - 6", "5. Khách hàng nhận thông báo đổi thành công kèm mã Voucher mới xuất hiện trong ví.", "6. Hệ thống trừ 300 điểm trong db.loyalty_points, sinh mã Voucher ngẫu nhiên lưu vào mảng vouchers của user và ghi lịch sử đổi quà.")
        ],
        "alt": [
            ("Số dư điểm không đủ", "3.a.1 Khách hàng tiếp tục tích lũy điểm qua các đơn hàng sau.", "3.a.2 Số dư khả dụng < điểm yêu cầu; hệ thống làm mờ nút đổi và báo: 'Bạn cần thêm X điểm để đổi voucher này'.")
        ]
    },
    {
        "id": "UC-19",
        "name": "Nâng hạng thành viên khách hàng (Tier Upgrade)",
        "actor": "Khách hàng, Loyalty Service",
        "desc": "Hệ thống tự động theo dõi tổng điểm tích lũy trọn đời (total_earned) và tự động nâng hạng thẻ thành viên: Đồng (Mặc định), Bạc (>= 500 điểm), Vàng (>= 1.500 điểm), Kim Cương (>= 3.000 điểm) kèm các đặc quyền độc quyền (Ưu tiên giao rau sớm, Giảm giá sinh nhật, Miễn phí vận chuyển trọn đời).",
        "pre": "Khách hàng tích lũy thêm điểm từ đơn hàng mới.",
        "post": "Hạng thành viên (current_tier) được nâng cấp và hiển thị huy hiệu mới trên giao diện cá nhân.",
        "basic": [
            ("Bước 1 - 2", "1. Sau mỗi lần cộng điểm thành công, Loyalty Service kiểm tra ngưỡng tổng điểm total_earned.", "2. Nếu total_earned chạm ngưỡng hạng mới, hệ thống tự động cập nhật current_tier (Ví dụ: Nâng từ 'Đồng' lên 'Bạc')."),
            ("Bước 3", "3. Khách hàng đăng nhập vào trang cá nhân (/profile).", "3. Hệ thống hiển thị huy hiệu Hạng thẻ mới kèm hiệu ứng chúc mừng và kích hoạt các đặc quyền ưu đãi tương ứng.")
        ],
        "alt": [
            ("Chưa đủ điểm thăng hạng", "1.a.1 Khách hàng xem thanh tiến trình thăng hạng.", "1.a.2 Hệ thống hiển thị thanh phần trăm: 'Còn X điểm nữa để thăng hạng Vàng'.")
        ]
    },
    {
        "id": "UC-20",
        "name": "Báo cáo thống kê doanh thu & Giám sát sàn",
        "actor": "Quản trị viên (Admin)",
        "desc": "Cung cấp bảng điều khiển trung tâm (Admin Dashboard) với các biểu đồ trực quan về tổng doanh thu theo ngày/tháng, số lượng đơn hoàn thành, top nông sản bán chạy nhất, và biểu đồ tỷ lệ phân loại chất lượng nông sản qua AI.",
        "pre": "Đăng nhập với quyền ROLE_ADMIN.",
        "post": "Số liệu thống kê tài chính và vận hành được kết xuất trực quan.",
        "basic": [
            ("Bước 1 - 2", "1. Admin truy cập trang chủ Quản trị (/admin).", "2. Hệ thống gọi GET /api/v1/statistics/dashboard, tổng hợp dữ liệu từ db.orders, db.products, db.users và db.ai_logs."),
            ("Bước 3 - 4", "3. Admin xem các chỉ số KPI: Tổng doanh thu (VNĐ), Tổng đơn hàng, Số lượng nhà vườn đối tác, Số lượt kiểm định AI.", "4. Hệ thống hiển thị biểu đồ đường Recharts doanh thu 30 ngày qua và biểu đồ tròn phân bố chất lượng (Loại 1: 65%, Loại 2: 28%, Loại 3: 7%)."),
            ("Bước 5", "5. Admin chọn khoảng thời gian và nhấn nút 'Xuất báo cáo PDF / Excel'.", "5. Backend kết xuất báo cáo tổng hợp kèm chữ ký số và mã QR Code lưu trữ.")
        ],
        "alt": [
            ("Không có dữ liệu trong khoảng thời gian chọn", "5.a.1 Admin chọn lại mốc thời gian hợp lý.", "5.a.2 Hệ thống hiển thị thông báo: 'Không có giao dịch phát sinh trong khoảng thời gian này'.")
        ]
    }
]

print(f"Loaded {len(AGRIXANH_USE_CASES)} Use Cases for AgriXanh.")
