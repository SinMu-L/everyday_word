import random, os
from Translate import ChatGLMTrans
from CusImage import CusImage


def random_word(wordfile: str="CET4.txt"):
    with open(wordfile, "r", encoding="utf8") as fp:
        data = fp.read()
    all_line = data.split("\n")
    # 生成随机数
    index = random.randint(0, len(all_line) - 1)
    line_text = all_line[index]
    word = line_text.split("\t")[0]
    return word


def get_word_info(word: str):
    ai_trans = ChatGLMTrans()
    info_text = ai_trans.chat(word=word)
    return info_text

def get_img(text: str, image_name:str):
    image_client = CusImage()
    image_client.create(text=text, image_name=image_name)

def get_material(text: str, image_name="static/cet4.png"):
    "获取随机的单词和图片"
    info_text = get_word_info(text=text)
    if info_text == None:
        info_text = get_word_info(text=text)
    get_img(text=text, image_name=image_name)
    return info_text
