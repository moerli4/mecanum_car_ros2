#!/usr/bin/env bash
set -euo pipefail

# CONFIG: mapping old -> new
declare -A MAP=(
  ["motor_pkg"]="motor_drivers"
  ["peripherals_pkg"]="peripherals_drivers"
  ["sensor_pkg"]="sensor_drivers"
  ["headlight_pkg"]="headlight_drivers"
  ["camera_pkg"]="camera_drivers"
)

# Tools required: git, sed, grep (or rg optional)
USE_RG=false
if command -v rg >/dev/null 2>&1; then
  USE_RG=true
fi

DRY_RUN=true
if [ "${1:-}" = "--apply" ]; then
  DRY_RUN=false
  echo "Running in APPLY mode — changes will be made."
else
  echo "Dry run (no changes). To apply, re-run with: ./rename_pkgs.sh --apply"
fi

# Helper: replace in files (prints what would be changed)
replace_in_files() {
  local old="$1" new="$2"
  if $USE_RG; then
    if $DRY_RUN; then
      echo "Will replace occurrences of '$old' -> '$new' in these files:"
      rg -n --hidden -S --no-ignore-vcs -g '!.git' "$old" || true
    else
      echo "Replacing occurrences of '$old' -> '$new' ..."
      rg -l --hidden -S --no-ignore-vcs -g '!.git' "$old" | xargs -r sed -i "s/${old}/${new}/g"
    fi
  else
    if $DRY_RUN; then
      echo "Will replace occurrences of '$old' -> '$new' in these files:"
      grep -RIn --binary-files=without-match --exclude-dir=.git --exclude-dir=build --exclude-dir=install --exclude-dir=log "$old" . || true
    else
      echo "Replacing occurrences of '$old' -> '$new' ..."
      grep -RIl --binary-files=without-match --exclude-dir=.git --exclude-dir=build --exclude-dir=install --exclude-dir=log "$old" . \
        | xargs -r sed -i "s/${old}/${new}/g"
    fi
  fi
}

for old in "${!MAP[@]}"; do
  new="${MAP[$old]}"

  # 1) git mv directory if exists
  if [ -d "$old" ]; then
    echo "Directory '$old' exists."
    if $DRY_RUN; then
      echo "Would run: git mv \"$old\" \"$new\""
    else
      echo "Running: git mv \"$old\" \"$new\""
      git mv "$old" "$new"
    fi
  else
    echo "Directory '$old' NOT found; skipping git mv."
  fi

  # 2) Replace occurrences in files under workspace (skip .git/build/install)
  replace_in_files "$old" "$new"

  # 3) If Python package/module dir inside new package still named old, rename it
  if [ -d "$new" ]; then
    if [ -d "$new/$old" ]; then
      if $DRY_RUN; then
        echo "Would rename Python module dir: \"$new/$old\" -> \"$new/$new\""
      else
        echo "Renaming Python module dir: \"$new/$old\" -> \"$new/$new\""
        git mv "$new/$old" "$new/$new"
        # also replace internal occurrences inside that module
        replace_in_files "$old" "$new"
      fi
    fi
  fi

done

echo "Done. Review changes with: git status"
if $DRY_RUN; then
  echo "To apply changes, run: ./rename_pkgs.sh --apply"
else
  echo "After review, commit with: git add -A && git commit -m \"Rename packages: *_pkg -> *_drivers\""
fi

