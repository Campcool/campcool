#!/usr/bin/env bash
set -euo pipefail

readonly output_dir="_site"

# Site policy: deny internal roots first, then allow only explicit public paths.
readonly -a deny_rules=(
  '/_site/***'
  '/work/***'
  '/.git*'
  '/.github/***'
  '/AI-Skills/***'
  '/scripts/***'
  '/*.md'
  '/*.jsx'
)
readonly -a public_rules=(
  '/.nojekyll'
  '/CNAME'
  '/favicon.ico'
  '/*.html'
  '/robots.txt'
  '/sitemap.xml'
  '/llms.txt'
  '/assets/***'
  '/areas/***'
)
readonly -a required_paths=(
  'index.html'
  'CNAME'
  'robots.txt'
  'sitemap.xml'
  'llms.txt'
  'assets'
)
readonly -a denied_paths=(
  'AI-README.md'
  'AI-Skills'
  'scripts'
  'BottomNav.jsx'
  'Header.jsx'
  'HeroSection.jsx'
  'PricingTable.jsx'
  'ProductCard.jsx'
)

mkdir -p "$output_dir"
rsync_args=(-a --delete --delete-excluded --prune-empty-dirs)
for rule in "${deny_rules[@]}"; do rsync_args+=(--exclude "$rule"); done
for rule in "${public_rules[@]}"; do rsync_args+=(--include "$rule"); done
rsync_args+=(--exclude '*')
rsync "${rsync_args[@]}" ./ "$output_dir/"

for required in "${required_paths[@]}"; do
  if [ ! -e "$output_dir/$required" ]; then
    echo "::error title=Pages artifact invalid::$required is missing from $output_dir"
    exit 1
  fi
done

for denied in "${denied_paths[@]}"; do
  if [ -e "$output_dir/$denied" ]; then
    echo "::error title=Internal path leaked::$denied must not be included in the Pages artifact"
    exit 1
  fi
done

echo "Public Pages artifact ready: $(find "$output_dir" -type f | wc -l | tr -d ' ') files"
find "$output_dir" -type f -print | sort
