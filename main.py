from generate import generate_full_sentence, save_model, load_model
import Levenshtein
from collections import OrderedDict
from gensim.models import Word2Vec
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def train_word2vec_model(word_list, vector_size=100, window=1, min_count=1, workers=4):
    models = Word2Vec([word_list], vector_size=vector_size, window=window, min_count=min_count, workers=workers)
    return models


def sentence_vector(sentencess, modelss):
    tokens = [find_similar_strings(token.strip(), get_contents().split(',')) for token in re.split(r'\s|,', sentencess)
              if token.strip()]
    # 단어 벡터 추출
    word_vectors = [modelss.wv.get_vector(token) for token in tokens if token in modelss.wv]
    if word_vectors:
        avg_vector = np.mean(word_vectors, axis=0)
        return avg_vector
    else:
        return None


def most_similar_word_to_sentence(sentencesss, modelsss):
    input_vector = sentence_vector(sentencesss, modelsss)
    if input_vector is not None:
        similarities = cosine_similarity([input_vector], modelsss.wv.vectors)
        most_similar_index = np.argmax(similarities)
        most_similar_word = modelsss.wv.index_to_key[most_similar_index]
        return most_similar_word
    else:
        return None


def read_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as files:
        lines = files.readlines()
    # 각 줄을 쉼표로 구분된 단어 리스트로 변환
    word_list = [word.strip() for line in lines for word in line.split(',')]
    return word_list


def split_korean(text):
    # 한글 글자를 자모 단위로 분리하는 함수
    results = []
    for char in text:
        if '가' <= char <= '힣':
            # 한글인 경우 자모 분리
            char_code = ord(char) - 0xAC00
            jong = char_code % 28
            jung = ((char_code - jong) // 28) % 21
            cho = ((char_code - jong) // 28) // 21
            results.extend([chr(0x1100 + cho), chr(0x1161 + jung)])
            if jong > 0:
                results.append(chr(0x11A7 + jong))
        else:
            # 한글이 아닌 경우 그대로 추가
            results.append(char)
    return results


def levenshtein_distance(str1, str2):
    # 레벤슈타인 거리를 계산하는 함수
    return Levenshtein.distance(str1, str2)


def find_similar_strings(input_texts, candidate_lists):
    input_split = split_korean(input_texts)

    # 입력값과 각 후보 문자열의 레벤슈타인 거리를 계산
    distances = [(candidate, levenshtein_distance(input_split, split_korean(candidate))) for candidate in
                 candidate_lists]

    # 거리가 가장 짧은 순으로 정렬
    distances.sort(key=lambda x: x[1])

    # 가장 가까운 문자열 반환
    return distances[0][0]


def main(input_text):
    contentsss = get_contents()
    candidate_list = contentsss.split(',')
    result = find_similar_strings(input_text, candidate_list)
    return result


def main2(user_input):
    # 메모장 파일에서 단어 리스트 읽어오기
    word_list = read_word_list('list.txt')

    # Word2Vec 모델 훈련
    modelssss = train_word2vec_model(word_list)

    # 가장 근사한 단어 찾기
    result_word = most_similar_word_to_sentence(user_input, modelssss)

    if result_word is not None:
        print(generate_full_sentence(result_word))
    else:
        print("입력한 문장에 대한 벡터를 계산할 수 없습니다.")


with open('list.txt', 'r', encoding='UTF8') as file:
    contents = file.read()


def get_contents():
    return contents


file2 = open('list.txt', 'a', encoding='UTF8')
model = load_model('model.json')
model2 = load_model('model2.json')

while True:
    mode = input("1. (대화)개발중\n2. 키워드-문장 생성\n3. 학습\n: ")
    if mode == '1':
        value = input("입력: ")
        main2(value)
    elif mode == '2':
        while True:
            value = input("입력(0으로 나가기): ")
            if value == '0':
                break
            result1 = main(value)
            generate_full_sentence(result1)
    elif mode == '3':
        with open('learn.txt', 'r', encoding='UTF8') as file3:
            value = file3.read()

        pattern = re.compile(r'[(\[{<][^(\[{<>]*[)\]}>]')
        value = value.replace("'", "").replace('"', '')
        value = value.replace('\t', ' ')

        while re.search(pattern, value):
            value = re.sub(pattern, '', value)
        sentences = re.split(r'\.(?!\d)', value)
        sentenceslist = []
        for i in sentences:
            sentenceslist += re.split(r'[!?:;\'"(){}\[\]/|\\+=\-*\n]+', i)
            sentenceslist += re.split(r'\.(?!\d)', i)
        sentenceslist = list(OrderedDict.fromkeys(filter(None, sentenceslist)))
        for sentence in sentenceslist:
            words = re.split(r'[,!?:;\'"(){}\[\]/|\\+=\-*\n\s]+', sentence)
            words = list(OrderedDict.fromkeys(filter(None, words)))
            for i in range(len(words) - 1):
                w = words[i]
                words[i] = w.split(r'\n')
                words[i] = list(OrderedDict.fromkeys(words[i]))
                words[i] = ' '.join(words[i])
                contents += ',' + words[i]
                if words[i] not in model:
                    model[words[i]] = {}
                if words[i + 1] not in model[words[i]]:
                    model[words[i]][words[i + 1]] = 0
                model[words[i]][words[i + 1]] += 0.000001
                print(words[i], words[i + 1], end=' ')
            for i in range(len(words) - 1):
                if words[1] not in model2:
                    model2[words[1]] = {}
                if words[i + 1] not in model2[words[1]]:
                    model2[words[1]][words[i + 1]] = 0
                model2[words[1]][words[i + 1]] += 0.000001
            print()
        save_model('model.json', model)
        save_model('model2.json', model2)
        contents = contents.split(',')
        contents = set(contents)
        contents = ",".join(contents)
        file2.write(contents)
    else:
        file2.close()
        break
print("Bye!")
