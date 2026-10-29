module Jekyll
  # Gives every publication a meta description. Without one, jekyll-seo-tag
  # falls back to the page excerpt, which for publications is the "BibTeX"
  # heading. Uses the abstract when present, otherwise a short citation line.
  class PublicationDescription < Generator
    safe true
    priority :low

    MAX_LENGTH = 155

    TYPE_LABELS = {
      'journal' => 'Journal article',
      'conference' => 'Conference paper',
      'workshop' => 'Workshop paper',
      'book_chapter' => 'Book chapter',
      'abstract' => 'Abstract',
      'misc' => 'Publication'
    }.freeze

    def generate(site)
      collection = site.collections['publications']
      return unless collection

      collection.docs.each do |doc|
        next unless doc.data['description'].to_s.strip.empty?

        doc.data['description'] = describe(doc.data)
      end
    end

    private

    def describe(data)
      abstract = data['abstract'].to_s.gsub(/<[^>]*>/, ' ').gsub(/\s+/, ' ').strip
      return truncate(abstract) unless abstract.empty?

      citation(data)
    end

    def citation(data)
      key = data['type'].to_s.strip
      type = TYPE_LABELS.fetch(key) { key.empty? ? 'Publication' : key.tr('_-', '  ').capitalize }
      authors = Array(data['authors']).compact.map(&:to_s).reject(&:empty?)
      text = type.dup
      text << " by #{authors.first}#{' et al.' if authors.size > 1}" unless authors.empty?
      details = [data['venue'], data['year']].map(&:to_s).reject(&:empty?)
      text << ", #{details.join(', ')}" unless details.empty?
      "#{text}."
    end

    def truncate(text)
      return text if text.length <= MAX_LENGTH

      cut = text[0, MAX_LENGTH - 1]
      cut = cut[0, cut.rindex(' ')] if cut.rindex(' ')
      "#{cut.sub(/[\s,;:.]+\z/, '')}…"
    end
  end
end
