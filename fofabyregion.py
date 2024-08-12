import re
import requests
import os
import time

# 定义要提取的网页列表和对应的保存文件名
urls = {
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiAgcmVnaW9uPSJIYWluYW4i": "Hainan-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkppbGluIg%3D%3D": "Jilin-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkNob25ncWluZyI%3D": "Chongqing-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlNoYW54aSI%3D": "Shanxi-store.txt",
    # 山西
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ikd1YW5neGkgWmh1YW5nenUi": "Guangxi Zhuangzu-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlNpY2h1YW4i": "Sichuan-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ikd1YW5nZG9uZyI%3D": "Guangdong-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlpoZWppYW5nIg%3D%3D": "Zhejiang-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkppYW5nc3Ui": "Jiangsu-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkJlaWppbmci": "Beijing-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkhlaWxvbmdqaWFuZyI%3D": "Heilongjiang-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkhlbmFuIg%3D%3D": "Henan-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ikh1YmVpIg%3D%3D": "Hubei-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ikh1bmFuIg%3D%3D": "Hunan-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlNoYW5kb25nIg%3D%3D": "Shandong-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkFuaHVpIg%3D%3D": "Anhui-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlNoYW5naGFpIg%3D%3D": "Shanghai-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkhlYmVpIg%3D%3D": "Hebei-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkxpYW9uaW5nIg%3D%3D": "Liaoning-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlNoYWFueGki": "Shaanxi-store.txt",
    # 陕西
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlRpYW5qaW4i": "Tianjin-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkZ1amlhbiI%3D": "Fujian-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkppYW5neGki": "Jiangxi-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlhpbmppYW5nIFV5Z3VyIg%3D%3D": "Xinjiang Uygur-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ik5laSBNb25nb2wi": "Nei Mongol-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ill1bm5hbiI%3D": "Yunnan-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ikd1aXpob3Ui": "Guizhou-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkdhbnN1Ig%3D%3D": "Gansu-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlFpbmdoYWki": "Qinghai-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249Ik5pbmd4aWEgSHVpenUi": "Ningxia Huizu-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IlRXIg%3D%3D": "TW-store.txt",
    "https://fofa.info/result?qbase64=dGl0bGU9ImlTdG9yZU9TIiAmJiBpY29uX2hhc2g9Ii0yMTMyODQxNDU1IiAmJiByZWdpb249IkhLIg%3D%3D": "HK-store.txt",
    # "https://fofa.info/result?qbase64=KCgiSFRUUCBjb3JlIHNlcnZlciBieSBSb3podWsgSXZhbi8xLjciIHx8ICJ1ZHB4eSIpICYmIGNvdW50cnk9IkNOIikgJiYgcmVnaW9uPSJYaXphbmci": "Xizang.txt",#Xizang
    # "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIg": "SXZ.txt",
    # "https://fofa.info/result?qbase64=L1pIR1hUVi9pbmRleC5waHA%3D": "ZHGX.txt",
    # "https://fofa.info/result?qbase64=c3RhdGljL3R2aC5qcy5neg%3D%3D": "TVH.txt",
    # "https://fofa.info/result?qbase64=Imh0dHA6Ly9tdW11ZHZiLm5ldC8i": "MUMU.txt",
    # "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04i": "udpandmsdcn.txt",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# 遍历网页列表

for url, filename in urls.items():
    try:
        print(f'正在爬取{filename}.....')
        # 发送GET请求获取源代码
        response = requests.get(url, headers=headers)
        page_content = response.text
        # 查找所有符合指定格式的网址
        pattern = r'<a href="http://(.*?)" target="_blank">'
        urls_all = re.findall(pattern, page_content)
        urls = set(urls_all)  # 去重得到唯一的URL列表
        existing_urls = []
        # 检查文件是否存在，如果不存在则创建文件
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8'):
                pass
        # 读取已存在的URL
        with open(filename, 'r', encoding='utf-8') as file:
            existing_urls = file.readlines()
        existing_urls = [url.strip() for url in existing_urls]  # 去除每行末尾的换行符
        with open(filename, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0, 0)  # 将文件指针移到文件开头
            for url in urls:
                if url not in existing_urls:
                    file.write(url + "\n")
                    print(url)
                    existing_urls.append(url)  # 将新写入的URL添加到已存在的URL列表中
            file.write(content)  # 将原有内容写回文件
    except Exception as e:
        print(f"爬取 {filename} URL {url} 失败：{str(e)}")
        continue
    # 暂停5秒
    time.sleep(5)
    print(f'{filename}爬取完毕,下一个')
