
# @Date 2022/05/16
# @Author special 15

import pytesseract
from PIL import Image


filename = '2222.png'
img = Image.open(filename)
print(img)
result = pytesseract.image_to_string(img, lang='chi_sim')
# result = result.replace('\n','').replace(' ','')
print(f'中文识别结果：\n {result}')