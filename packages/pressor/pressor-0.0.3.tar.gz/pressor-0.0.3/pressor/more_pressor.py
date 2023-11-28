# -*- coding: UTF-8 -*-
# @Time : 2023/11/27 11:03 
# @Author : 刘洪波
import epubs
import ebooksp
import docx
from zipfile import ZipFile
from bs4 import BeautifulSoup
from pressor.units import parse_html_from_epub


def epub_to_text(file_path: str, func=parse_html_from_epub):
    """epub格式转 text"""
    data = []
    ep_text = epubs.to_text(file_path, func=func)
    for ep in ep_text:
        if ep:
            data += ep
    return data


def mobi_to_text(file_path: str):
    """mobi格式转 text"""
    data = []
    ep_text = ebooksp.to_text(file_path)
    for ep in ep_text:
        if ep:
            data += ep
    return data


def azw_to_text(file_path: str):
    """azw格式转 text"""
    return mobi_to_text(file_path)


def word_to_text(file_path: str):
    """word格式转 text"""
    data = []
    try:
        f = docx.Document(file_path)
        for para in f.paragraphs:
            data.append(para.text)
    except Exception as e:
        print('第一种方案解析docx失败', e)
        data = []
        document = ZipFile(file_path)
        xml = document.read("word/document.xml")
        word_obj = BeautifulSoup(xml.decode("utf-8"), features='lxml')
        texts = word_obj.findAll("w:t")
        for text in texts:
            if text.text is not None:
                data.append(text.text)
    return data
