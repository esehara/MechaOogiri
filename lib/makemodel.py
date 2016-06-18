from gensim.models import word2vec
def save_model():
    sentence = word2vec.Text8Corpus("../resource/oogiri_wakati.txt")
    result_model = word2vec.Word2Vec(sentence)
    result_model.save("../resource/oogiri_gensim.model")


if __name__ == "__main__":
    save_model()
