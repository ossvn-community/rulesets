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
```

## Cách dùng

### GitHub Free

Import recipe trong `repository/` vào từng public repo.

### GitHub Team hoặc Enterprise

Import recipe trong `organization/` và target repo bằng `risk_level` custom property.

## Safety

- Recipe mới để `disabled` cho tới khi target và required checks đã được kiểm tra.
- Không require status check chưa từng chạy.
- Review thay đổi ruleset như thay đổi hạ tầng.
- Test trên repo thử trước khi áp dụng rộng.

## Contribution

Đọc [CONTRIBUTING.md](CONTRIBUTING.md) và chạy `python scripts/validate.py` trước khi mở PR.

## License

Repo `rulesets` dùng MIT License.
