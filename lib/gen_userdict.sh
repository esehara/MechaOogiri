# Source for
# http://qiita.com/ynakayama/items/388c82cbe14c65827769

# はてなキーワード
curl -L http://d.hatena.ne.jp/images/keyword/keywordlist_furigana.csv | iconv -f euc-jp -t utf-8 > keywordlist_furigana.csv

# Wikipedia
curl -L http://dumps.wikimedia.org/jawiki/latest/jawiki-latest-all-titles-in-ns0.gz | gunzip > jawiki-latest-all-titles-in-ns0
ruby gen_userdict.rb
/usr/lib/mecab/mecab-dict-index -d /usr/share/mecab/dic/ipadic -u custom.dic -f utf-8 -t utf-8 custom.csv
