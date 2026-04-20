import pandas as pd
import spacy

# 读取xlsx文件
df = pd.read_excel("D:/NJU文件/社会网络分析赛题/赛题1/output_with_language3.xlsx.xlsx")

# 加载 spaCy 模型
nlp_en = spacy.load("en_core_web_sm")  # 英语
nlp_ar = spacy.load("ar_core_news_sm")  # 阿拉伯语
nlp_ja = spacy.load("ja_core_news_sm")  # 日语
nlp_ko = spacy.load("ko_core_news_sm")  # 韩语

# 对description列进行POS分析，创建新的pos列
def pos_tagging(text):
    if isinstance(text, str):
        doc_en = nlp_en(text)
        doc_ar = nlp_ar(text)
        doc_ja = nlp_ja(text)
        doc_ko = nlp_ko(text)
        return (
            [(token.text, token.pos_) for token in doc_en],
            [(token.text, token.pos_) for token in doc_ar],
            [(token.text, token.pos_) for token in doc_ja],
            [(token.text, token.pos_) for token in doc_ko]
        )
    else:
        return []

df[['pos_en', 'pos_ar', 'pos_ja', 'pos_ko']] = df['user/description'].apply(pos_tagging).apply(pd.Series)

# 保存带有新pos列的DataFrame为新的xlsx文件
df.to_excel("output_with_pos.xlsx", index=False, engine='openpyxl')
