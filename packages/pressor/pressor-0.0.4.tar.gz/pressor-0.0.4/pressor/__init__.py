# -*- coding: UTF-8 -*-
# @Time : 2023/11/21 16:04 
# @Author : 刘洪波
from pressor.html_pressor import html_to_text, html_data_to_text, get_text_from_whitelist, get_text_from_main_body
from pressor.more_pressor import epub_to_text, mobi_to_text, azw_to_text, word_to_text


func_dict = {
    'html': html_to_text,
    'epub': epub_to_text,
    'mobi': mobi_to_text,
    'azw': azw_to_text,
    'azw3': azw_to_text,
    'docx': word_to_text,
}


def pressor(file_path, file_type: str = None, url: str = None):
    """
    从 html epub mobi azw azw3 docx 中提取提取文本
    :param file_path: 文件路径
    :param file_type: 文件后缀名，可以不传入，会自动判断
    :param url:  当要提取的格式是html时，传入url可以自动选择相应网站的xpath进行解析，否则使用通用解析算法
    :return:
    """
    from bigtools import get_file_type
    if file_type is None:
        file_type = get_file_type(file_path)
    if file_type in func_dict:
        func = func_dict.get(file_type)
        if file_type == 'html':
            result = func(file_path, url)
        else:
            result = func(file_path)
        return result
    raise TypeError(f'{file_type} format is not supported')
