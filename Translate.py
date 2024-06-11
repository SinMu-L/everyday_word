# -*- coding: utf-8 -*-
import uuid
import requests
import hashlib
import time, os, json

from zhipuai import ZhipuAI

ai_trans_prompt = (
    lambda word: f"""
将 {word} 翻译为中文，并生成一句话解释和音标

---
【中文释义】：
【中文解释】：
【音标】
"""
)


class YouDao:
    def __init__(self, app_key, app_secret):
        self.YOUDAO_URL = "https://openapi.youdao.com/api"
        self.APP_KEY = app_key
        self.APP_SECRET = app_secret

    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode("utf-8"))
        return hash_algorithm.hexdigest()

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10 : size]

    def do_request(self, data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)

    def connect(self, q: str):

        data = {}
        data["from"] = "en"
        data["to"] = "zh"
        data["signType"] = "v3"
        curtime = str(int(time.time()))
        data["curtime"] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data["appKey"] = self.APP_KEY
        data["q"] = q
        data["salt"] = salt
        data["sign"] = sign
        # data['vocabId'] = "您的用户词表ID"

        response = self.do_request(data)
        if response.status_code == 200:
            return response.json()


class ChatGLMTrans:
    prompt_template = """
将 {word} 翻译为中文，并生成一句话解释和音标

---
【中文释义】：
【中文解释】：
【音标】
"""

    def __init__(self) -> None:
        self._api_key = os.getenv("ONE-API_API_KEY")

    def chat(self, word) -> None:
        url = "https://one-api-ew3c.onrender.com/v1/chat/completions"
        prompt = self.prompt_template.replace("{word}", word)
        payload = json.dumps(
            {
                "model": "gemini-1.5-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            }
        )
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]

