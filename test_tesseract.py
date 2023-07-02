# -*- coding: utf-8 -*-
import subprocess
import pytesseract
from PIL import Image

# 指定 tesseract 命令路径和语言模型
tesseract_cmd = '/usr/bin/tesseract'
lang = 'chi_sim'

# 读取图片
img = Image.open('/home/robuster/RoboCom/oi.jpg')

# 将图像数据通过标准输入传递给 tesseract
# 将图片转换为字符串及边界框信息
p = subprocess.Popen([tesseract_cmd, 'stdin', 'stdout', '-psm', '6', lang, 'box'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate(img.tobytes())

# 将字节串列表转换为字符串列表
boxes = [box.decode('utf-8') for box in out.strip().split('\n')]

# 设置输出编码格式为 UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 打印识别结果
text = pytesseract.image_to_string(img, lang=lang)
print(text)