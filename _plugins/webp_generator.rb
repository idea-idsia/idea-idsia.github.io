# Generates .webp counterparts for all JPEG/PNG images in the site output.
# Runs after every Jekyll build — locally and in CI — so no WebP files need
# to be committed to git. New images added to assets/images/ are handled
# automatically on the next build.
#
# Requirements: cwebp (brew install webp / apt-get install -y webp)

Jekyll::Hooks.register :site, :post_write do |site|
  cwebp = `which cwebp 2>/dev/null`.strip
  if cwebp.empty?
    Jekyll.logger.warn "WebP:", "cwebp not found — skipping WebP generation (install: brew install webp)"
    next
  end

  pattern = File.join(site.dest, "assets", "images", "**", "*.{jpg,jpeg,png}")
  generated = 0
  Dir.glob(pattern).each do |src|
    webp = src.sub(/\.(jpg|jpeg|png)\z/i, ".webp")
    next if File.exist?(webp)
    ok = system(cwebp, "-q", "85", src, "-o", webp, "-quiet",
                out: File::NULL, err: File::NULL)
    generated += 1 if ok
  end
  Jekyll.logger.info "WebP:", "generated #{generated} file(s)" if generated > 0
end
