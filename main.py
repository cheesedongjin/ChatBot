import re
from generate import generate, generate_full_sentence, save_model, load_model
import Levenshtein


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


def developer():
    contentss = get_contents()
    candidate_list = contentss.split(',')
    while True:
        # 테스트
        input_text = input("입력(없는 단어로 나가기): ")

        result = find_similar_strings(input_text, candidate_list)
        print(f"입력값: {input_text}, 비슷한 문자열: {result}")
        if input_text not in candidate_list:
            to_addd = input("입력값이 올바른 단어입니까?(1234567890로 예, 0로 나가기): ")
            if to_addd == '1234567890':
                contentss += ',' + input_text
                candidate_list.append(input_text)
                print("\"" + input_text + "\"가 추가되었습니다.")
            elif to_addd == '0':
                break


def main(input_text):
    contentsss = get_contents()
    candidate_list = contentsss.split(',')
    result = find_similar_strings(input_text, candidate_list)
    return result


with open('list.txt', 'r') as file:
    contents = file.read()


def get_contents():
    return contents


file2 = open('list.txt', 'w')
model = load_model('model.json')

while True:
    mode = input("1. developer mode\n2. word mode\n3. sentence mode\n4. learn\n")
    if mode == '1':
        developer()
    elif mode == '2':
        value = input("입력: ")
        result1 = main(value)
        if value == result1:
            generate(result1)
        else:
            to_add = input("입력값이 올바른 단어입니까?(1234567890로 예): ")
            if to_add == '1234567890':
                contents += ',' + value
                file2.write(contents)
                print("\"" + value + "\"가 추가되었습니다.")
                generate(value)
            else:
                break
    elif mode == '3':
        value = input("입력: ")
        result1 = main(value)
        if value == result1:
            generate_full_sentence(result1)
        else:
            to_add = input("입력값이 올바른 단어입니까?(1234567890로 예): ")
            if to_add == '1234567890':
                contents += ',' + value
                file2.write(contents)
                print("\"" + value + "\"가 추가되었습니다.")
                generate_full_sentence(value)
            else:
                break
    elif mode == '4':
        with open('learn.txt', 'r', encoding='UTF8') as file3:
            value = file3.read()
        sentences = value.split(".")
        sentenceslist = []
        for i in sentences:
            sentenceslist += re.split(r'[.,!?:;\'"()]+', i)
        sentenceslist = list(filter(None, sentenceslist))
        for sentence in sentenceslist:
            words = sentence.split(" ")
            for i in range(len(words) - 1):
                contents += ',' + words[i]
                if words[i] not in model:
                    model[words[i]] = {}
                if words[i + 1] not in model[words[i]]:
                    model[words[i]][words[i + 1]] = 0
                model[words[i]][words[i + 1]] += 0.000001
        save_model('model.json', model)
        print(sentenceslist)
        file2.write(contents)
    else:
        file2.close()
        break
print("Bye!")
