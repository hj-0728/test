import base64
import random
from io import BytesIO
from typing import List, Optional, Tuple

from infra_basic.basic_model import BasePlusModel
from infra_utility.file_helper import build_abs_path_by_file
from PIL import Image, ImageDraw, ImageFilter, ImageFont


class CaptchaParams(BasePlusModel):
    length: int = 4
    char_list: List[str] = ["ABCDEFGHJKLMNPQRSTVWXYZ", "123456789"]
    img_size: Tuple[int, int] = (160, 40)
    img_mode: str = "RGB"
    font_size: int = 30
    draw_lines: bool = True
    draw_lines_number: Tuple[int, int] = (5, 9)
    draw_points: bool = False
    draw_points_percent: float = 0.05


class GraphicalCaptchaHelper:
    def __init__(self, params: Optional[CaptchaParams] = None):
        self._font_path = build_abs_path_by_file(__file__, "../docs/font/simhei.ttf")
        self._params = params if params else CaptchaParams()

    def captcha(self) -> Tuple[str, str]:
        """
        生成验证码
        :return:
        """
        # 创建图形
        img = Image.new(self._params.img_mode, self._params.img_size, (255, 255, 255))
        # 创建画笔
        draw = ImageDraw.Draw(img)
        if self._params.draw_lines:
            self.draw_line(draw=draw)
        if self._params.draw_points:
            self.draw_line(draw=draw)
        captcha_char = self.draw_char(draw=draw)
        self.distortion(img=img)
        return self.image_to_base64(image=img), captcha_char

    def draw_line(self, draw: ImageDraw):
        """
        绘制干扰线条
        :return:
        """
        # 干扰线条数
        line_num = random.randint(*self._params.draw_lines_number)
        width, height = self._params.img_size
        # pylint: disable= W0612
        for i in range(line_num):
            begin = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([begin, end], fill=self.random_color_rgb())

    @staticmethod
    def random_color_rgb(color_range=(0, 255)):
        """
        随机生成颜色
        """
        return (
            random.randint(*color_range),
            random.randint(*color_range),
            random.randint(*color_range),
        )

    def draw_points(self, draw: ImageDraw):
        """
        绘制干扰点
        :param draw:
        :return:
        """
        for width in range(self._params.img_size[0]):
            for height in range(self._params.img_size[1]):
                if random.random() < self._params.draw_points_percent:
                    draw.point((width, height), fill=(0, 0, 0))

    def draw_char(self, draw: ImageDraw):
        """
        绘制验证码字符
        :return:
        """
        char_str = "".join(self._params.char_list)
        c_chars = random.sample(char_str, self._params.length)
        # 每个字符前后以空格隔开
        strs = " ".join(c_chars)
        font = ImageFont.truetype(self._font_path, self._params.font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(
            (
                (self._params.img_size[0] - font_width) / 3,
                (self._params.img_size[1] - font_height) / 3,
            ),
            strs,
            font=font,
            fill=self.random_color_rgb((120, 255)),
        )
        return "".join(c_chars)

    @staticmethod
    def image_to_base64(image: Image, ext: str = "bmp") -> str:
        """
        将图片转为base64
        :return:
        """
        output_buffer = BytesIO()
        image.save(output_buffer, format=ext)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode()
        return f"data:image/{ext};base64,{base64_str}"

    def distortion(self, img: Image):
        """
        使得线条弯曲等
        :param img:
        :return:
        """
        params = [
            1 - float(random.randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500,
        ]
        # 创建扭曲
        img.transform(self._params.img_size, Image.PERSPECTIVE, params)
        # 滤镜，边界加强（阈值更大）
        img.filter(ImageFilter.EDGE_ENHANCE_MORE)
