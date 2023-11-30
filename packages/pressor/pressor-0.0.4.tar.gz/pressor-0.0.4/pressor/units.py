# -*- coding: UTF-8 -*-
# @Time : 2023/11/27 11:12 
# @Author : 刘洪波
from bs4 import BeautifulSoup
import re
import html2text


h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True


def parse_html_from_epub(html_file):
    md_data = []
    html_file = html_file.decode('utf-8')
    file = html_file.replace('&#13;', ' ')
    soup = BeautifulSoup(file, 'html.parser')
    body = soup.body.contents
    if isinstance(body, list) and len(body) == 2:
        body = body[0]
    for i in body:
        element_name = i.name
        if element_name:
            element_name = element_name.lower()
            content = i.get_text().strip()
            content = re.sub(r'\[\d+\]', '', content).strip()
            content = re.sub(r'〔\d+〕', '', content).strip()
            if 'h' in element_name and 'hr' not in element_name:
                num = re.findall(r'\d+', element_name)
                if num:
                    tag = '#' * int(num[0])
                    c = f'{tag} {content}'
                    c = c.replace('\t', ' ')
                    md_data.append(c)
            elif element_name in 'a'.split():
                content = content.replace('\t', ' ').strip()
                if content:
                    md_data.append(f'<{content}>')
            elif element_name in 'ul ol li'.split():
                content = content.replace('\t', ' ').strip()
                if content:
                    md_data.append(f'- {content}')
            elif element_name in 'p div b strong section aside blockquote span'.split():
                content = content.replace('\t', ' ')
                md_data.append(content)
    return md_data


def html_to_markdown(data):
    return h.handle(data)
