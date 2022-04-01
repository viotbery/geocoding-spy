#-*-coding:utf-8-*-

__author__ = 'Viotbery'
import requests
from urllib.parse import urlencode
from pymongo import MongoClient
import coordtransf
import Geocoding

# 网站ajax请求url
base_url = 'https://www.ihchina.cn/Article/Index/getProject.html?province=&rx_time=&type=&cate=&keywords=&category_id=16&limit=10&'
client = MongoClient('mongodb://localhost:27017/')        # 连接本地MongoDB
db = client['cult']                 # 指定数据库
collection = db['cultcase3']        # 指定集合

def get_json(page):
    """
        获取相应页面(page)返回的json,每一条json包含十条非遗信息,传出json
    """
    # 设置参数，仅有'p'参数需要改变，代表page
    params = {
            'province': '',
            'rx_time': '',
            'type': '',
            'cate': '',
            'keywords': '',
            'category_id': '16',
            'limit': '10',
            'p': page
    }
    # 组合url与参数，模拟ajax请求
    url = base_url + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()      # 解析内容为json返回
    except requests.ConnectionError as e:
        print('Error',e.args)           #输出异常信息
 
 
def parsing_json(json):
    """
        创建迭代器,解析一条json中的十条信息,提取需要的信息
    """
    if json:
        items = json.get('list')
        for item in items:
            cultural = {}
            cultural['id'] = item.get('id')         # 项目id
            cultural['title'] = item.get('title')   # 非遗名称
            cultural['type'] = item.get('type')     # 类型
            cultural['province'] = item.get('province') # 申报省份/直辖市/城市/县级
            cultural['num'] = item.get('num')       # 项目代号
            yield cultural
 
def save(result):
    """
        将一条非遗信息数据插入Mongo数据库
    """
    if result:
        collection.insert_one(result)

if __name__ =='__main__':
    for page in range(1,3):
        try:
            json = get_json(page)
            results = parsing_json(json)
            for result in results:
                coord = Geocoding.getcoord(result.get('province'))     # 地理编码得到该地区的WGS84经纬度
                result['经度'] = coord[0]                               # 将获得的经纬度信息写入字典
                result['纬度'] = coord[1]
                print(result)
                save(result)
        except:
            print('ERROR! Stopped on page:', page)
            break
        else :
            print('page:', page, ' completed!')
