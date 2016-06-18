require 'natto'
nm = Natto::MeCab.new
FILENAME = "bokete.txt"
LIMIT = 1000000

def from_csv file
  LIMIT.times do
    l = file.gets
    next if l.nil?
    no, title, answer, _, _ = l.split(',')
    text = title.to_s + answer.to_s
    text = "" if answer == "投稿なし" || text.nil?
    wakati_line l
  end
end

def from_txt file
  LIMIT.times do
    l = file.gets
    next if l.nil?
    wakati_line l
  end
end

def wakati_line l
  nm_result = nm.parse(text)
  puts nm_result.split("\n")
        .map {|line| line.split("\t")}
        .select {|line| line.size > 1}
        .map { |line|
    raw = line[1].split(",")[-3]
    raw == "*" ? line[0] : raw
  }.to_a.join(" ")
end

open(FILENAME) do |file|
  from_txt file
end
