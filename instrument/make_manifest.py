"""Generate dataset.json — the machine-readable dataset card.

One record per kata package: provenance class, difficulty tier, upstream source, test count,
and oracle strength (mutation kill rate + registered-equivalent count). Regenerate after
`make mutation`; the manifest is committed so downstream studies can stratify by provenance
and cite per-package oracle error bars without running anything.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
TESTS = ROOT / "tests"

# Provenance classes:
#   translated-human-tests  — suites hand-written upstream (C#/Java), machine-translated
#                             2025, translation-repaired + mutation-hardened 2026
#   machine-from-human-spec — implementation and tests machine-authored 2026 from a
#                             human-written kata specification (paraphrased; source cited)
TRANSLATED = {
    "addition_triangulation", "advent_day6", "alarm_system", "bowling_game", "calc_stats",
    "calculator_tdd_ebook", "change_calculator", "darts", "decorator_examples", "fibonacci",
    "fibonacci_brute_force", "fibonacci_dynamic", "find_max", "find_min", "fizzbuzz_kata",
    "lcd_digits", "leap_year", "mine_fields", "money", "natural_string_sorting",
    "odd_even_kata", "password_verifier", "prime_factor", "recently_used_list",
    "roman_numerals", "stack", "string_calculator", "string_helper", "string_sum",
    "sum_example", "tennis_game", "tetris", "tic_tac_toe", "word_wrap", "xunit",
}

TIERS = {
    # legacy corpus: tiers assigned by the kata's community classification
    **dict.fromkeys(["fizzbuzz_kata", "leap_year", "string_sum", "sum_example", "find_max",
                     "find_min", "fibonacci", "fibonacci_brute_force", "fibonacci_dynamic",
                     "addition_triangulation", "string_helper", "decorator_examples",
                     "odd_even_kata", "prime_factor", "roman_numerals", "lcd_digits",
                     "calc_stats", "change_calculator", "stack", "recently_used_list",
                     "natural_string_sorting", "advent_day6"], "beginner"),
    **dict.fromkeys(["bowling_game", "string_calculator", "password_verifier", "mine_fields",
                     "word_wrap", "tennis_game", "darts", "tic_tac_toe", "alarm_system",
                     "calculator_tdd_ebook", "money"], "intermediate"),
    **dict.fromkeys(["tetris", "xunit"], "advanced"),
    # tddbuddy ingestion (catalog tiers)
    **dict.fromkeys(["hundred_doors", "anagram_detector", "balanced_brackets",
                     "conways_sequence", "end_of_line_trim", "greeting", "ip_validator",
                     "last_sunday", "metric_converter", "numbers_to_words",
                     "recipe_calculator", "rock_paper_scissors", "time_zone_converter"],
                    "beginner"),
    **dict.fromkeys(["age_calculator", "bank_account", "bank_ocr", "character_copy",
                     "clam_card", "code_breaker", "diamond", "heavy_metal_bake_sale",
                     "library_management", "linked_list", "mars_rover", "maze_walker",
                     "memory_cache", "pagination", "parking_lot", "robot_factory",
                     "shopping_cart", "social_network", "timesheet_calculator", "url_parts",
                     "url_shortener"], "intermediate"),
    **dict.fromkeys(["bingo", "circuit_breaker", "csv_query_engine", "event_sourcing",
                     "fluent_calculator", "game_of_life", "gilded_rose", "jelly_vs_tower",
                     "kata_potter", "laundry_reservation", "markdown_parser", "poker_hands",
                     "rate_limiter", "snake_game", "string_transformer",
                     "supermarket_pricing", "text_justification", "video_club_rental",
                     "weather_station", "zombie_survivor"], "advanced"),
}


def source_for(pkg: str) -> str:
    text = " ".join(f.read_text() for f in (SRC / pkg).glob("*.py"))
    m = re.search(r"tddbuddy\.com/katas/[\w-]+", text)
    if m:
        return f"https://www.{m.group(0)}"
    if pkg in ("money", "xunit"):
        return "Kent Beck, Test-Driven Development: By Example (reimplemented from the book's spec)"
    if pkg == "tetris":
        return "https://github.com/luontola/tdd-tetris-tutorial"
    if pkg == "darts":
        return "https://github.com/danidemi/tutorial-java-tdd"
    if pkg in TRANSLATED:
        return "https://github.com/garora/TDD-Katas (or per-file docstring credit)"
    return "per-file docstring"


def count_tests(pkg: str) -> int:
    total = 0
    for f in TESTS.glob("test_*.py"):
        text = f.read_text()
        if re.search(rf"\bfrom {pkg}[.\s]|\bimport {pkg}\b", text):
            total += len(re.findall(r"^def test_", text, re.M))
    return total


def main() -> None:
    scores = json.loads((ROOT / "instrument" / "mutation_scores.json").read_text())
    equiv_text = (ROOT / "instrument" / "equivalent_mutants.md").read_text()

    packages = sorted(p.name for p in SRC.iterdir()
                      if p.is_dir() and p.name != "__pycache__")
    records = []
    for pkg in packages:
        s = scores["packages"].get(pkg, {})
        survivors = s.get("survived", 0)
        registered = len(re.findall(rf"^## .*\b{pkg}\b|\b{pkg}\b.*—", equiv_text, re.M))
        req = ROOT / "requirements" / f"{pkg}.md"
        records.append({
            "package": pkg,
            "requirements": f"requirements/{pkg}.md" if req.is_file() else None,
            "tier": TIERS.get(pkg, "unclassified"),
            "provenance": ("translated-human-tests" if pkg in TRANSLATED
                           else "machine-from-human-spec"),
            "source": source_for(pkg),
            "tests": count_tests(pkg),
            "mutants": s.get("mutants"),
            "mutation_kill_rate": s.get("kill_rate"),
            "surviving_mutants": survivors,
            "survivors_registered_equivalent": survivors == 0 or registered > 0,
        })

    manifest = {
        "dataset": "tdd-dataset-py",
        "requirements_protocol": "requirements/PROTOCOL.md",
        "description": "TDD kata corpus with mutation-measured oracle strength; suites "
                       "serve as held-out oracles for evaluating agentic coding systems.",
        "license": "MIT (original code); kata concepts are community material, attributed",
        "packages": len(records),
        "total_tests": sum(r["tests"] for r in records),
        "overall_mutation_kill_rate": scores["overall"]["kill_rate"],
        "provenance_classes": {
            "translated-human-tests": sum(1 for r in records
                                          if r["provenance"] == "translated-human-tests"),
            "machine-from-human-spec": sum(1 for r in records
                                           if r["provenance"] == "machine-from-human-spec"),
        },
        "records": records,
    }
    out = ROOT / "dataset.json"
    out.write_text(json.dumps(manifest, indent=2))
    print(f"{len(records)} packages, {manifest['total_tests']} tests -> {out}")


if __name__ == "__main__":
    main()
