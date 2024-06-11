import time


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from dotenv import load_dotenv
from feishu import FeiShu
from utools import random_word, get_material, get_word_info, get_img
from CusImage import random_picture, CusImage


load_dotenv()

app = FastAPI()
feishu_client = FeiShu()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # 暴露所有标头
)


@app.get("/trans_word")
def trans_word(text: str):
    if len(text) <= 0:
        return {"error": True, "msg": "请传递 text 查询参数"}
    info_text = get_word_info(word=text)
    return {"info_text": info_text}


@app.get("/generate_img")
def generate_img(request: Request, word: str):
    if len(word) <= 0:
        return {"error": True, "msg": "请传递 word 查询参数"}
    get_img(text=word, image_name="static/random_pic.png")
    return {"img_link": str(request.url_for("static", path="random_pic.png"))}


@app.post("/workflow/everyday_word")
@app.get("/workflow/everyday_word")
async def workflow_everyday_word():
    "生成CET4 随机单词和图片"
    cet4_img = "static/random_pic4.png"
    cet4_word = random_word()
    print("cet4_word: ", cet4_word)
    get_img(text=cet4_word, image_name=cet4_img)
    cet4_info_text = get_word_info(word=cet4_word)
    feishu_client.send_img_feishu(filepath=cet4_img)
    time.sleep(0.5)
    feishu_client.send_msg_feishu(text=cet4_info_text)

    " 生成CET6 随机单词和图片"
    cet6_img = "static/random_pic6.png"
    cet6_word = random_word(wordfile="CET6.txt")
    get_img(text=cet6_word, image_name=cet6_img)
    cet6_info_text = get_word_info(word=cet6_word)
    feishu_client.send_img_feishu(filepath=cet6_img)
    time.sleep(0.5)
    feishu_client.send_msg_feishu(text=cet6_info_text)

    return {
        "cet4_word": cet4_word,
        "cet4_info_text": cet4_info_text,
        "cet6_word": cet6_word,
        "cet6_info_text": cet6_info_text,
    }


@app.post("/feishu_callback")
async def feishu_callback(reqest: Request):
    data = await reqest.json()
    if data.get("type", None) == "url_verification":
        return {"challenge": data["challenge"]}


@app.get("/")
async def index():
    return {"status": "running..."}


@app.get("/random_pic")
async def random_pic():
    random_picture()
    cus_image = CusImage()
    cus_image.random_pic(text="hello")


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, host="0.0.0.0")
