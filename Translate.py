# -*- coding: utf-8 -*-

import requests
import os, json

import google.generativeai as genai


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
        self._api_key = os.getenv("GEMINI_FLASH_API_KEY")

    def chat(self, word) -> None:
        genai.configure(api_key=self._api_key)

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        prompt = self.prompt_template.replace("{word}", word)
        response = model.generate_content(prompt)
        return response.text
