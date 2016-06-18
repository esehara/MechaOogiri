require 'csv'

original_data = {
  wikipedia: 'jawiki-latest-all-titles-in-ns0',
  hatena: 'keywordlist_furigana.csv'
}

# Source code for 
# http://qiita.com/ynakayama/items/388c82cbe14c65827769


CSV.open("custom.csv", 'w') do |csv|
  original_data.each do |type, filename|
    next unless File.file? filename
    open(filename).each do |title|
      title.strip!

      next if title =~ %r(^[+-.$()?*/&%!"'_,]+)
      next if title =~ /^[-.0-9]+$/
      next if title =~ /曖昧さ回避/
      next if title =~ /_\(/
      next if title =~ /^PJ:/
      next if title =~ /の登場人物/
      next if title =~ /一覧/

      title_length = title.length

      if title_length > 3
        score = [-36000.0, -400 * (title_length ** 1.5)].max.to_i
        csv << [title, nil, nil, score, '名詞', '一般', '*', '*', '*', '*', title, '*', '*', type]
      end
    end
  end
end
