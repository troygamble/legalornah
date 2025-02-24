Jekyll::Hooks.register :site, :post_write do |site|
  Dir.glob("_site/**/*.html").each do |file|
    html = File.read(file)
    unless html.include?('<meta name="description"')
      puts "⚠️ Missing meta description in #{file}"
    end
    unless html.include?('<link rel="canonical"')
      puts "⚠️ Missing canonical tag in #{file}"
    end
  end
end
