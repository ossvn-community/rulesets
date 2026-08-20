from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "baseline.json",
    "r0-content.json",
    "r1-low-risk.json",
    "r2-production.json",
    "r3-critical.json",
}
RISK_RECIPES = {
    "r0-content.json",
    "r1-low-risk.json",
    "r2-production.json",
    "r3-critical.json",
}
SOURCES = {
    "repository": "Repository",
    "organization": "Organization",
}
ORG_PLACEHOLDERS = {
    "r0-content.json": "__SET_RISK_LEVEL_R0_BEFORE_ACTIVATION__",
    "r1-low-risk.json": "__SET_RISK_LEVEL_R1_BEFORE_ACTIVATION__",
    "r2-production.json": "__SET_RISK_LEVEL_R2_BEFORE_ACTIVATION__",
    "r3-critical.json": "__SET_RISK_LEVEL_R3_BEFORE_ACTIVATION__",
}
REQUIRED_KEYS = {
    "name",
    "target",
    "source_type",
    "enforcement",
    "conditions",
    "rules",
}


def validate_recipe(path: Path, expected_source: str) -> list[str]:
    errors: list[str] = []
    relative = path.relative_to(ROOT)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{relative}: invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return [f"{relative}: recipe root must be an object"]

    missing = REQUIRED_KEYS - data.keys()
    if missing:
        errors.append(f"{relative}: missing keys: {', '.join(sorted(missing))}")
        return errors

    if not isinstance(data["name"], str) or not data["name"].strip():
        errors.append(f"{relative}: name must be a non-empty string")

    if data["target"] != "branch":
        errors.append(f"{relative}: target must be 'branch'")

    if data["source_type"] != expected_source:
        errors.append(
            f"{relative}: source_type must be '{expected_source}' for this folder"
        )

    if data["enforcement"] != "disabled":
        errors.append(f"{relative}: enforcement must remain 'disabled' in recipe files")

    conditions = data["conditions"]
    if not isinstance(conditions, dict):
        errors.append(f"{relative}: conditions must be an object")
    else:
        ref_name = conditions.get("ref_name")
        if not isinstance(ref_name, dict):
            errors.append(f"{relative}: conditions.ref_name must be an object")
        elif "~DEFAULT_BRANCH" not in ref_name.get("include", []):
            errors.append(f"{relative}: ref_name.include must contain ~DEFAULT_BRANCH")

        if path.parent.name == "organization":
            repository_name = conditions.get("repository_name")
            if not isinstance(repository_name, dict):
                errors.append(f"{relative}: conditions.repository_name must be an object")
            else:
                include = repository_name.get("include")
                if path.name == "baseline.json":
                    if include != ["~ALL"]:
                        errors.append(
                            f"{relative}: baseline repository_name.include must be ['~ALL']"
                        )
                else:
                    expected_placeholder = ORG_PLACEHOLDERS[path.name]
                    if include != [expected_placeholder]:
                        errors.append(
                            f"{relative}: repository_name.include must be [{expected_placeholder!r}]"
                        )

    rules = data["rules"]
    if not isinstance(rules, list) or not rules:
        errors.append(f"{relative}: rules must be a non-empty list")
    else:
        rule_types = []
        for index, rule in enumerate(rules):
            if not isinstance(rule, dict) or not isinstance(rule.get("type"), str):
                errors.append(f"{relative}: rules[{index}] must have a string type")
            else:
                rule_types.append(rule["type"])

        if path.name in RISK_RECIPES and "required_status_checks" in rule_types:
            errors.append(
                f"{relative}: risk recipes must not hard-code required_status_checks"
            )

    bypass_actors = data.get("bypass_actors", [])
    if not isinstance(bypass_actors, list):
        errors.append(f"{relative}: bypass_actors must be a list when present")

    return errors


def validate() -> list[str]:
    errors: list[str] = []
    count = 0

    for folder, source_type in SOURCES.items():
        directory = ROOT / folder
        if not directory.is_dir():
            errors.append(f"Missing recipe directory: {folder}")
            continue

        actual = {path.name for path in directory.glob("*.json")}
        missing = EXPECTED - actual
        unexpected = actual - EXPECTED

        if missing:
            errors.append(f"{folder}: missing recipes: {', '.join(sorted(missing))}")
        if unexpected:
            errors.append(f"{folder}: unexpected recipes: {', '.join(sorted(unexpected))}")

        for name in sorted(EXPECTED & actual):
            count += 1
            errors.extend(validate_recipe(directory / name, source_type))

    if not errors:
        print(f"Ruleset validation passed ({count} recipes).")

    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(f"- {problem}" for problem in problems))
        sys.exit(1)
