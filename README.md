# OSSVN Rulesets

Version-control các GitHub Ruleset recipe của OSSVN.

**Repo này không tự enforce rule.** Ruleset active thật nằm trong GitHub Organization hoặc Repository Settings.

## Structure

```text
repository/
├── baseline.json
├── branch-naming.json
├── r0-content.json
├── r1-low-risk.json
├── r2-production.json
└── r3-critical.json

organization/
├── baseline.json
├── branch-naming.json
├── r0-content.json
├── r1-low-risk.json
├── r2-production.json
└── r3-critical.json
```

## Ba lớp rule

- `baseline.json` - bảo vệ default branch: không delete, không force push, merge qua Pull Request và resolve review conversation.
- `branch-naming.json` - convention chung cho branch: `<type>/<short-kebab-case>` với `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`; `main` vẫn được phép.
- `r0` đến `r3` - mức độ review theo risk level.

Required status checks không nằm trong R0-R3. Mỗi repository cấu hình checks riêng dựa trên workflow thực tế của chính repo đó.

## Cách dùng

### GitHub Free

Cho mỗi public repository:

1. Import `baseline.json`.
2. Import `branch-naming.json`.
3. Import đúng một risk recipe R0-R3.
4. Chạy Pull Request thử.
5. Cấu hình required status checks trong GitHub Settings, chỉ chọn những check đã thực sự xuất hiện và pass.

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
