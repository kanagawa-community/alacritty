#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.toml from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
# The 16 ANSI colors, normal then bright.
COLORS = [f"term.{c}" for c in ANSI] + [f"term.bright_{c}" for c in ANSI]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}

def theme(variant, appearance, c):
    def table(name, keys):
        return [f"[colors.{name}]"] + [f'{k} = "{c[r]}"' for k, r in keys] + [""]

    out = [f"# Kanagawa {variant.capitalize()}", "# https://github.com/kanagawa-community/alacritty", ""]
    out += table("primary", [("background", "ui.bg"), ("foreground", "ui.fg")])
    out += table("cursor", [("text", "ui.bg"), ("cursor", "ui.fg_dim")])
    out += table("selection", [("text", "ui.fg"), ("background", "ui.bg_visual")])
    out += table("normal", [(a, f"term.{a}") for a in ANSI])
    out += table("bright", [(a, f"term.bright_{a}") for a in ANSI])
    for i, r in ((16, "term.extended_1"), (17, "term.extended_2")):
        out += ["[[colors.indexed_colors]]", f"index = {i}", f'color = "{c[r]}"', ""]
    return "\n".join(out)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.toml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(theme(v, variants[v]["appearance"], roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
