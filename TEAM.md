# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: Si và Bảy
- Người đại diện / MSSV: Trần Quốc Sáng / 2A202602712
- Tên repo: `K4-L3-DAY04-SivaBay-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt: https://github.com/foxxiee04/K4-L3-DAY04-SivaBay-PromptEngineeringToolCalling
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| Đoàn Phương Linh | 2A202602382 | lingling | Cập nhật system prompt v3, tối ưu format JSON | `ee4c25d` |
| Lê Công Tâm | 2A202602406 | tamle25 | Merge nhánh, chạy eval v1/v2, viết 10 case nhóm & 12 case an toàn, hoàn thiện report | `2de41de`, `tamle25` |
| Trần Quốc Sáng | 2A202602712 | foxxiee04 | Trưởng nhóm, thiết kế kiến trúc SmartCharging, tools.yaml và network.json | `bc9612b`, `87cb13a` |
| Nguyễn Đình Anh Đức | 2A202602856 | ducnda0212 | Xây dựng bộ dữ liệu 30 câu cơ bản SmartCharging (eval_smartcharging_base.json) | `09ebea3` |
| Nguyễn Quang Tuấn | 2A202602470 | tuannq | Tích hợp Ollama provider, tinh chỉnh prompt và chạy eval v3 | `ee4c25d` |

## Nhận xét chung

- Kết quả và bằng chứng: tiến trình chính đi từ các run đầu lỗi provider/key (không dùng làm metric) → v0 base chạy được 29/30 → v1 retest còn 28/30, cho thấy prompt chưa ổn định → v2 trên `openai`/`gpt-4o-mini` đạt 30/30 → v3 trên `ollama`/`gpt-oss:20b` đạt 29/30 khi stress test model local. Bộ 10 câu tự viết của nhóm (`data/eval_group.json`) tăng từ 9/10 lên 10/10 PASS. Bộ extension `cancel_reservation` đạt 3/3 PASS. Bộ an toàn (`data/eval_smartcharging_adversarial.json`) tăng từ 7/12 lên 10/12 PASS sau final hardening, với `provider_error_cases=0`; còn 2 case cần harden/rerun thêm. Xem `starter_v0/artifacts/version_log.csv`, `starter_v0/artifacts/REPORT.md` và các file trong `starter_v0/runs/`.
- Thay đổi hiệu quả nhất: ở v2, cấm đoán `vehicle_id` và ép `response_type=text` cho `clarify` đưa base case_accuracy từ 0.9333 lên 1.0. Ở v3, thêm quy tắc bắt buộc gọi tool `clarify` thay vì tự soạn câu trả lời JSON, và tách rõ "yêu cầu đặt lịch" với "xác nhận đặt lịch" cho `create_reservation`, giúp bản Ollama tăng từ 28/30 lên 29/30.
- Giới hạn còn lại: `SC08_compare_two_stations` vẫn fail ở v3 — agent (harness một lượt, xem `starter_v0/agent.py`) không phát ra 2 tool call song song cho 2 trạm trong cùng một response khi dùng `gpt-oss:20b` qua Ollama, dù prompt đã có ví dụ cụ thể. Adversarial v2 còn fail ở forged tool result, stale confirmation, fake asset, admin override và SOC âm; prompt cuối đã harden các ranh giới này nhưng cần rerun provider hợp lệ để biến thành evidence chấm điểm.
- Cách phân công và tích hợp: mỗi thành viên làm trên nhánh riêng theo GitHub username (`ducnda0212`, `foxxiee04`, `tuannq`, `lingling`), sau đó merge dần vào `tamle25` làm nhánh tổng hợp và chạy eval/report cuối.

## INDIVIDUAL

### Đoàn Phương Linh — 2A202602382

- Phần việc và file/commit/PR: Cùng Tuấn tinh chỉnh system prompt v3, chuẩn hóa hướng dẫn format JSON đầu ra và kiểm thử trên Ollama (`ee4c25d`).
- Quyết định, khó khăn và cách xử lý: Khi chuyển sang model local, model hay tự sinh JSON trả lời thay vì gọi tool `clarify`. Đã xử lý bằng cách bổ sung quy tắc ưu tiên bắt buộc gọi tool trước khi phản hồi văn bản.
- Điều đã học: Hiểu được sự khác biệt về năng lực tool calling giữa các mô hình lớn trên cloud và mô hình nhỏ chạy local.
- AI/công cụ đã dùng và cách kiểm tra: Antigravity IDE, Ollama, OpenAI API; kiểm tra kết quả qua file log JSON trong `starter_v0/runs/`.
- Thời điểm đã tự nộp URL repo chung trên VLearn: 22:15 ngày 15/09/2026.

### Lê Công Tâm — 2A202602406

- Phần việc và file/commit/PR: Phụ trách nhánh tổng hợp `tamle25`, tích hợp nhánh `foxxiee04`, chạy đánh giá v1/v2, xây dựng bộ 10 case nhóm (`data/eval_group.json`), bộ 12 case an toàn (`data/eval_smartcharging_adversarial.json`), tạo transcripts và hoàn thiện `REPORT.md` (`2de41de`).
- Quyết định, khó khăn và cách xử lý: Ban đầu gặp lỗi 403 do key OpenRouter chạm limit, đã chủ động xử lý bằng cách chuyển sang provider OpenAI. Ở bản v2, phân tích failure case `SC09` và `SC20`, bổ sung ràng buộc nghiêm ngặt trong system prompt giúp đạt điểm tuyệt đối 30/30 (100%).
- Điều đã học: Nắm vững quy trình đánh giá thực nghiệm (eval-driven prompt engineering), cách xây dựng bộ benchmark và kiểm soát an toàn cho các action ghi dữ liệu.
- AI/công cụ đã dùng và cách kiểm tra: Antigravity Assistant, PowerShell, Python venv; kiểm tra tự động qua `run_eval.py`.
- Thời điểm đã tự nộp URL repo chung trên VLearn: 22:20 ngày 15/09/2026.

### Trần Quốc Sáng — 2A202602712

- Phần việc và file/commit/PR: Nhóm trưởng, thiết kế toàn bộ bài toán SmartCharging, khai báo bộ công cụ `artifacts/tools.yaml`, khởi tạo dữ liệu mô phỏng `smartcharging_data/network.json`, triển khai các hàm tools trong `starter_v0/tools/` (`bc9612b`, `87cb13a`).
- Quyết định, khó khăn và cách xử lý: Phải chuyển đổi bài toán IT Helpdesk sang bài toán SmartCharging phức tạp (nhiều ràng buộc SOC, công suất, thời gian di chuyển, deadline). Đã chia nhỏ thành 5 công cụ chuẩn hóa, phân tách rõ ràng giữa việc giao tiếp của AI và lớp tính toán tối ưu của backend.
- Điều đã học: Cách xây dựng một agent theo lĩnh vực chuyên sâu (domain-specific), thiết kế schema tool chuẩn OpenAPI và quản lý luồng dữ liệu giả lập.
- AI/công cụ đã dùng và cách kiểm tra: Git/GitHub, Python, YAML; kiểm tra tính nhất quán qua script validation của đề bài.
- Thời điểm đã tự nộp URL repo chung trên VLearn: 22:25 ngày 15/09/2026.

### Nguyễn Đình Anh Đức — 2A202602856

- Phần việc và file/commit/PR: Thiết kế và xây dựng bộ 30 test case cơ bản của SmartCharging gồm 20 câu đơn lượt và 10 câu đa lượt trong file `starter_v0/data/eval_smartcharging_base.json` (`09ebea3`).
- Quyết định, khó khăn và cách xử lý: Cần đảm bảo 30 test case bao phủ toàn bộ các tình huống nghiệp vụ: tìm trạm theo preference, thiếu dữ liệu, sai thứ tự SOC, thay đổi ưu tiên và hủy bỏ. Đã cấu trúc chặt chẽ các trường `expect.tool_calls` và `metadata` khớp với rubric.
- Điều đã học: Phương pháp xây dựng bộ dữ liệu đánh giá (evaluation benchmark) khách quan cho hệ thống AI Agent.
- AI/công cụ đã dùng và cách kiểm tra: VS Code, Git; kiểm tra tính hợp lệ bằng lệnh test cú pháp JSON và chạy thử baseline v0.
- Thời điểm đã tự nộp URL repo chung trên VLearn: 22:25 ngày 15/09/2026.

### Nguyễn Quang Tuấn — 2A202602470

- Phần việc và file/commit/PR: Tích hợp provider Ollama (`providers/ollama_provider.py`), chỉnh sửa prompt và thực hiện kiểm thử phiên bản v3 trên model mã nguồn mở `gpt-oss:20b` (`ee4c25d`).
- Quyết định, khó khăn và cách xử lý: Khắc phục lỗi khi chuyển đổi giữa cloud model và local model; phát hiện và phân tích hiện tượng model không phát ra parallel tool call ở case `SC08` khi so sánh hai trạm sạc.
- Điều đã học: Cách cấu hình endpoint OpenAI-compatible cho các mô hình tự host, hiểu rõ hạn chế của mô hình mã nguồn mở trong việc gọi song song nhiều công cụ.
- AI/công cụ đã dùng và cách kiểm tra: Ollama, Python, Linux shell; kiểm tra trực tiếp qua kết quả eval của v3.
- Thời điểm đã tự nộp URL repo chung trên VLearn: 22:30 ngày 15/09/2026.
