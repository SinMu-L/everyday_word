import os


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from dotenv import load_dotenv
from feishu import FeiShu
from utools import random_word, get_material


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


@app.post("/workflow/everyday_word")
async def workflow_everyday_word():
    " 生成CET4 随机单词和图片 "
    cet4_img = "static/cet4.png"
    cet4_word = random_word()
    cet4_info_text = get_material(text=cet4_word, image_name=cet4_img)
    feishu_client.send_img_feishu(filepath=cet4_img)
    feishu_client.send_msg_feishu(text=cet4_info_text)

    " 生成CET6 随机单词和图片"
    cet6_img = "static/cet6.png"
    cet6_word = random_word(wordfile="CET6.txt")
    cet6_info_text = get_material(text=cet6_word, image_name=cet6_img)

    return {"cet4_info_text": cet4_info_text, "cet6_info_text":cet6_info_text}
    
@app.post("/feishu_callback")
async def feishu_callback(reqest: Request):
    data = await reqest.json()
    return {"challenge": data["challenge"]}

@app.get("/")
async def index():
    return {"status":"running..."}

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, host="0.0.0.0")