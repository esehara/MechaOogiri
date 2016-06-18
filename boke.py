# -*- coding: utf-8 -*-
from gensim.models import word2vec
import MeCab
import random
model = word2vec.Word2Vec.load("./resource/oogiri_gensim.model")
tagger = MeCab.Tagger("-Ochasen")
LIMIT = 30


def word_and_kind_parse(line):
    line_word = line.split("\t")
    if len(line_word) < 2:
        return None
    w, _, _, k, _, _ = line_word
    k = k.split(u"-")[0]
    if k == u"助詞":
        return None
    return w, k


def word_choice(words):
    random.shuffle(words)
    return words[0::(random.randint(1, 2))]


def question(text, pre=None, after=None, p_or_a=None, simple=False, bokelast=[], return_boke=False):
    bokes = []
    for x in range(LIMIT):
        text = "".join(
            filter(lambda x: x != u"、" and x != u"。", [c for c in text]))
        result = tagger.parse(text).split('\n')
        result = map(lambda x: x[0],
                     filter(lambda x: x,
                            [word_and_kind_parse(l) for l in result]))
        result = word_choice(list(result))
        boke_text = s(result, pre, after, p_or_a, simple, bokelast)
        bokes.append(boke_text)
    if return_boke:
        return [b for b in bokes if b]

def s(words, pre, after, p_or_a, simple, bokelast, negative=[], recur=True):
    try:
        word_and_kind = WordManager.parse(words, negative)
        boke_text = boke(word_and_kind, pre, after, p_or_a, simple, bokelast)
        if recur:
            for word in [w for w, _ in word_and_kind]:
                return s([w], pre, after, simple, p_or_a, bokelast, [], False)
        return boke_text
    except KeyError:
        pass


class WordManager(object):

    def __init__(self, words):
        words = list(words)
        self.set_noum(words)
        self.set_v(words)
        self.set_adv(words)
        self.set_interj(words)
        self.joshi = [u"の", u"は", u"が", u"を"]
        random.shuffle(self.joshi)

    def set_noum(self, words):
        self.noum = list(filter(lambda x: x[1] == u"名詞", words))
        random.shuffle(self.noum)

    def set_v(self, words):
        self.v = list(filter(lambda x: x[1] == u"動詞", words))
        random.shuffle(self.v)

    def set_adv(self, words):
        self.adv = list(filter(lambda x: x[1] == u"副詞", words))
        random.shuffle(self.adv)

    def set_interj(self, words):
        self.interj = list(filter(lambda x: x[1] == u"感動詞", words))
        random.shuffle(self.adv)

    @classmethod
    def parse(self, words, negative=[]):
        most_similar = [w for w in model.most_similar(
            positive=words, negative=negative)]
        return filter(
            lambda x: x,
            [word_kind(m) for m, _ in most_similar])

    def choice_interj(self, tried_time=0):
        try:
            interj = self.adv.pop()[0]
            while (interj in choiced_word):
                interj = self.adv.pop()[0]
            choiced_word.append(interj)
            return interj
        except IndexError:
            random.shuffle(choiced_word)
            if not len(choiced_word):
                return ""
            self.set_interj(self.parse([choiced_word[0]]))
            if tried_time < 10:
                return self.choice_interj(tried_time + 1)
            else:
                return ""

    def choice_adv(self, tried_time=0):
        try:
            adv = self.adv.pop()[0]
            while (adv in choiced_word):
                adv = self.adv.pop()[0]
            choiced_word.append(adv)
            return adv
        except IndexError:
            random.shuffle(choiced_word)
            self.set_adv(self.parse([choiced_word[0]]))
            if tried_time < 10:
                return self.choice_adv(tried_time + 1)
            else:
                return ""

    def choice_noum(self):
        try:
            noum = self.noum.pop()[0]
            while (noum in choiced_word):
                noum = self.noum.pop()[0]
            choiced_word.append(noum)
            return noum
        except IndexError:
            random.shuffle(choiced_word)
            self.set_noum(self.parse([choiced_word[0]]))
            return self.choice_noum()

    def choice_v(self, tried_time=0):
        try:
            v = self.v.pop()[0]
            while (v in choiced_word):
                v = self.v.pop()[0]
            choiced_word.append(v)
            return v
        except IndexError:
            seed = choiced_word + self.noum
            random.shuffle(seed)
            self.set_v(self.parse([seed[0][0]]))
            if tried_time < 10:
                return self.choice_v(tried_time + 1)
            else:
                return ""

    def choice_joshi(self):
        return self.joshi.pop()


class BokePattern:

    @classmethod
    def prefix_pattern(cls):
        s = [
            [],
            [u"感動詞"],
            [u"感動詞", u"副詞"],
            [u"副詞"]
        ]
        random.shuffle(s)
        return s.pop()

    @classmethod
    def subject_pattern(cls):
        s = [
            [u"名詞"],
            [u"名詞", u"名詞"],
            [u"名詞", u"の", u"名詞"],
            [u"動詞"]
        ]
        random.shuffle(s)
        return s.pop()

    @classmethod
    def connect_rep(cls):
        c = [
            [u"が"],
            [u"を"],
            [u"は"],
            [u""],
        ]
        random.shuffle(c)
        return c.pop()

    @classmethod
    def subord_pattern(cls):
        s = [
            [u"名詞"],
            [u"名詞", u"助詞", u"名詞"],
            [u"動詞"],
        ]
        random.shuffle(s)
        return s.pop()

    @classmethod
    def simple_or_complex(cls, simple):
        s = [(
            cls.subject_pattern() +
            cls.connect_rep() +
            cls.subord_pattern()),
            cls.subject_pattern()]
        if simple:
            choiced = s[1]
        else:
            random.shuffle(s)
            choiced = s.pop()

        prefix_flag = random.randint(0, 1)
        if prefix_flag:
            choiced = cls.prefix_pattern() + choiced

        return choiced

    @classmethod
    def choice(cls, simple=False):
        return cls.simple_or_complex(simple)


choiced_word = []
def boke(words, pre, after, p_or_a, simple, bokelast):
    w = WordManager(words)
    boke_str = u""
    for word_kind in (BokePattern.choice(simple) + bokelast):
        if word_kind == u"名詞":
            boke_str += w.choice_noum()
        elif word_kind == u"助詞":
            boke_str += w.choice_joshi()
        elif word_kind == u"動詞":
            boke_str += w.choice_v()
        elif word_kind == u"副詞":
            boke_str += w.choice_adv()
        elif word_kind == u"感動詞":
            pre_boke = w.choice_interj()
            if pre_boke != "":
                boke_str += pre_boke + "、"
        else:
            boke_str += word_kind

    if pre:
        boke_str = pre + boke_str
    if after:
        boke_str += after
    if p_or_a:
        p_a_flag = random.randint(0, 1)
        if p_a_flag:
            boke_str += p_or_a
        else:
            boke_str = p_or_a + boke_str

    print(boke_str)
    return boke_str


def word_kind(m):
    try:
        w, k = mecab_result(m)
        kind = k.split(u"-")[0]
        return w, kind
    except TypeError:
        return None


def mecab_result(word):
    try:
        result = tagger.parse(word)
        w, _, _, k, subk, _ = result.split(u"\t")
        return w, k
    except ValueError:
        pass


def resave():
    sentence = word2vec.Text8Corpus("../resource/oogiri_wakati.txt")
    result_model = word2vec.Word2Vec(sentence)
    result_model.save("../resource/oogiri_gensim.model")
    model = result_model
