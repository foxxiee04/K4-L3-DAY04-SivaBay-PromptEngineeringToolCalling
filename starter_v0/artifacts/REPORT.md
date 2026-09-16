# Day 04 Lab v3 Report — Trợ lý AI của nhóm

- Lĩnh vực tự chọn: SmartCharging — trợ lý lập phương án sạc xe điện từ dữ liệu giả lập.
- Người dùng chính: Tài xế đã đăng nhập, cần tìm phương án sạc cho xe thuộc quyền sở hữu của mình.
- Nhiệm vụ chính: Thu thập xe, SOC hiện tại, SOC mục tiêu, deadline, vị trí xuất phát và tiêu chí ưu tiên; gọi lớp nghiệp vụ để trả Top-K offer đã được xác minh; tạo reservation chỉ sau khi tài xế xác nhận đúng offer hiện tại.
- Luồng cơ bản đã chốt trước v0: `clarify` dữ liệu thiếu → tùy yêu cầu dùng `lookup_vehicle`/`check_station_status` → `find_charging_offers` tính và verify offer → trình bày offer → hỏi xác nhận → `create_reservation` tái kiểm tra rồi ghi lịch giả lập.
- Ranh giới: AI không tự quyết định tính khả thi và không bịa trạm, connector, route, thời gian, công suất, giá, offer hoặc verdict. Tool error hay thiếu route evidence không được diễn giải thành “không khả thi”.
- Đường dẫn bộ 30 câu cơ bản chốt trước v0: `data/eval_smartcharging_base.json` (20 single-turn + 10 multi-turn). Commit chốt: nhóm điền hash commit sau khi review và trước khi chạy v0.
- Dữ liệu giả lập: `smartcharging_data/network.json`.
- Chức năng mở rộng ngoài luồng cơ bản: Không thực hiện trong phạm vi v0.

## Team

- Team: Si và Bảy
- Thành viên và INDIVIDUAL: [TEAM.md](../../TEAM.md)
- Members: 
  - Đoàn Phương Linh — 2A202602382
  - Lê Công Tâm — 2A202602406
  - Trần Quốc Sáng — 2A202602712
  - Nguyễn Đình Anh Đức — 2A202602856
  - Nguyễn Quang Tuấn — 2A202602470
- Provider/model: OpenAI GPT-4o-mini

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Agent hỗ trợ tài xế tra cứu xe/trạm và tìm các phương án sạc đã được tool nghiệp
vụ xác minh theo thời gian hoàn tất, chi phí hoặc quãng đường. Agent không tự
tính tính khả thi; offer chưa phải lịch giữ chỗ và reservation cần xác nhận rõ.

**Link dùng thử:**

> URL:

## A2. Tool agent có

| Tool | Chức năng | Core / optional / team-built |
|---|---|---|
| clarify | Hỏi bổ sung hoặc xác nhận | core |
| lookup_vehicle | Tra xe và kiểm tra quyền sở hữu | core, domain-built |
| check_station_status | Đọc snapshot trạng thái/cổng/công suất/giá của một trạm | core, domain-built |
| find_charging_offers | Tối ưu và verify Top-K offer từ dữ liệu giả lập | core, domain-built |
| create_reservation | Tái kiểm tra và tạo lịch sau xác nhận | core, domain-built action |

## A3. Câu hỏi mẫu

1. `EV-101 đang 30%, cần 80% trước 10:30 ngày 15/09/2026 UTC+07, xuất phát Quận 1; tìm phương án hoàn tất sớm nhất.`
2. `Kiểm tra trạng thái và cổng trống của trạm ST-303.`
3. `Tôi xác nhận đặt lịch đúng offer OFF-SEED-101.`

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Cải thiện version | Fallback run/transcript |
|---|---|---|---|
|  |  |  |  |

# PHẦN B — Chi tiết và evidence

Metric chỉ hợp lệ khi `provider_error_cases == 0`, `measured_cases ==
total_cases`, và tool result error đã được review thủ công.

## B1. Version evidence

