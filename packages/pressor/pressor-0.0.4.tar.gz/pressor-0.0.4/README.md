# pressor

## 介绍
从各种不同格式文件来源里提取出文本数据。pressor有压缩机的意思，希望本项目能成为数据压缩机。
## 支持的格式
- html
- epub
- mobi
- azw
- azw3
- docx

## 快速使用

```python3
from pressor import pressor

file_path = 'your_html_path.epub'
result = pressor(file_path)
print(result)
```

## 关于从网站网页的html中提取正文
由于各个网站的网页结构不同，目前没有一个完美的提取正文的方案，本项目采用的方案也不适配所有网站，经过实测可以提取大多数网站。
### 解决方案
- 适配了一批热门网站，使用提前准备好的xpath进行解析，后续也会继续适配其他网站
- 其他网站使用通用算法解析提取正文

### 适配网站目录

| 网站                            |        别名         |              
|:------------------------------|:-----------------:| 
| https://www.ifeng.com/        |       ifeng       | 
| https://www.sohu.com/         |       sohu        | 
| https://www.163.com/          |        163        | 
| https://www.sina.com.cn/      |       sina        | 
| https://www.qq.com/           |      new_qq       | 
| https://www.huxiu.com/        |       huxiu       | 
| https://baijiahao.baidu.com/  |  baijiahao_baidu  | 
| https://baike.baidu.com/      |    baike_baidu    | 
| https://zhuanlan.zhihu.com/   |  zhuanlan_zhihu   |  

### 使用教程
- 对于html文件使用pressor提取
```python3

from pressor import pressor
file_path = 'your_html_path.html'
# 使用通用算法提取正文
result = pressor(file_path)
print(result)

# 使用白名单（已适配网站）提取正文
# url 也可使用白名单里网站的别名，例如：https://www.sina.com.cn/ 的别名是 sina, url="sina"
url = 'https://you_web.com'
result = pressor(file_path, url=url)
print(result)
```
- 对于已加载至内存的html数据使用pressor提取
```python3
from pressor import html_data_to_text
import requests

url = '' 
headers = {}
resp = requests.get(url, headers=headers)
html_text = resp.text
result = html_data_to_text(html_text, url=url)
print(result)
```
- 使用自定义xpath提取正文

```python3
from pressor import get_text_from_whitelist
html_text = open('xxx.html').read()
true_xpath = {'title': 'xxxxx ', 'main_body': 'yyyyy'}
result = get_text_from_whitelist(html_text, true_xpath=true_xpath)
print(result)
```

- 使用通用算法提取正文
```python3
from pressor import get_text_from_main_body
html_text = open('xxx.html').read()
result = get_text_from_main_body(html_text)
print(result)
```

