import type { RequestPhrases } from './types';

export const vi: RequestPhrases = {
  folderLabel: 'Dựng các video trong',
  folderPlaceholder: '[nhập thư mục video]',
  goalLabel: 'Mục tiêu',
  defaultGoal: 'biến video gốc thành một video rõ ràng, cuốn hút',
  formatLabel: 'Khung hình',
  paceLabel: 'Nhịp',
  captionsLabel: 'Phụ đề',
  visualsLabel: 'Hình ảnh',
  sceneReference: reference => `Cảnh tham khảo trong danh mục: ${reference}. Điều chỉnh chữ cho khớp với video thực tế.`,
  cleanupLabel: 'Dọn dẹp tiêu chuẩn khi dựng',
  cleanup: 'Loại bỏ các khoảng lặng không cần thiết, tiếng thở nghe rõ, chỗ nói vấp, chỗ nói hụt và những chỗ lặp lại thừa. Giữ trọn từng từ, nhịp nói tự nhiên, các khoảng lặng có chủ đích và ý nghĩa của lời nói. Đo điểm cắt trên bản ghi thực tế và kiểm tra các chỗ chuyển để lời nói không bị cắt cụt. Với các bản sửa có phạm vi cụ thể, chỉ dọn dẹp trong phạm vi chỉnh sửa được yêu cầu; giữ nguyên nội dung không liên quan và các mốc thời gian đã duyệt.',
  closing: 'Trước khi dựng, chỉ kiểm tra cục bộ các tệp đã chọn, trình bày bản tóm tắt đầy đủ các thiết lập tôi yêu cầu và bạn đề xuất, rồi chờ tôi xác nhận, kể cả khi yêu cầu này đã chi tiết. Bao gồm hình ảnh và bộ lọc, xử lý âm thanh và nhạc, phụ đề, ngôn ngữ trò chuyện/lời nói/phụ đề, các điểm cắt và khoảng lặng cần giữ, khung hình/độ phân giải/FPS/bố cục, đồ họa, duyệt đoạn mẫu và bàn giao. Không thêm nhạc, hiệu ứng âm thanh hay âm thanh nền trừ khi tôi yêu cầu rõ ràng. Cảnh minh họa, chuyển cảnh và nhịp dựng nhanh không có nghĩa là được thêm âm thanh. Giữ nguyên âm thanh có sẵn trong video gốc trong phạm vi được yêu cầu. Giữ nguyên diện mạo hình ảnh gốc: không tự ý đổi độ sáng, tông màu, độ tương phản, độ bão hòa, bộ lọc hay tự động chuyển đổi HDR/SDR. Giải thích các chuyển đổi cần thiết trước khi tiếp tục. Giữ nguyên ngôn ngữ đã ghi âm trừ khi tôi yêu cầu dịch. Lưu mỗi dự án gọn gàng trong thư mục Downloads/nhipdung với các bản xuất được đánh số; nếu chạy từ xa hoặc không có quyền truy cập, hãy giải thích và xác nhận một nơi lưu mà tôi truy cập được. Trước tiên, kiểm tra môi trường và các tệp. Giữ nguyên bản gốc, lời đã nói và ý nghĩa. Không bịa ra giá, kết quả hay lời chứng thực. Chuẩn bị một đoạn mẫu 8–15 giây để tôi duyệt trước khi hoàn thiện toàn bộ video. Không dùng dịch vụ trả phí hoặc tải media lên bên thứ ba khi chưa được tôi cho phép. Khi hoàn tất, báo cho tôi tệp kết quả và các bước kiểm tra đã thực hiện.',
  formats: { source: 'giữ nguyên tỉ lệ, độ phân giải và tốc độ khung hình gốc', vertical: '9:16 (dọc)', horizontal: '16:9 (ngang)', square: '1:1 (vuông)', portrait: '4:5 (dọc cho bảng tin)' },
  paces: { natural: 'tự nhiên, giữ các khoảng lặng có chủ đích', dynamic: 'nhanh, với điểm cắt chính xác và giữ trọn từng từ', calm: 'chậm rãi, có khoảng nghỉ cho cảm xúc và sự thấu hiểu' },
  captions: { readable: 'dễ đọc, nhấn nhẹ vào các từ quan trọng', subtle: 'tinh tế, không hiệu ứng động', none: 'không có phụ đề' },
  effects: { subtle: 'tinh tế, chỉ khi giúp giải thích lời nói', educational: 'mang tính hướng dẫn, với các bước, dấu chỉ và tiêu đề', expressive: 'giàu cảm xúc, với chuyển cảnh và điểm nhấn cân bằng', none: 'không có cảnh minh họa hay hiệu ứng bổ sung' },
};
