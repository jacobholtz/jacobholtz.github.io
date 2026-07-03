source "https://rubygems.org"

# NOTE: intentionally NOT the `github-pages` gem — it pins Jekyll 3.9,
# which relies on Ruby APIs (String#tainted?, default-gem CSV, etc.) that
# modern Ruby has removed, making local builds fail. GitHub's classic Pages
# build service runs its own fixed Jekyll version server-side regardless of
# this Gemfile, so this only affects local `jekyll serve`/`build` previews.
# Every plugin below is on GitHub Pages' supported-plugins allowlist.
gem "jekyll", "~> 4.3"

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
end

# Windows/JRuby compatibility shims some environments need for Jekyll.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
