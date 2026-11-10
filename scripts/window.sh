# Window hook for .github/scripts/capture-windows.sh: Alacritty runs the shared session
# from docs/PREVIEWS.md with each theme.
# Requires: alacritty, fastfetch, eza.
# shellcheck shell=bash
name=Alacritty

launch() {
  printf '[general]\nimport = ["%s"]\n[font]\nsize = 11\nnormal.family = "%s"\n[window]\npadding = { x = 8, y = 8 }\n' \
    "$root/themes/kanagawa-$1.toml" "$font" >"$work/alacritty-$1.toml"
  printf 'alacritty --config-file %s --title kanagawa -e %s %s' "$work/alacritty-$1.toml" "$session" "$1"
}
