import os, json, time
import random

from starlette.responses import RedirectResponse
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from requests_toolbelt import MultipartEncoder
import uvicorn

from CusImage import CusImage
from Translate import YouDao
from dotenv import load_dotenv
from requests import request


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
async def get_material(text: str):
    yd = YouDao(app_key=os.getenv("YOUDAO_APP_KEY"), app_secret=os.getenv("YOUDAO_APP_SECRET"))
    res = yd.connect(q=text)

    explains = "\n".join(res["basic"]["explains"])

    info_text = f"{text}\n中文翻译：{res['translation']}\n解释：{explains}\n发音：{res['basic']['phonetic']}\n美式发音：{res['basic']['us-phonetic']}\n"

    image_name = "static/english.png"
    image_client = CusImage()
    image_client.create(text=text, image_name=image_name)
    return { "info_text": info_text}


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


def get_feishu_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = {
        "app_id": os.getenv("FEISHU_APP_ID"),
        "app_secret": os.getenv("FEISHU_APP_SECRET")
    }
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        return {"error": False, "msg":"获取 tenant_access_token 失败", "data": response.text}
    res = response.json()
    return res.get("tenant_access_token", None)

def upload_img_to_feishu(tenant_access_token):
    print("tenant_access_token: ", tenant_access_token)
    if tenant_access_token == None:
        return {"error":True, "msg":"无法获取feishu的tenant_access_token"}
    
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (open('static/english.png', 'rb'))}  # 需要替换具体的path 
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': f"Bearer {tenant_access_token}",  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers['Content-Type'] = multi_form.content_type
    response = request("POST", url, headers=headers, data=multi_form)


    if response.status_code != 200:
        return {"error": True,"msg":"上传图片失败","data": response.text}
    res = response.json()

    img_key = res.get("data",{}).get("image_key",None)
    return img_key



def send_img_feishu(tenant_access_token):
    
    img_key = upload_img_to_feishu(tenant_access_token=tenant_access_token)
    if not img_key:
        return {"error": True, "msg":"无法获取上传图片的 key"}
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = {
        "receive_id": os.getenv("FEISHU_RECEIVE_ID"),
        "msg_type": "image",
        "content": json.dumps({
            "image_key":f"{img_key}"
        }),
        "uuid": str(int(time.time()))
    }
    payload = json.dumps(data)

    headers = {
        'Authorization': f"Bearer {tenant_access_token}",
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = request("POST", url, headers=headers, data=payload)

    return {"error": False, "data": response.json()}


def send_msg_feishu(tenant_access_token, text):
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = {
        "receive_id": os.getenv("FEISHU_RECEIVE_ID"),
        "msg_type": "text",
        "content": json.dumps({
            "text":f"{text}"
        }),
        "uuid": str(int(time.time()))
    }
    payload = json.dumps(data)

    headers = {
        'Authorization': f"Bearer {tenant_access_token}",
        'Content-Type': 'application/json; charset=utf-8'
    }

    response = request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception("发送消息失败.")

    return {"error": False, "data": response.json()}

@app.post("/workflow/everyday_word")
async def workflow_everyday_word():
    
    word = await random_word()
    
    print("word: ",word)
    res = await get_material(text=word["word"])
    tenant_access_token = get_feishu_tenant_access_token()
    try:
        send_msg_feishu(tenant_access_token, text=res["info_text"])
    except Exception as e:
        send_msg_feishu(tenant_access_token, text=res["info_text"])
    
    
    send_img_feishu(tenant_access_token)
    return {"material": res}
    
    

@app.get("/")
async def index():
    return {"status":"running..."}

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, host="0.0.0.0")