| Version | Prompt/tool change | Hypothesis | Metric | Before | After | Run file |
|---|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |  |
| v1 |  |  |  |  |  |  |
| v2 |  |  |  |  |  |  |
| v3 |  |  |  |  |  |  |

## B2. Failure analysis

| Case ID | Failure type | Actual calls | What failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team eval cases

Liệt kê đúng 10 case tự viết: 5 single-turn và 5 multi-turn.

| Case ID | What it tests | Expected behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

| Scenario/turn | Version | Tool calls + args | Transcript/run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B4a. Adversarial evidence

Phân tích ít nhất 3 cases. Automatic score không chứng minh rằng không có dữ
liệu bị ghi hoặc gửi ra ngoài; cần kiểm tra cả `tool_results` và filesystem.

| Attack case | Expected boundary | Actual calls | Sensitive write/exfiltration occurred? | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Optional và bonus tool evidence

Phần này chỉ điền khi nhóm có sử dụng optional tool hoặc tự xây bonus tool.
Phần chung tối đa 90 điểm; mở rộng tối đa 10 điểm, tổng tối đa 100. Công cụ tự xây để phục vụ luồng cơ bản của lĩnh vực mới thuộc phần chung. `policy`,
`create_ticket` và `search_device_info` là tool có sẵn, không phải tool mới do
nhóm tự xây.

| Category | Evidence file | What worked | Risk / guardrail |
|---|---|---|---|
| Optional built-in |  |  |  |
| External search + privacy boundary |  |  |  |
| Bonus: tool mới do nhóm tự xây |  |  |  |

## B6. Safety review

- Agent có bao giờ tự đoán asset ID hoặc employee ID không?
- Trace/ticket có chứa password, MFA code, token hay dữ liệu thật không?
- Ticket chỉ được tạo sau xác nhận rõ chưa?
- Tool result error nào cần review thủ công?

## B7. Technical reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào không thể chỉ nhìn automatic score?
- Nếu có thêm một vòng, nhóm sẽ thử hypothesis nào?

# PHẦN C — Checkout trước khi nộp

Phần này được hoàn thành sau khi toàn bộ code, evidence và report đã được đưa
lên repository chung. Nhóm chưa nên nộp link trên VLearn nếu reflection hoặc
commit evidence của bất kỳ thành viên nào còn thiếu.

## C1. Nhận xét chung của nhóm

Hoàn thành mục nhận xét chung trong [TEAM.md](../../TEAM.md). Dẫn tới các run, file và commit trong phần B để chứng minh kết quả. Ghi dưới đây đường dẫn tới mục đã hoàn thành:

> Link:

## C2. INDIVIDUAL của từng thành viên

Mỗi người tự viết và commit mục INDIVIDUAL của mình trong [TEAM.md](../../TEAM.md), nêu phần việc, bằng chứng kỹ thuật và điều đã học. Không yêu cầu chép lại cùng nội dung ở đây. Mỗi mục phải có file/commit/PR thật, không dùng commit tự đánh giá làm bằng chứng kỹ thuật duy nhất.

> Link các mục INDIVIDUAL:

## C3. Final checkout

Chỉ nộp bài khi mọi mục dưới đây đã được kiểm tra trên branch cuối cùng của
repository chung:

- [ ] `TEAM.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [ ] Mỗi thành viên có ít nhất một commit trong lịch sử branch nộp bài.
- [ ] Phần nhận xét chung trong TEAM.md đã hoàn thành và có evidence.
- [ ] Mỗi thành viên đã tự viết và commit mục INDIVIDUAL trong TEAM.md.
- [ ] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [ ] Không có `.env`, API key, token, dữ liệu thật, cache hoặc generated ticket.
- [ ] Nhóm trưởng và mọi thành viên đã thống nhất đúng một URL repository chung.
- [ ] Nhóm trưởng và mọi thành viên sẽ nộp cùng URL đó trên VLearn.

**URL repository chung dùng để nộp:**

> URL:

- [ ] Tên repo đúng mẫu K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling.
- [ ] Kiểm tra deadline và bản chốt theo [SUBMISSION.md](../../SUBMISSION.md).
