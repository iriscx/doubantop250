import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

# 返回URL的HTML页面
def get_a_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#　解析页面，返回一个生成器
def parse_a_html(html):
    reg = '<li>.*?em.*?(\d+)</em>.*?href="(.*?)">.*?src="(.*?)"\s+class.*?title">' + \
            '(.*?)</span>.*?bd.*?class="">(.*?)<br>.*?star.*?average">(\d.\d)<.*?</li>'
    pattern = re.compile(reg, re.S)
    results = re.findall(pattern, html) # 返回一个元祖列表
    for item in results:
        yield {
            'rank': item[0],
            'name': item[3],
            'link': item[1],
            'img': item[2],
            'cast': item[4].strip().replace("&nbsp;",' '),
            'score': item[5]
        }


# 写入文件
def write_an_item(item):
    with open('doubantop250.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://movie.douban.com/top250?start=' + str(offset)
    html = get_a_page(url)
    for item in parse_a_html(html):
        write_an_item(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*25 for i in range(10)])
    pool.close()
    pool.join()
