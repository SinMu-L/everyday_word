import os
import random

from starlette.responses import RedirectResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from CusImage import CusImage
from Translate import YouDao
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # 暴露所有标头
)
@app.get("/get_static_url", name="static_url")
async def get_static_url():
    # 这里返回的是完整的 URL
    return RedirectResponse(url="/static/test.png")


@app.get("/get_material")
async def get_material(request: Request, text: str):
    yd = YouDao(app_key=os.getenv("YOUDAO_APP_KEY"), app_secret=os.getenv("YOUDAO_APP_SECRET"))
    res = yd.connect(q=text)

    explains = "\n".join(res["basic"]["explains"])

    info_text = f"{text}\n中文翻译：{res['translation']}\n解释：{explains}\n发音：{res['basic']['phonetic']}\n美式发音：{res['basic']['us-phonetic']}\n"

    image_name = "static/english.png"
    image_client = CusImage()
    image_client.create(text=text, image_name=image_name)
    return {"image_link": str(request.url_for("static", path="english.png")), "info_text": info_text}


@app.get("/random_word")
async def random_word():
    with open("words.txt", "r", encoding="utf8") as fp:
        data = fp.read()
    all_line = data.split("\n")
    # 生成随机数
    index = random.randint(0, len(all_line) - 1)
    line_text = all_line[index]
    word = line_text.split("\t")[0]
    return {"word": word}


@app.get("/")
async def index():
    return {"status":"running..."}

if __name__ == '__main__':

    uvicorn.run("main:app", port=5000, host="0.0.0.0")