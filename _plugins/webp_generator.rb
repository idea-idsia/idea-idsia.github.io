# Generates .webp counterparts for all JPEG/PNG images in the site output.
# Runs after every Jekyll build — locally and in CI — so no WebP files need
# to be committed to git. New images are handled automatically on next build.
#
# Images are also resized to the maximum useful display width (× 2 for retina)
# based on directory. cwebp never upscales, so small images stay at their
# original size.
#
# Requirements: cwebp (brew install webp / apt-get install -y webp)

# Max width per directory (2× the largest display size in that context).
WEBP_MAX_WIDTHS = {
  %r{/people/}   => 480,   # person cards: ~220px display
  %r{/projects/} => 800,   # project cards: ~400px display
  %r{/software/} => 800,   # software cards: ~400px display
}.freeze
WEBP_DEFAULT_MAX_WIDTH = 1600  # hero / other root images: full-width

Jekyll::Hooks.register :site, :post_write do |site|
  cwebp = `which cwebp 2>/dev/null`.strip
  if cwebp.empty?
    Jekyll.logger.warn "WebP:", "cwebp not found — skipping (install: brew install webp)"
    next
  end

  pattern = File.join(site.dest, "assets", "images", "**", "*.{jpg,jpeg,png}")
  generated = 0
  Dir.glob(pattern).each do |src|
    webp = src.sub(/\.(jpg|jpeg|png)\z/i, ".webp")
    next if File.exist?(webp)

    max_w = WEBP_MAX_WIDTHS.find { |pat, _| src.match?(pat) }&.last || WEBP_DEFAULT_MAX_WIDTH
    # -resize width 0 → scale to width, preserve aspect ratio; cwebp never upscales
    ok = system(cwebp, "-q", "95", "-resize", max_w.to_s, "0", src, "-o", webp, "-quiet",
                out: File::NULL, err: File::NULL)
    generated += 1 if ok
  end
  Jekyll.logger.info "WebP:", "generated #{generated} file(s)" if generated > 0
end
