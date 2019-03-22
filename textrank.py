#rule-based로 문장을 구분 하는 방법
import re 
text = "이세돌은 알파고를 이겼다. 이세돌은 강하다. 알파고도 짱쎔."

def xplit(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiter) for delimiter in delimiters]), value)
# print(xplit('. ', '? ', '! ', '\n', '.\n')("This is a sentence. Here is another sentence.\nHello, world!"))
# ['This is a sentence', 'Here is another sentence', 'Hello, world!']
print(xplit('. ', '? ', '! ', '\n', '.\n')(text))
xplittext = xplit('. ', '? ', '! ', '\n', '.\n')(text)

#그냥 Mecab형태소 분석기
from konlpy.tag import Mecab
mecab = Mecab(dicpath="C:/mecab/mecab-ko-dic")
print(mecab.nouns(text))
print("\n")

#test xplit,Mecab동시 사용
from collections import Counter
bow1 = Counter(mecab.nouns(xplittext[0]))
bow1 += Counter(mecab.nouns(xplittext[1]))
bow2 = Counter(mecab.nouns(xplittext[1]))
print(bow1,",",bow2)
print("\n")
# Counter({'이세돌': 2, '파고': 1}) , Counter({'이세돌': 1})

#j_index: 문장간 영향력을 행사하는 정도
#이걸 word2vec로 바꾸면 잘되나?

print((bow1 & bow2).values())
j_index = sum((bow1 & bow2).values()) / sum((bow1 | bow2).values())
print(j_index)

#사실 이 말고도 여러가지 방법이 있다. 명사 말고 동사도 포함시켜도 되고, 
#레벤슈타인 거리를 사용해도 되고,
#TF-IDF를 계산해서 문장간의 각도를 사용해도 된다.
#이제 문장을 node로 뒀을때 edge에 부여할 값을 
#계산 할수 있게 되었으니 남은건 이걸로 그래프를 그리고 
#거기서 PageRank를 돌릴 것

class Sentence:

    @staticmethod
    def co_occurence(sentence1, sentence2):
        p = sum((sentence1.bow & sentence2.bow).values())
        q = sum((sentence1.bow | sentence2.bow).values())
        return p / q if q else 0

    def __init__(self, text, index=0):
        self.index = index
        self.text = text
        self.nouns = twitter.nouns(self.text)
        self.bow = Counter(self.nouns)

    def __eq__(self, another):
        return hasattr(another, 'index') and self.index == another.index

    def __hash__(self):
        return self.index


sentences = get_sentences(text)
graph = build_graph(sentences)
pagerank = networkx.pagerank(graph, weight='weight')
reordered = sorted(pagerank, key=pagerank.get, reverse=True)