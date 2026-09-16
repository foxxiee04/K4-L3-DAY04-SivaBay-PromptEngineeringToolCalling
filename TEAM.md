# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: Si và Bảy
- Người đại diện / MSSV: 2A202602712
- Tên repo: `K4-L3-DAY04-SivaBay-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt: 
+ URL repo: https://github.com/foxxiee04/K4-L3-DAY04-SivaBay-PromptEngineeringToolCalling/tree/main
+ Nhánh nộp: main
+ Commit chốt: 
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| Đoàn Phương Linh | 2A202602382 | | | |
| Lê Công Tâm | 2A202602406 | | | |
| Trần Quốc Sáng | 2A202602712 | | | |
| Nguyễn Đình Anh Đức | 2A202602856 | | | |
| Nguyễn Quang Tuấn | 2A202602470 | | | |

## Nhận xét chung

- Kết quả và bằng chứng:
- Thay đổi hiệu quả nhất:
- Giới hạn còn lại:
- Cách phân công và tích hợp:

## INDIVIDUAL

Sao chép mục này cho từng thành viên.

### Trần Quốc Sáng — 2A202602712

- Phần việc và file/commit/PR:
  - Phụ trách phần cải thiện v1 cho SmartCharging trên nhánh `foxxiee04`.
  - Cập nhật prompt trong `starter_v0/artifacts/system_prompt.md` để agent ưu tiên lập phương án sạc bằng offer đã xác minh, không chỉ chọn trạm gần nhất.
  - File/commit: `starter_v0/artifacts/system_prompt.md`, commit `87cb13a feat: improve smartcharging v1 prompt`.
- Quyết định, khó khăn và cách xử lý:
  - Khó khăn chính là agent có xu hướng gọi `lookup_vehicle` dù yêu cầu đã đủ dữ liệu để lập phương án sạc.
  - Cách xử lý là làm rõ rule trong prompt: nếu đủ vehicle ID, SOC hiện tại, SOC mục tiêu, deadline và vị trí xuất phát thì gọi `find_charging_offers`; nếu thiếu hoặc dữ liệu không hợp lệ thì gọi `clarify`.
- Điều đã học:
  - Biết cách tách lỗi prompt, lỗi chọn tool và lỗi argument khi đọc kết quả eval.
  - Hiểu rằng offer chỉ là đề xuất, còn reservation là hành động ghi dữ liệu nên phải có xác nhận rõ.
- AI/công cụ đã dùng và cách kiểm tra:
  - Dùng ChatGPT/Codex để đọc yêu cầu, rà lỗi v1 và hỗ trợ chỉnh prompt.
  - Kiểm tra bằng `python scripts/preflight_provider.py --provider openai` và `python run_eval.py --provider openai --version v1 --suite base --eval-cases data/eval_smartcharging_base.json`.
  - Run v1 hợp lệ với `provider_error_cases: 0`, `measured_cases: 30`, `total_cases: 30`.
- Thời điểm đã tự nộp URL repo chung trên VLearn:
  - Chưa nộp, sẽ điền sau khi nộp URL repo chung trên VLearn.
