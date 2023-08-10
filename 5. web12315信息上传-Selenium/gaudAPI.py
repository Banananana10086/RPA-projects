import requests
import configparser

config = configparser.ConfigParser()
configPath = r"./config.ini"
config.read(configPath)
key = config['asd']['key']


class GaodeGeo:
    def __init__(self):
        self.key = key

    def requestApi(self, url):
        re = requests.get(url, timeout=5).json()
        return re

    # 地理编码
    def getGeoCode(self, address):
        url = f'https://restapi.amap.com/v3/geocode/geo?parameters&key={self.key}&address={address}'
        json_data = self.requestApi(url)
        return json_data
        # print(json_data["geocodes"])
        # if json_data['status'] == '1':
        #     location = json_data['geocodes'][0]['location']
        #     return location
        # else:
        #     return '获取失败'

    # 根据经纬坐标获取地址等信息
    def getInverseGeoCode(self, location):
        url = f'https://restapi.amap.com/v3/geocode/regeo?parameters&key={self.key}&location={location}'
        json_data = self.requestApi(url)
        if json_data['status'] == '1':
            area = json_data['regeocode']['addressComponent']['district']
            return area
        else:
            return '获取失败'


if __name__ == "__main__":
    gd = GaodeGeo()
    while True:
        address = input()
        geocoding = gd.getGeoCode(address)
        province = geocoding['geocodes'][0]['province']
        city = geocoding['geocodes'][0]['city']
        district = geocoding['geocodes'][0]['district']
        adcode = geocoding['geocodes'][0]['adcode']
        print("--", province, city, district, adcode)
