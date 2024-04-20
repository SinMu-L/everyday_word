import random, os
from Translate import YouDao
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


def get_word_info(text: str):
    yd = YouDao(app_key=os.getenv("YOUDAO_APP_KEY"), app_secret=os.getenv("YOUDAO_APP_SECRET"))
    res = yd.connect(q=text)

    explains = "\n".join(res["basic"]["explains"])

    info_text = f"{text}\n中文翻译：{res['translation']}\n解释：{explains}\n发音：{res['basic']['phonetic']}\n美式发音：{res['basic']['us-phonetic']}\n"
    return info_text


def get_material(text: str, image_name="static/cet4.png"):
    info_text = get_word_info()
    image_client = CusImage()
    image_client.create(text=text, image_name=image_name)
    return info_text
