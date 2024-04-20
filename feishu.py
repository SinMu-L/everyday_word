import os, json, time
from requests import request
from requests_toolbelt import MultipartEncoder

class FeiShu:
    def __init__(self) -> None:
        self.APP_ID = os.getenv("FEISHU_APP_ID")
        self.FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
        self.FEISHU_RECEIVE_ID = os.getenv("FEISHU_RECEIVE_ID")
        self.url = "https://open.feishu.cn/open-apis"
        
        self.tenant_access_token = self.get_tenant_access_token()
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f"Bearer {self.tenant_access_token}",
        }


        pass
    def get_tenant_access_token(self):
        endpoint = "/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.APP_ID,
            "app_secret": self.FEISHU_APP_SECRET
        }
        payload = json.dumps(data)

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        response = request("POST", self.url+endpoint, headers=headers, data=payload)
        if response.status_code != 200:
            return {"error": False, "msg":"获取 tenant_access_token 失败", "data": response.text}
        res = response.json()
        return res.get("tenant_access_token", None)
        
    def upload_img_to_feishu(self,  filepath:str="static/cet4.png"):

        if self.tenant_access_token == None:
            return {"error":True, "msg":"无法获取feishu的tenant_access_token"}
        
        url = f"{self.url}/im/v1/images"
        form = {'image_type': 'message',
                'image': (open(filepath, 'rb'))}  # 需要替换具体的path 
        multi_form = MultipartEncoder(form)
        headers = {
            'Authorization': f"Bearer {self.tenant_access_token}",  ## 获取tenant_access_token, 需要替换为实际的token
        }
        headers['Content-Type'] = multi_form.content_type
        response = request("POST", url, headers=headers, data=multi_form)

        if response.status_code != 200:
            return {"error": True,"msg":"上传图片失败","data": response.text}
        res = response.json()

        img_key = res.get("data",{}).get("image_key",None)
        return img_key


    def send_img_feishu(self, filepath):
        """ 发生图片到飞书 """
        img_key = self.upload_img_to_feishu( filepath=filepath)
        if not img_key:
            return {"error": True, "msg":"无法获取上传图片的 key"}
        url = f"{self.url}/im/v1/messages?receive_id_type=open_id"
        data = {
            "receive_id": self.FEISHU_RECEIVE_ID,
            "msg_type": "image",
            "content": json.dumps({
                "image_key":f"{img_key}"
            }),
            "uuid": str(int(time.time()))
        }
        payload = json.dumps(data)

        response = request("POST", url, headers=self.headers, data=payload)

        return {"error": False, "data": response.json()}


    def send_msg_feishu(self, text):
        """ 发送文字消息到飞书 """
        url = f"{self.url}/im/v1/messages?receive_id_type=open_id"
        data = {
            "receive_id": self.FEISHU_RECEIVE_ID,
            "msg_type": "text",
            "content": json.dumps({
                "text":f"{text}"
            }),
            "uuid": str(int(time.time()))
        }
        payload = json.dumps(data)

        response = request("POST", url, headers=self.headers, data=payload)
        if response.status_code != 200:
            raise Exception("发送消息失败.")

        return {"error": False, "data": response.json()}


