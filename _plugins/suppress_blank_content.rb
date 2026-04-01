module Jekyll
  # Prevents individual pages from being generated for collection documents
  # whose body content is empty. The documents still appear in the collection
  # Liquid variables (e.g. site.projects) so listing pages are unaffected.
  class SuppressBlankContent < Generator
    safe true
    priority :low

    COLLECTIONS = %w[projects publications].freeze

    def generate(site)
      COLLECTIONS.each do |name|
        collection = site.collections[name]
        next unless collection

        collection.docs.each do |doc|
          next unless doc.content.strip.empty?

          doc.define_singleton_method(:write?) { false }
        end
      end
    end
  end
end
