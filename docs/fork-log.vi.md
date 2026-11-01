# Nhật ký thay đổi của fork (tiếng Việt)

Fork: [ducnhanle/editonny](https://github.com/ducnhanle/editonny), tách từ [soumatheusgomes/editonny](https://github.com/soumatheusgomes/editonny) (tác giả gốc: Matheus Gomes, giấy phép MIT). Tệp này là ngoại lệ ngôn ngữ đã ghi trong `AGENTS.md`. Bằng chứng kiểm chứng chuẩn (tiếng Anh) nằm ở `docs/validation.md`, mục "Vietnamese support and fork source (2026-11-01)".

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
- `widths.json` (bảng độ rộng chữ của template): thêm 412 mục cho chữ tiếng Việt, đo bằng đúng font trình duyệt sẽ vẽ. Các mục cũ giữ nguyên.
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
| `npm run test:engine` | Đạt 120 test (1 bỏ qua có sẵn), trong đó 20 test tiếng Việt mới |
| Test trình duyệt (Playwright) | 205 đạt, 30 bỏ qua, 1 lỗi. Lỗi `library.spec.ts:112` trên điện thoại cũng hỏng 6/6 lần trên bản gốc chưa sửa trong cùng môi trường, nên không do thay đổi này |
| Trang `/vi` | Đạt kiểm tra a11y (axe), không tràn ngang, không lỗi console, sáng/tối, desktop/điện thoại |
| Render thật HyperFrames 0.8.179 | Đạt (smoke chuẩn và bản tiếng Việt). Phải nạp GSAP 3.14.2 từ npm vì container chặn cdn.jsdelivr.net |

Ảnh render đã xem trực tiếp:
- Phụ đề "CẢM ƠN"
- Nhãn viết tay "Tuyệt vời ông mặt trời"
- Cảnh doanh thu với "DOANH THU HÀNG THÁNG", "trong 30 ngày, mỗi ngày một video", "+37 đơn hôm nay"
- Hook "ĐỪNG BỎ LỠ BÍ QUYẾT NÀY", CTA "ĐẶT HÀNG NGAY" và chú thích

### Chưa làm và lý do

- **Đổi tên/nhận diện thương hiệu khi phát hành công khai:** cần bạn quyết định tên mới, ảnh và thông tin tác giả của fork. Hiện vẫn giữ tên "editonny" và ghi công tác giả gốc, điều này hợp lệ theo MIT.
- **README tiếng Việt và banner tiếng Việt:** README dịch là ngoại lệ tùy chọn. Banner nhúng font Latin nên cần làm riêng.
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
git clone https://github.com/ducnhanle/editonny.git && cd editonny
python3 install.py --target claude   # hoặc --target both
```

Sau đó nhờ agent làm theo `skills/editonny/references/setup.md` để tải renderer, model Whisper và OCR, khởi động lại Claude Code rồi gõ `/editonny`. Để chạy trang hướng dẫn: `npm ci && python3 editonny.py guide`, rồi mở `http://localhost:4173/vi`.
