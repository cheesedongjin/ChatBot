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


def generate_sentence(original, keyword, model1, model2=None):
    def get_top_n_words(word_model, n):
        if word_model:
            sorted_words = sorted(word_model.items(), key=lambda x: x[1], reverse=True)
            return [word[0] for word in sorted_words[:n]]

        return []

    def select_word_from_model(word_model, n):
        top_n_words = get_top_n_words(word_model, n)
        return random.choice(top_n_words) if top_n_words else None

    if random.choice([True, True, True, False]):
        if keyword in model1:
            selected_word_model1 = select_word_from_model(model1[keyword], 5)

            if model2 is not None and original in model2:
                overlapping_words = set(get_top_n_words(model2[original], 5)).intersection(selected_word_model1)

                if overlapping_words:
                    return list(overlapping_words)[0]

            return selected_word_model1

    else:
        if keyword in model1:
            return select_word_from_model(model1[keyword], 5)

    return None


def generate(user_input):
    # 데이터 로드 및 전처리
    model = load_model('model.json')

    # 사용자로부터 키워드 입력
    keywords = user_input.split()

    # 생성된 문장 출력
    generated_word = generate_sentence(keywords[0], keywords[0], model)
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
    model2 = load_model('model2.json')

    # 사용자로부터 키워드 입력
    keywords = user_input.split()

    # 생성된 문장 출력
    generated_sentence = []
    length = 12
    while length > 11:
        generated_sentence = []
        length = 0
        generated_word = generate_sentence(keywords[0], keywords[0], model, model2)
        while generated_word is not None:
            generated_sentence.append(generated_word)
            length += 1
            generated_word = generate_sentence(keywords[0], generated_word, model, model2)
    print(f"생성된 문장: {user_input} {' '. join(generated_sentence)}")
    rate = input("1부터 10까지의 평가를 입력하세요: ")
    if not rate.isdigit():
        rate = 4
    rate = int(rate)
    for i in range(len(generated_sentence) - 1):
        model2[user_input][generated_sentence[i + 1]] = rate * 0.0000005 - 0.000002
    save_model('model2.json', model2)
