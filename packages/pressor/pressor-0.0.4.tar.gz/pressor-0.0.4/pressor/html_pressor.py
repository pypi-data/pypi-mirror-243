# -*- coding: UTF-8 -*-
# @Time : 2023/11/21 16:05 
# @Author : 刘洪波
"""
从网页中提取文章标题与正文
解决方案：当提取的网页所属网站在白名单内时，加载用于所属网站的xpath进行提取；否则就使用通用算法进行提取。
通用算法有一定的缺陷，有些网站不能正确识别到标题与正文部分。
"""

from bigtools import get_keywords_from_text
from lxml import etree
from pressor.units import html_to_markdown
from pressor.config import xpath_dict, alias_dict, opposite_alias_dict


def count_keywords_from_paragraph_text(title: str, paragraph_texts: list):
    keywords = get_keywords_from_text(title)
    keywords = list(set(keywords))
    max_num = 0
    max_text = None
    for p in paragraph_texts:
        count_num = 0
        for k in keywords:
            count_num += p.count(k)
        if count_num > max_num:
            max_text = p
            max_num = count_num
    return max_num, max_text


def get_text_from_p_tag(html_etree):
    text_from_p_tag = {}
    p_tag = html_etree.xpath('//body//p')
    for p in p_tag:
        p_html = etree.tostring(p, pretty_print=True, encoding='unicode')
        p_text = html_to_markdown(p_html)
        p_text = p_text.strip()
        if '。' in p_text and len(p_text) > 2:
            text_from_p_tag[p_text] = p
    return text_from_p_tag


def get_text_from_main_body(html_text: str):
    main_body = None
    html_etree = etree.HTML(html_text)
    article_tag = html_etree.xpath('//article')
    h1_all_attr = [f'contains("{i}", "title")' for i in html_etree.xpath('//h1/@*')]
    title = []
    if h1_all_attr:
        title = html_etree.xpath(f'//h1[{" or ".join(h1_all_attr)}]//text()')
        title = [i.strip() for i in title]
    if not title:
        title = html_etree.xpath('//title//text()')
        title_meta = html_etree.xpath('//meta[contains("property", "title")]/@content')
        title += title_meta
        title = [i.strip() for i in title]
    title = title[0]
    if article_tag:
        if len(article_tag) > 1:
            main_body = article_tag[0].xpath('./..')[0]
        else:
            main_body = article_tag[0]
    else:
        text_from_p_tag = get_text_from_p_tag(html_etree)
        if text_from_p_tag:
            if title in text_from_p_tag:
                del text_from_p_tag[title]
            # print(text_from_p_tag)
            max_num, max_text = count_keywords_from_paragraph_text(title, list(text_from_p_tag.keys()))
            if max_num and max_text:
                center_p = text_from_p_tag[max_text]
                # print(max_num, max_text, center_p)
                main_body = center_p.xpath('./..')[0]

    if main_body is not None:
        selected_html = etree.tostring(main_body, pretty_print=True, encoding='unicode')
        # print(selected_html)
        return {'title': title, 'text_data': html_to_markdown(selected_html)}
    return ''


def get_xapth_from_xpath_dict(url: str):
    """获取xpath"""
    _alias = alias_dict.get(url, '')
    key = url
    _xpath = {}
    if _alias:
        _xpath = xpath_dict[_alias]
    else:
        for k in xpath_dict.keys():
            if (url.startswith('http://') or url.startswith('https://')) and k in url:
                _xpath = xpath_dict[k]
                key = opposite_alias_dict.get(k)
                break
    return _xpath, key


def get_text_from_whitelist(html_text: str, true_xpath: dict):
    """
    当提取的网页所属网站在白名单内时，加载用于所属网站的xpath进行提取
    :param html_text:
    :param true_xpath: type is dict, example: {'title': '//h1', 'main_body': '//div'}
    :return:
    """
    html_etree = etree.HTML(html_text)
    title = html_etree.xpath(true_xpath['title'])
    if title:
        title = title[0]
        main_body = html_etree.xpath(true_xpath['main_body'])
        if main_body:
            selected_html = etree.tostring(main_body[0], pretty_print=True, encoding='unicode')
            return {'title': title, 'text_data': html_to_markdown(selected_html)}
        return {'title': title, 'text_data': ''}
    return {}


def html_data_to_text(html_text, url: str):
    """
    从网页数据中提取文章标题与正文
    :param html_text:
    :param url:
    :return:
    """
    data, mode = '', ''
    if url:
        true_xpath, xpath_key = get_xapth_from_xpath_dict(url)
        if true_xpath:
            data = get_text_from_whitelist(html_text, true_xpath)
            mode = f"whitelist: website is {xpath_key}"
    if not mode:
        data = get_text_from_main_body(html_text)
        mode = "common"
    return {'data': data, 'mode': mode}


def html_to_text(file_path: str, url: str):
    """从保存的网页中提取文章标题与正文"""
    html_text = open(file_path, 'r', errors='ignore').read()
    return html_data_to_text(html_text, url)
