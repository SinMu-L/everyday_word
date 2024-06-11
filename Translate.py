# -*- coding: utf-8 -*-
import uuid
import requests
import hashlib
import time, os, json

import google.generativeai as genai

ai_trans_prompt = (
    lambda word: f"""
将 {word} 翻译为中文，并生成一句话解释和音标

---
【中文释义】：
【中文解释】：
【音标】
"""
)


class ChatGLMTrans:
    prompt_template = """
将 {word} 翻译为中文，并生成一句话解释和音标

---
按照如下格式返回
【中文释义】：
【中文解释】：
【音标】
"""

    def __init__(self) -> None:
        self._api_key = os.getenv("GEMINI_1.5_FLASH_API_KEY")

    def chat(self, word) -> None:
        genai.configure(api_key=self._api_key)

        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        prompt = self.prompt_template.replace("{word}", word)
        response = model.generate_content(prompt)
        return response.text


    def chat_bak(self, word) -> None:
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

