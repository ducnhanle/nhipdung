# Nhật ký thay đổi của fork nhipdung (tiếng Việt)

Fork: [ducnhanle/nhipdung](https://github.com/ducnhanle/nhipdung) (trước đây là `ducnhanle/editonny`), tách từ [soumatheusgomes/editonny](https://github.com/soumatheusgomes/editonny) (tác giả gốc: Matheus Gomes, giấy phép MIT). Tệp này là ngoại lệ ngôn ngữ đã ghi trong `AGENTS.md`. Bằng chứng kiểm chứng chuẩn (tiếng Anh) nằm ở `docs/validation.md`, mục "Vietnamese support and fork source (2026-11-01)".

## 2026-11-01 · Bỏ link Instagram của tác giả gốc

Bạn yêu cầu bỏ link Instagram và dòng "forked from". Đã bỏ link Instagram (`instagram.com/matheusgomes`) khỏi:
- mục tác giả trong cả 4 README;
- dòng ghi công trong `SKILL.md` và README của engine và visuals;
- `package.json`: trường `url` của tác giả gốc giờ là `github.com/soumatheusgomes`;
- metadata và dữ liệu có cấu trúc (JSON-LD) của trang hướng dẫn: link tác giả gốc giờ cũng trỏ về GitHub.

Vẫn giữ tên, email và link GitHub của Matheus Gomes. Thông báo bản quyền trong `LICENSE.md` cũng giữ nguyên, vì giấy phép MIT bắt buộc như vậy.

Không sửa được bằng mã nguồn (phải làm trong cài đặt GitHub):
- Ô **Website** trong mục About của repo vẫn là `https://instagram.com/matheusgomes`; ô **Description** vẫn ghi "Created by Matheus Gomes.". Hai ô này được chép từ repo gốc khi fork.
- Dòng **"forked from soumatheusgomes/editonny"**: chỉ GitHub mới tách được repo khỏi mạng fork.

## 2026-11-01 · README tiếng Việt

Bạn yêu cầu tạo README tiếng Việt. Đã làm:

- **`README.vi.md`**: bản dịch đầy đủ của `README.md`.
  - Yêu cầu cài đặt chép nguyên văn từ trang `/vi`; test bắt buộc hai chỗ phải khớp nhau.
  - Dòng chọn ngôn ngữ ở cả 4 README đều có thêm "Tiếng Việt".
  - Gói plugin giờ kèm theo tệp này.
- **11 banner động tiếng Việt** trong `docs/assets/readme/vi/`, tạo bằng `npm run readme:art` từ chữ của trang `/vi`.
  - Banner nhúng đúng các font của trang `/vi`: Plus Jakarta Sans, Anton, Montserrat, Sriracha, Sedgwick Ave Display. Font Latin cũ (Figtree) thiếu 93 chữ cái tiếng Việt.
  - Độ rộng chữ được đo bằng chính Plus Jakarta Sans, nên chữ được ngắt dòng và co cỡ theo đúng font.
  - Ô phụ đề viết tay dùng hệ số rộng của Sriracha. Nếu giữ hệ số của Caveat, chữ sẽ tràn ô.
  - Tiêu đề lớn ở banner đầu giãn dòng thêm 10%: ở bản đầu, dấu nặng của "Bạn" chạm vào chữ "i" của "Video".
- **Sửa thêm một lỗi có sẵn ở cả 4 ngôn ngữ:** dòng chữ xanh dưới tên tác giả trong banner đầu tràn ra ngoài viền khung (khoảng 8 px ở bản tiếng Anh, 11 px ở bản tiếng Việt). Banner đầu của 3 ngôn ngữ kia chỉ đổi đúng độ rộng khung này.
- Sửa câu "3 ngôn ngữ" thành "4 ngôn ngữ" trong README tiếng Bồ Đào Nha và Tây Ban Nha.

Kiểm chứng:
- `npm run check` đạt: 113 test Python, 22 test Node, 339 test Vitest.
- Có test mới kiểm tra banner tiếng Việt nhúng font có đủ chữ tiếng Việt. Khi cố tình cho banner tiếng Việt dùng font Latin, test này báo lỗi.
- Đã xem cả 11 banner trong Chromium, ở trạng thái cuối và khi nằm trong thẻ `<img>`. Khi bật chính sách bảo mật (CSP) giống raw.githubusercontent.com, ảnh hiển thị giống hệt từng điểm ảnh.

Vòng rà soát độc lập (agent Claude Code, model Opus, chỉ đọc):
- Tìm ra 1 lỗi quan trọng và 7 lỗi nhỏ. Tôi đã tái hiện và sửa hết.
- **Lỗi quan trọng:** dấu tiếng Việt bị cắt ở mép các khung màu. Ví dụ: dấu nặng của "nhịp" và dấu hỏi của "Chỉ".
  - Mực đen nằm ngoài khung màu bị chìm vào nền tối.
  - Khung giờ cao hơn: 0,92 em phía trên dòng chữ, 0,27 em phía dưới.
- **Các lỗi nhỏ đã sửa:**
  - Tiêu đề thẻ Editor tiếng Việt tràn khung, nay được co cỡ vừa thẻ.
  - Dòng trả lời chữ in hoa bị dính: móc của "Ẳ" nằm ngay dưới chữ "U", đọc thành "CÂỤ". Dòng chữ in hoa tiếng Việt nay giãn 18%.
  - Terminal minh họa thiếu font Liberation Mono, nên trên Linux dấu bị lệch sang bên.
  - Test font chỉ kiểm tra 3 trong 5 font, nay kiểm tra đủ 5.
  - Hàm chọn font khi bị gọi lồng nhau thì đặt lại font Latin thay vì khôi phục font cũ.
  - Một số câu trong tài liệu chưa đúng.
  - Vài từ trong README tiếng Việt chưa tự nhiên, ví dụ "skill di động" và "nguồn gốc".
- Banner tiếng Anh, Bồ Đào Nha và Tây Ban Nha chỉ đổi ở banner đầu (độ rộng khung tác giả) và banner cài đặt (danh sách font của terminal).

Giới hạn:
- Chưa xem trực tiếp trên GitHub, Safari, Firefox.
- Chữ đơn cách (monospace) dùng font của máy người xem.
- Tiêu đề lớn trên trang `/vi` của guide cũng bị dấu nặng của "Bạn" chạm chữ "i" ở dòng dưới (giãn dòng 0.92). Bước này chưa sửa guide.
- Bản dịch chưa được người dịch chuyên nghiệp duyệt.

## 2026-11-01 · Repo GitHub đổi tên thành ducnhanle/nhipdung

Bạn đã đổi tên repo trên GitHub. Tôi đã kiểm tra: repo hiện là `ducnhanle/nhipdung`, công khai.

Mọi link giờ dùng tên mới:
- yêu cầu cài đặt ở 4 ngôn ngữ và 3 README
- nguồn kiểm tra cập nhật của skill
- nút GitHub trên trang hướng dẫn
- huy hiệu, lịch sử sao, lệnh `git clone`
- `package.json`, banner cài đặt

Link cũ `ducnhanle/editonny` vẫn được GitHub tự chuyển hướng. Các mục nhật ký bên dưới ghi tên cũ vì đó là trạng thái lúc ấy.

## 2026-11-01 · Đổi tên thành nhipdung (Nhịp Dựng)

Bạn để tôi chọn tên. Tôi chọn **nhipdung** ("Nhịp Dựng" — nhịp của bản dựng) vì 3 lý do:
- khớp đúng lời hứa của sản phẩm "video có nhịp";
- chưa có repo GitHub nào trùng tên, tên gói npm còn trống;
- chỉ dùng chữ ASCII, nên gõ lệnh dễ và mọi font đều hiển thị được.

| Trước | Sau |
|---|---|
| `/editonny`, `$editonny`, `/editonny:editonny` | `/nhipdung`, `$nhipdung`, `/nhipdung:nhipdung` |
| `skills/editonny/`, `editonny.py`, `scripts/editonny.py` | `skills/nhipdung/`, `nhipdung.py`, `scripts/nhipdung.py` |
| `~/.local/share/editonny`, `~/Downloads/editonny/` | `~/.local/share/nhipdung`, `~/Downloads/nhipdung/` |
| Biến môi trường `EDITONNY_*`, gói `editonny-engine`, `@editonny/*` | `NHIPDUNG_*`, `nhipdung-engine`, `@nhipdung/*` (chỉ đổi tên, không đổi phiên bản thư viện nào) |
| Logo và biểu tượng chữ "e" | Chữ "n" |
| Tên trên trang hướng dẫn, README, banner, thẻ chia sẻ | nhipdung |

Giữ nguyên có chủ đích:
- Tên repo GitHub `ducnhanle/editonny`. Đổi tên repo là thao tác trên GitHub, bạn tự quyết. Sau khi đổi, báo tôi để cập nhật link; GitHub sẽ tự chuyển hướng link cũ.
- Mọi chỗ ghi công "editonny của Matheus Gomes" và link repo gốc.
- Các trang tham chiếu "đóng băng" trong `design-system/reference/`.
- Ảnh mẫu `og-image.png` của bộ thiết kế.
- Các mục lịch sử đã ghi ngày trong `docs/validation.md`.

Không có lớp tương thích với bản cài editonny cũ: hai bản có thể cài song song mà không đụng nhau. Nếu bạn đã cài bản cũ, cài lại bằng `python3 install.py --target claude` từ bản fork mới rồi gọi `/nhipdung`.

## 2026-11-01 · Thông tin tác giả của fork

Người duy trì fork: **ducnhanle** ([GitHub](https://github.com/ducnhanle)). Tài khoản GitHub không công khai tên hiển thị hay email, nên fork chỉ ghi tên tài khoản và trang GitHub; không đưa email lên repo công khai.

| Nơi | Thay đổi |
|---|---|
| `LICENSE.md`, `skills/editonny/LICENSE.md` | Giữ dòng bản quyền của Matheus Gomes (bắt buộc theo MIT), thêm dòng bản quyền cho phần sửa đổi của fork |
| `package.json` | `author` là ducnhanle; Matheus Gomes chuyển sang `contributors` |
| `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json` | Tác giả/chủ plugin là ducnhanle |
| README (3 ngôn ngữ), `SKILL.md`, README của engine và visuals | Ghi người duy trì fork, link repo/issues và nhật ký; vẫn ghi công tác giả gốc |
| Trang hướng dẫn | Chân trang: thay Instagram và email của tác giả gốc bằng `@ducnhanle`, thêm câu "Bản fork tiếng Việt này do ducnhanle duy trì" (4 ngôn ngữ). Metadata và JSON-LD ghi ducnhanle là người duy trì/xuất bản, Matheus Gomes vẫn là tác giả |

Giữ nguyên có chủ đích: chip "Người tạo ra editonny" với ảnh của Matheus Gomes trên trang chủ và thẻ chia sẻ. Đây là ghi công cho người tạo ra sản phẩm. Muốn thay bằng ảnh của bạn thì cần một tấm ảnh bạn đồng ý đưa lên repo.

**Đổi tên (chờ bạn chọn):**
- Ứng viên: **Nhịp Dựng** (`nhipdung`, chưa có repo GitHub nào trùng tên, khớp khẩu hiệu "video có nhịp"), Dựng Gọn (`dunggon`), Hậu Kỳ (`hauky`), Nhanh Gọn (`nhanhgon`), hoặc giữ `editonny-vi`.
- Đổi tên thật sự sẽ đụng tới lệnh `/editonny`, thư mục cài đặt và đường dẫn skill, nên làm riêng sau khi bạn chọn.

## 2026-11-01 · Hỗ trợ tiếng Việt và chuyển nguồn cài đặt sang fork

Nhánh: `ccr-1c161f3d-uzze72`. Thực hiện bằng Claude Code theo yêu cầu "làm/sửa những gì bạn đề xuất và ghi log lại".

### Tóm tắt

| Hạng mục | Kết quả |
|---|---|
| Nguồn cài đặt và cập nhật | Trỏ về `ducnhanle/editonny`; không bao giờ đề nghị "cập nhật" từ repo gốc |
| Chính sách agent | Cho phép phát triển bằng Claude Code hoặc Codex |
| Font tiếng Việt | Phụ đề, hook, CTA, chú thích, đồ họa chuyển động, template HyperFrames và 135 cảnh HTML đều vẽ đủ dấu |
| Từ vựng tiếng Việt | Từ đệm, từ không nên đứng cuối dòng, câu Whisper hay bịa, từ chức năng |
| Đọc số và tiền | "hai triệu rưỡi", "một trăm linh năm", "500k", "5 củ", đồng/VND/₫/đô |
| Gợi ý hình ảnh | Nhận giá, thu nhập, số đếm, phần trăm nói bằng tiếng Việt |
| Trang hướng dẫn | Thêm ngôn ngữ `vi` tại `/vi` (giao diện, 54 ví dụ, 145 cảnh, yêu cầu tạo ra, font, thẻ chia sẻ) |

### 1. Nguồn cài đặt và cập nhật

- `skills/editonny/references/setup.md`: mỗi lần gọi skill, agent kiểm tra cập nhật từ `ducnhanle/editonny`. Repo gốc được ghi rõ là upstream và **không** được đề nghị như bản cập nhật, vì cài nó sẽ xóa các thay đổi của fork.
- Yêu cầu cài đặt (`Install.askRequest`) ở cả 3 ngôn ngữ cũ, 3 README, banner cài đặt của README, nút "Lấy skill" trên trang hướng dẫn, `package.json`: đều trỏ về fork.
- Giữ ghi công tác giả: dòng tác giả trong README, chip tác giả, chân trang và thẻ chia sẻ vẫn trỏ về repo gốc. README có thêm dòng "This fork".

### 2. Chính sách phát triển bằng agent

`AGENTS.md` và `docs/setup.md` trước đây bắt buộc mọi việc dùng LLM phải qua Codex `gpt-6-astra`. Nay cho phép Claude Code hoặc Codex, vẫn cấm proxy, API key trả phí và đổi model ngầm. Ngoại lệ: pipeline đồ thị mã cục bộ (`npm run graph:update`) vẫn yêu cầu dấu vết Codex vì `scripts/graph_runtime.py` kiểm tra điều đó.

### 3. Font cho tiếng Việt

Vấn đề tìm thấy:

- Figtree (phụ đề `clean_caption`, chữ phụ của CTA, chú thích), Caveat (chữ viết tay) và Permanent Marker (hook `marker`) không có chữ tiếng Việt. Engine **xóa** các chữ thiếu: "Việt Nam, cảm ơn các bạn" thành "Vit Nam, cm n các bn".
- **Lỗi âm thầm nghiêm trọng hơn:** với chữ Figtree không có sẵn nhưng bộ dựng chữ (libraqm) tự ghép từ chữ gốc và dấu rời, kết quả bị mất dấu mà không có cảnh báo: "Nguyễn" hiển thị thành "Nguyẽn".
- Font Inter trong các cảnh chỉ có bản cắt Latin, Sora không có tiếng Việt, nên trình duyệt lấy font hệ thống cho các chữ có dấu.

Cách sửa:

- Thêm 3 font OFL có đủ tiếng Việt, kiểu dáng gần với font gốc (đã so sánh bằng ảnh render): **Plus Jakarta Sans** (thay vai trò Figtree), **Sriracha** (thay Caveat), **Sedgwick Ave Display** (thay Permanent Marker). Chúng được khai báo là `fallback` trong `fonts.json`.
- `text_render.font_for_texts`: một video, hook hay thẻ **chỉ** đổi sang font dự phòng khi văn bản có chữ mà font gốc không có glyph riêng. Việc kiểm tra tắt bộ dựng chữ, nên bắt được cả lỗi "Nguyễn → Nguyẽn". Cả track phụ đề dùng chung một font (không nhảy font giữa các câu). Tiếng Anh, Bồ Đào Nha, Tây Ban Nha giữ nguyên font cũ.
- Đồ họa chuyển động (bar chart, steps, checklist…) dùng cùng cơ chế qua `visuals/engine.text_fonts`.
- HTML (cảnh và template HyperFrames): thêm khai báo `@font-face` cùng tên họ font với `unicode-range` chỉ gồm các chữ còn thiếu:
  - Inter: bản cắt tiếng Việt của chính Inter 4.001 từ Google Fonts (cùng bản build, cùng thông số; ghép liền mạch).
  - Sora: các chữ thiếu lấy từ Plus Jakarta Sans.
  - Caveat: các chữ thiếu lấy từ Sriracha.
- **Lưu ý kỹ thuật đã kiểm chứng:** Chrome chỉ ghép các `@font-face` có `unicode-range` khi khai báo độ đậm giống hệt nhau. Font phụ luôn dùng đúng `font-weight` của font chính.
- `widths.json` (bảng độ rộng chữ của template): thêm 412 mục cho chữ tiếng Việt, đo bằng đúng font trình duyệt sẽ vẽ (không qua bộ dựng chữ). Các mục cũ giữ nguyên.
- Bổ sung giấy phép OFL cho Inter, Sora, Playfair Display và các font mới; ghi nguồn và SHA-256 trong `THIRD_PARTY_NOTICES.md`. Repo gốc thiếu giấy phép của Inter, Sora và Playfair Display.

### 4. Từ vựng tiếng Việt trong engine

- `assemble_cut.py`: từ đệm "ờ, ơ, ừ, ừm, ờm, à, ừa, hử, thì, kiểu".
  - **Sửa lỗi gốc:** các từ đệm có dấu của tiếng Bồ Đào Nha ("então", "né", "tá", "aí", "hã", "éé") trước đây không bao giờ khớp, vì token đã bị bỏ dấu trước khi so. Nay danh sách được chuẩn hóa giống token.
- `text_render.py`: các từ không nên đứng cuối dòng phụ đề ("và, của, là, thì, mà, những, các, một, cho, với, để…").
- `transcribe.py`: các câu Whisper hay bịa ra trên đoạn im lặng, ví dụ "Hãy subscribe cho kênh Ghiền Mì Gõ để không bỏ lỡ những video hấp dẫn". Chúng chỉ bị bỏ khi phần lớn đoạn đó là im lặng; người nói thật sự nói câu này vẫn được giữ.
- `suggest_visuals.py`: từ chức năng tiếng Việt.

### 5. Đọc số và tiền tiếng Việt

- `spoken_numbers.py`: số tiếng Việt được nhận theo **đúng cách viết có dấu**, nên không nhầm "sáu" (6) với "sau", "năm" (5) với "nam", "đô" (USD) với "đó".
- Ngữ pháp vị trí đọc được:
  - hàng trăm/chục/đơn vị: "một trăm linh năm" = 105, "hai mươi lăm" = 25, "mười lăm" = 15
  - lũy thừa nghìn/triệu/tỷ: "hai tỷ năm trăm triệu"
  - kiểu nói tắt: "một triệu hai" = 1,2 triệu, "hai triệu rưỡi" = 2,5 triệu, "nửa triệu"
  - kiểu viết tắt: "500k", "2,5 triệu", "5 củ"
  - đơn vị tiền: đồng, VND, ₫, đ, đô
- Các trường hợp không bị nhận nhầm là tiền: "hai đồng hồ", "không đồng ý", "năm đó", "đồ cũ", "hàng triệu người". "mười năm" là mười năm (thời gian), không phải 15.
- **Sửa lỗi gốc:** "500k" và "10mil" (viết liền) trước đây không đọc được.
- `suggest_visuals.py` gợi ý được bảng giá, giá cũ → giá mới, thu nhập theo tháng, số học viên ("hơn 500 học viên"), "3 sai lầm", "30 phần trăm".

### 6. Trang hướng dẫn tiếng Việt (`/vi`)

- Đường dẫn: `/vi`, `/vi/tao-yeu-cau`, `/vi/danh-muc`, `/vi/vi-du`, `/vi/cai-dat`. Trình duyệt tiếng Việt (`vi`, `vi-VN`) tự chuyển sang `/vi`.
- Bản dịch: giao diện (`web/messages/vi.json`), 54 ví dụ (`web/content/examples/vi.json`), 145 cảnh (`web/content/scenes/vi.json`), câu yêu cầu gửi agent (`web/src/features/request/phrases/vi.ts`, dịch đủ mọi điều khoản về dọn dẹp, xác nhận, âm thanh, màu sắc, đoạn mẫu).
- Menu ngôn ngữ có "Tiếng Việt" (cờ Việt Nam). Tìm kiếm bỏ dấu và coi "đ" như "d" ("dau chi" tìm được "Dấu chỉ").
- Font riêng cho trang tiếng Việt (bản cắt Latin + tiếng Việt), không ảnh hưởng tải trang các ngôn ngữ khác. Thẻ chia sẻ (Open Graph) tiếng Việt hiển thị đủ dấu.

### Kiểm chứng (2026-11-01, container Linux)

| Lệnh | Kết quả |
|---|---|
| `npm run check` | Đạt: 113 test Python, 21 Node, 337 Vitest, lint, typecheck, 49 icon |
| `npm run build` | Đạt |
| `npm run test:engine` | Đạt 131 test (1 bỏ qua có sẵn), trong đó 31 test tiếng Việt mới |
| Test trình duyệt (Playwright) | Lần chạy cuối: 206 đạt, 30 bỏ qua. Ở một lần chạy trước, `library.spec.ts:112` trên điện thoại bị lỗi; test này cũng hỏng 6/6 lần trên bản gốc chưa sửa trong cùng môi trường, nên đó là lỗi do môi trường, không do thay đổi này |
| Trang `/vi` | Đạt kiểm tra a11y (axe), không tràn ngang, không lỗi console, sáng/tối, desktop/điện thoại |
| Render thật HyperFrames 0.8.179 | Đạt (smoke chuẩn và bản tiếng Việt). Phải nạp GSAP 3.14.2 từ npm vì container chặn cdn.jsdelivr.net |

Ảnh render đã xem trực tiếp:
- Phụ đề "CẢM ƠN"
- Nhãn viết tay "Tuyệt vời ông mặt trời"
- Cảnh doanh thu với "DOANH THU HÀNG THÁNG", "trong 30 ngày, mỗi ngày một video", "+37 đơn hôm nay"
- Hook "ĐỪNG BỎ LỠ BÍ QUYẾT NÀY", CTA "ĐẶT HÀNG NGAY" và chú thích

### Vòng rà soát độc lập (sau commit đầu)

Một agent rà soát chỉ đọc (Claude Code) đã kiểm tra toàn bộ thay đổi bằng dữ liệu thật. Mọi lỗi đều đã tái hiện, sửa và có test hồi quy:

| Lỗi | Cách sửa |
|---|---|
| **Nghiêm trọng:** bộ gợi ý crash với "2 triệu người theo dõi" (số + đơn vị tiếng Việt) | Dùng chung bảng hệ số `ALL_MULTIPLIERS` |
| Phụ đề tiếng Bồ Đào Nha bị tính thấp hơn tới 35 px (ảnh hưởng chỗ đặt phụ đề) | Chỉ thêm chữ hoa có dấu; 125/125 trường hợp khớp bản gốc |
| "2 đô thị" bị hiểu là $2, "đồng bào" là tiền; "giỏ", "làn", "Ba Lan" bị hiểu là "giờ", "lần" | Đơn vị phải đúng chính tả có dấu; loại trừ từ ghép của đồng/đô; chuẩn hóa cả câu thay vì từng từ |
| Văn bản dấu tách rời (NFD) khiến "bà" bị đọc thành "ba" (số 3) | Chuẩn hóa về NFC trước khi nhận số, vẫn giữ bản đồ vị trí |
| Ký hiệu ₫ biến mất trên thẻ giá | Ký hiệu tiền tệ cũng quyết định font; ₫ dự phòng thành đ |
| 36 độ rộng chữ của Caveat đo sai | Đo không qua bộ dựng chữ |
| "Comenta ROI" (tiếng Bồ Đào Nha) mất gợi ý | Bỏ các từ chức năng tiếng Việt trùng với tiếng Bồ Đào Nha sau khi bỏ dấu |
| "Um" (một) và "há" (có) tiếng Bồ Đào Nha bị cắt như từ đệm | So từ đệm đúng như được nói (giữ dấu) |
| "4k" (độ phân giải) bị hiểu là 4000 | Bỏ qua "Nk" khi chỉ có một chữ số |
| Chia câu phụ đề và render có thể dùng hai font khác nhau | `captions.json` lưu font đã dùng khi chia câu |

Còn để lại (đã ghi trong `docs/validation.md`):
- Trang `/vi` vẫn tải trước font Latin Figtree; Next.js tải trước font theo layout nên không tách riêng được cho từng ngôn ngữ.
- Chữ Sriracha bổ sung cho Caveat không được làm đậm giả.
- Chưa đọc được một số cách nói rất khẩu ngữ như "hai lăm nghìn", "1tr2", "chục triệu".

### Chưa làm và lý do

- **Đổi tên/nhận diện thương hiệu khi phát hành công khai:** cần bạn quyết định tên mới, ảnh và thông tin tác giả của fork. Hiện vẫn giữ tên "editonny" và ghi công tác giả gốc, điều này hợp lệ theo MIT.
- **README tiếng Việt và banner tiếng Việt:** README dịch là ngoại lệ tùy chọn. Banner nhúng font Latin nên cần làm riêng. *(Đã làm sau đó, xem mục "README tiếng Việt" ở đầu tệp.)*
- **Xuất timeline cho phần mềm dựng, phụ đề dịch, hỗ trợ Windows:** là tính năng lớn. Phụ đề dịch đụng tới cơ chế xác nhận và băm cài đặt; Windows không kiểm thử được trong container Linux. Nên làm thành từng đợt riêng.
- **Cảnh riêng cho lĩnh vực của bạn:** cần biết lĩnh vực và nội dung bạn muốn.
- **Các bộ gợi ý hình ảnh khác** (các bước, checklist, gạch bỏ, kêu gọi bình luận, bước ngoặt, ưu đãi, nhấn mạnh) vẫn dựa trên câu tiếng Bồ Đào Nha/Anh.
- **Số chữ mỗi câu phụ đề:** tiếng Việt viết theo âm tiết cách nhau bằng dấu cách, nên mặc định "tối đa 3 từ" thực chất là 3 âm tiết. Nên đề xuất khoảng 5 âm tiết cho video tiếng Việt trong bảng cài đặt. Chưa đổi mặc định vì cần thử độ dễ đọc trên video thật.
- **Không chạy được:** `npm run test:preview` và `npm run test:scenes` (cần công cụ `agent-browser`). Chưa thử trên giọng nói tiếng Việt thật, độ chính xác Whisper tiếng Việt, mọi cảnh, video dài.
- **Bản dịch chưa được người bản ngữ duyệt.** Một số lựa chọn có thể muốn chỉnh:
  - Số tiền minh họa "R$" vẫn giữ nguyên.
  - Tên "editonny" viết thường.
  - Chữ trên thẻ cảnh cần giữ ngắn gần bằng bản gốc: nhãn "đơn hàng hôm nay" dài hơn "sales today" đã bị HyperFrames báo che khuất.

### Cách dùng bản fork

```sh
git clone https://github.com/ducnhanle/nhipdung.git && cd nhipdung
python3 install.py --target claude   # hoặc --target both
```

Sau đó nhờ agent làm theo `skills/editonny/references/setup.md` để tải renderer, model Whisper và OCR, khởi động lại Claude Code rồi gõ `/editonny`. Để chạy trang hướng dẫn: `npm ci && python3 editonny.py guide`, rồi mở `http://localhost:4173/vi`.
