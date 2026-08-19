# Contributing to OSSVN Rulesets

Ruleset là configuration ảnh hưởng trực tiếp tới merge/deploy flow, vì vậy thay đổi cần nhỏ và dễ review.

## Trước khi mở PR

### 1. Kiểm tra diff

```bash
git status --short
git diff --check
git diff
```

### 2. Chạy automated checks

Từ root của repository:

```bash
python scripts/validate.py
```

### 3. Kiểm tra thủ công

- Đọc từng recipe JSON đã sửa và xác nhận `enforcement` vẫn là `disabled` trong source repository.
- Nếu sửa `required_status_checks`, đối chiếu từng `context` với tên check thực sự tồn tại ở repo sẽ áp dụng recipe.
- Nếu sửa `conditions` hoặc behavior của rule, import recipe vào một repo thử khi ruleset vẫn disabled và xác nhận GitHub chấp nhận JSON trước khi áp dụng vào repo thật.

### 4. Kết quả mong đợi

- `git diff --check` exit code bằng `0`.
- `python scripts/validate.py` in `Ruleset validation passed (10 recipes).`.
- Không recipe nào trong source repository active ngoài ý muốn.
- Recipe thay đổi behavior được GitHub chấp nhận ở repo thử trước khi activation thật.
