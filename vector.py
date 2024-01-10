import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA


def plot_word_distribution(model, num_points=100):
    # 모델의 단어 벡터들을 가져옵니다
    word_vectors = model.wv.vectors

    # Principal Component Analysis (PCA)를 사용하여 차원을 1로 축소합니다
    pca = PCA(n_components=1)
    word_vectors_1d = pca.fit_transform(word_vectors)

    # 1차원으로 축소된 벡터를 정렬합니다
    sorted_indices = np.argsort(word_vectors_1d[:, 0])
    sorted_word_vectors = word_vectors_1d[sorted_indices]

    # 수직선에 보여줄 포인트 수를 조정합니다
    step_size = len(sorted_word_vectors) // num_points
    selected_points = sorted_word_vectors[::step_size]

    # 원래의 단어 인덱스를 찾습니다
    original_indices = sorted_indices[::step_size]
    words = [model.wv.index_to_key[idx] for idx in original_indices]

    # 수직선 상에 단어 분포도를 플로팅합니다
    plt.figure(figsize=(10, 5))
    plt.plot(selected_points, np.zeros_like(selected_points), 'o')
    plt.yticks([])
    plt.title('Word Distribution on a 1D Space')
    plt.xlabel('1D Space')

    # 각 포인트에 단어를 주석으로 표시합니다
    for word, point in zip(words, selected_points):
        plt.annotate(word, (point, 0), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8,
                     color='blue')

    plt.show()
