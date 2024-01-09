from gensim.models import Word2Vec
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def train_word2vec_model(word_list, vector_size=100, window=1, min_count=1, workers=4):
    model = Word2Vec(word_list, vector_size=vector_size, window=window, min_count=min_count, workers=workers)
    model.train(word_list, total_examples=len(word_list), epochs=10)
    return model


def sentence_vector(sentence, model):
    tokens = [token.strip() for token in re.split(r'\s|,', sentence) if token.strip()]
    print("tokens: ", tokens)
    # 단어 벡터 추출
    word_vectors = [model.wv.get_vector(token) for token in tokens if token in model.wv]
    print("word_vectors: ", word_vectors)
    if word_vectors:
        avg_vector = np.mean(word_vectors, axis=0)
        return avg_vector
    else:
        return None


def most_similar_word_to_sentence(sentence, model):
    input_vector = sentence_vector(sentence, model)
    print("input_vector: ", input_vector)
    if input_vector is not None:
        similarities = cosine_similarity([input_vector], model.wv.vectors)
        most_similar_index = np.argmax(similarities)
        most_similar_word = model.wv.index_to_key[most_similar_index]
        return most_similar_word
    else:
        return None


def read_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 각 줄을 쉼표로 구분된 단어 리스트로 변환
    word_list = [word.strip() for line in lines for word in line.split(',')]
    return word_list


def main2(user_input):
    # 메모장 파일에서 단어 리스트 읽어오기
    word_list = read_word_list('list.txt')

    # Word2Vec 모델 훈련
    model = train_word2vec_model(word_list)

    # 가장 근사한 단어 찾기
    result_word = most_similar_word_to_sentence(user_input, model)

    if result_word is not None:
        print(f"입력한 문장의 평균 벡터와 가장 유사한 단어: {result_word}")
    else:
        print("입력한 문장에 대한 벡터를 계산할 수 없습니다.")
