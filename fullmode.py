import torch
from transformers import BertTokenizer, BertForTokenClassification
from kss import split_sentences  # (선택적) 문장 분리를 위한 라이브러리


def extract_keywords(sentence):
    # (선택적) 문장 분리
    sentences = split_sentences(sentence)

    # KoBERT 모델 및 토크나이저 로딩
    model_name = "snunlp/kobert"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForTokenClassification.from_pretrained(model_name)

    keywords = []

    for sent in sentences:
        # 문장을 토큰화하고 BERT 입력 형식으로 변환
        tokens = tokenizer.encode(sent, return_tensors='pt')

        # 모델로부터 예측값 받아오기
        with torch.no_grad():
            outputs = model(tokens)

        # 토큰의 예측 클래스 중 중요한 토큰 선택
        predictions = torch.argmax(outputs.logits, dim=2)
        selected_tokens = [tokenizer.decode(token.item()) for token in tokens[0][predictions[0] == 1]]

        # 선택된 토큰을 키워드 리스트에 추가
        keywords.extend(selected_tokens)

    return keywords
