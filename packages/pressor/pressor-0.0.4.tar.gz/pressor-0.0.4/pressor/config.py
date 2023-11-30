# -*- coding: UTF-8 -*-
# @Time : 2023/11/28 11:26 
# @Author : 刘洪波


alias_dict = {
    'ifeng': '.ifeng.com/c',
    'sohu': '.sohu.com/a',
    '163': '163.com',
    'sina': 'sina.com.cn',
    'new_qq': 'https://new.qq.com/',
    'huxiu': 'https://www.huxiu.com/article/',
    'baijiahao_baidu': 'https://baijiahao.baidu.com/',
    'baike_baidu': 'https://baike.baidu.com/item/',
    'zhuanlan_zhihu': 'https://zhuanlan.zhihu.com/p/',
}


opposite_alias_dict = {v: k for k, v in alias_dict.items()}


xpath_dict = {
    '.ifeng.com/c': {'title': '//body//h1/text()', 'main_body': '//div[@class="index_text_D0U1y"]'},
    '.sohu.com/a': {'title': '//div[@class="text-title"]/h1/text()', 'main_body': '//article[@class="article"]'},
    '163.com': {'title': '//h1[@class="post_title"]/text()', 'main_body': '//div[@class="post_body"]'},
    'sina.com.cn': {'title': '//h1[@class="main-title"]/text()', 'main_body': '//div[@class="article"]'},
    'https://new.qq.com/': {'title': '//div[@class="content-article"]/h1/text()',
                            'main_body': '//div[@id="ArticleContent"]'},
    'https://www.huxiu.com/article/': {'title': '//h1[@class="article__title"]/text()',
                                       'main_body': '//div[@id="article-content"]'},
    'https://baijiahao.baidu.com/': {'title': '//div[@id="header"]/div[1]/text()',
                                     'main_body': '//div[@data-testid="article"]'},
    'https://baike.baidu.com/item/': {'title': '//h1[@class="lemmaTitle_nn0pA J-lemma-title"]/text()',
                                      'main_body': '//div[@type="defaultTab"]'},
    'https://zhuanlan.zhihu.com/p/': {'title': '//h1[@class="Post-Title"]/text()',
                                      'main_body': '//div[@options="[object Object]"]'},
}



