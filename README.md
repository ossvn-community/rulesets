# OSSVN Rulesets

Version-control các GitHub Ruleset recipe của OSSVN.

**Repo này không tự enforce rule.** Ruleset active thật nằm trong GitHub Organization hoặc Repository Settings.

## Structure

```text
repository/
├── baseline.json
├── r0-content.json
├── r1-low-risk.json
├── r2-production.json
└── r3-critical.json

organization/
├── baseline.json
├── r0-content.json
├── r1-low-risk.json
├── r2-production.json
└── r3-critical.json

examples/
└── required-checks.json
```

## Hai lớp rule

- `baseline.json` - bảo vệ default branch: không delete, không force push, merge qua Pull Request và resolve review conversation.
- `r0` đến `r3` - mức độ review theo risk level.

Required status checks không nằm trong R0-R3. Mỗi repository cấu hình checks riêng dựa trên workflow thực tế của chính repo đó.

Tên branch dùng convention `<type>/<short-kebab-case>` với các type chung như `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`. Đây là convention, không enforce bằng ruleset.

## Required Checks

`examples/required-checks.json` là mẫu để tạo ruleset required checks riêng cho từng repository. File này không được import nguyên trạng cho mọi repo.

Trước khi cấu hình:

1. Mở một Pull Request thử để workflow của repo chạy ít nhất một lần.
2. Xác nhận tên check thực tế đã xuất hiện và pass.
3. Copy `examples/required-checks.json`.
4. Sửa `name` và danh sách `required_status_checks` cho đúng repo.
5. Import JSON đã sửa vào `Settings > Rules > Rulesets` của repository.
6. Kiểm tra target là default branch, sau đó mới chuyển enforcement sang Active.

Ví dụ `community` có hai check `validate` và `links`, giữ:

```json
"required_status_checks": [
  { "context": "validate" },
  { "context": "links" }
]
```

Ví dụ `rulesets` chỉ có `validate`, sửa thành:

```json
"required_status_checks": [
  { "context": "validate" }
]
```

Repo `.github` hiện chưa có automated check, vì vậy không cần tạo Required Checks ruleset.

Không thêm `test`, `build`, `security`, `links` hoặc bất kỳ context nào chỉ vì tên nghe hợp lý. Chỉ require check thực sự tồn tại và đã chạy thành công trong repository đó.

## Cách dùng

### GitHub Free

Cho mỗi public repository:

1. Import `baseline.json`.
2. Import risk recipe phù hợp nếu muốn enforce mức review tương ứng.
3. Chạy Pull Request thử để các workflow cần thiết xuất hiện và pass.
4. Nếu repo có automated checks cần bắt buộc, copy và sửa `examples/required-checks.json`, rồi import ruleset đã sửa.

### GitHub Team hoặc Enterprise

Organization recipes là starting point. Cấu hình target repository hoặc `risk_level` trong GitHub Settings trước khi activate.

## Safety

- Recipe trong source repository luôn để `disabled`.
- Không require status check chưa từng chạy.
- Chỉ activate đúng một risk ruleset cho mỗi repository.
- Review thay đổi ruleset như thay đổi hạ tầng.
- Test recipe thay đổi behavior trên repo thử trước khi áp dụng rộng.

## Contribution

Đọc [CONTRIBUTING.md](CONTRIBUTING.md) và chạy `python scripts/validate.py` trước khi mở PR.

## License

Repo `rulesets` dùng MIT License.
