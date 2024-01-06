from collections import defaultdict
import random
import json


def load_model(file_path):
    try:
        with open(file_path, 'r') as file:
            model_data = json.load(file)
        return defaultdict(lambda: defaultdict(float), model_data)
    except FileNotFoundError:
        return defaultdict(lambda: defaultdict(float))


def save_model(file_path, model):
    with open(file_path, 'w') as file:
        json.dump({k: dict(v) for k, v in model.items()}, file)


def load_words(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split(',')
    return words


def generate_sentence(keyword, model):
    if keyword in model:
        possible_words = model[keyword]
        if possible_words:
            sorted_words = sorted(possible_words.items(), key=lambda x: x[1], reverse=True)

            # 고려할 확률의 상위 N개를 선택
            top_n = min(5, len(sorted_words))
            selected_words = random.choices(sorted_words[:top_n], k=1)

            return selected_words[0][0]

    return None


def generate(user_input):
    # 데이터 로드 및 전처리
    model = load_model('model.json')

    # 사용자로부터 키워드 입력
    keywords = user_input.split()

    # 생성된 문장 출력
    generated_word = generate_sentence(keywords[0], model)
    print(f"생성된 단어: {user_input} {generated_word}")

    # 사용자에게 평가 받기
    rating = input("1에서 10까지의 평가를 입력하세요: ")
    if not rating.isdigit():
        rating = 4
    else:
        rating = int(rating)

    if rating <= 5:
        # 사용자에게 직접 입력 받아 학습
        new_word = input("뒤에 올 가능성이 높은 단어를 입력하세요: ")
        model[keywords[0]][new_word] += 0.000001
    else:
        # 높은 등급에 따라 더 많이 학습
        if generated_word:
            model[keywords[0]][generated_word] += rating * 0.0000005 - 0.000002

    another = input("다른 경우에 올 수 있는 단어를 입력하세요: ")
    if another not in model[keywords[0]]:
        model[keywords[0]][another] = 0
    model[keywords[0]][another] += 0.000001

    # 모델 저장
    save_model('model.json', model)


def generate_full_sentence(user_input):
    # 데이터 로드 및 전처리
    model = load_model('model.json')

    # 사용자로부터 키워드 입력
    keywords = user_input.split()

    # 생성된 문장 출력
    generated_sentence = []
    generated_word = generate_sentence(keywords[0], model)
    while generated_word is not None:
        generated_sentence.append(generated_word)
        generated_word = generate_sentence(generated_word, model)
    print(f"생성된 문장: {user_input} {generated_sentence}")
