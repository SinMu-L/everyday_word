from PIL import Image, ImageDraw, ImageFont
import random


class CusImage:

    def create(self, text: str, image_name: str="artistic_text_image.png"):
        # 创建一个100x100像素的白色图片
        width = 270
        height = int(16 * width / 9)
        # width, height = 400, 200
        # 随机一个颜色
        color = (random.randint(200,255), random.randint(200,255), random.randint(200,255))  # 白色，RGB格式
        image = Image.new('RGB', (width, height), color)

        # 使用Windows系统下的宋体
        font = ImageFont.truetype("AlimamaDongFangDaKai-Regular.ttf", 50)

        # 创建一个可以在图片上绘图的对象
        draw = ImageDraw.Draw(image)

        # 设置文本的位置和颜色
        text_color = (0, 0, 0)  # 黑色文本

        # 计算自动水平居中，上下1/3的位置坐标
        x, y = self.get_coordinates(draw=draw,text=text,font=font, img_width=width,img_height=height)

        # 使用艺术字体写入文本
        # draw.text((text_x, text_y), text=text, align="center", font=font, fill=text_color)

        draw.text((x,y),text=text,align="center", font=font, fill=text_color)

        # 保存图片为PNG格式
        image.save(image_name)

    def get_coordinates(self, draw, text, font, img_width, img_height):
        # 左、上、右、下
        text_left, text_top, text_right, text_bottom = draw.textbbox((0, 0), text=text, font=font)
        textbox_width = (text_right - text_left)
        textbox_height = (text_bottom - text_top)
        x = (img_width - textbox_width) / 2
        y = (img_height - textbox_height) / 3
        return x,y
