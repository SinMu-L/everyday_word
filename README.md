## 环境变量



|环境变量名 | 说明|
|---|---|
|`YOUDAO_APP_KEY` | 有道API的API KEY |
|`YOUDAO_APP_SECRET`| 有道API的API Secret |
|`FEISHU_APP_ID`| 飞书自建应用的 APP ID | 
|`FEISHU_APP_SECRET`| 飞书自建应用的 APP Secret |
|`FEISHU_RECEIVE_ID`| 飞书中接收消息的用户ID |



随机获取一张风景图片
```shell

curl --location 'https://api.unsplash.com/photos/random?client_id=uq6XvNZRi4bZuVODAhb0FOxcdY-irRS8OqBbr0HM2BU&query=%E9%A3%8E%E6%99%AF'
```