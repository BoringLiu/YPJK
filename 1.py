import requests
import time
import hashlib
import json

# === 参数配置 ===
item_id = "922038391070"  # 替换成你要查询的 itemId
m_h5_tk = "3885325d0d3dabbc97d857038d7ca260_1747910679105"
m_h5_tk_enc = "d581e0ac6227fc78796796c47fa2f7d0"
appKey = "12574478"
t = str(int(time.time() * 1000))

# === 构造 data 参数 ===
data_dict = {
    "itemId": item_id,
    "bizCode": "ali.china.damai",
    "scenario": "itemsku",
    "exParams": json.dumps({"dataType": 4, "dataId": ""}),
    "platform": "8",
    "comboChannel": "2",
    "dmChannel": "damai@damaih5_h5"
}
data_str = json.dumps(data_dict, separators=(',', ':'))
token = m_h5_tk.split('_')[0]
sign_str = f"{token}&{t}&{appKey}&{data_str}"
sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

# === 拼接 URL ===
url = f"https://mtop.damai.cn/h5/mtop.alibaba.detail.subpage.getdetail/2.0/?" \
      f"jsv=2.7.4&appKey={appKey}&t={t}&sign={sign}&api=mtop.alibaba.detail.subpage.getdetail&v=2.0" \
      f"&H5Request=true&type=originaljson&timeout=10000&dataType=json&valueType=original" \
      f"&forceAntiCreep=true&AntiCreep=true&useH5=true&data={requests.utils.quote(data_str)}"

# === 请求头 ===
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://m.damai.cn/",
    "Cookie": f"_m_h5_tk={m_h5_tk}; _m_h5_tk_enc={m_h5_tk_enc};"
}

# === 发起请求 ===
resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'
try:
    data = resp.json()
    sku_list = data['data']['itemSku']['calendar']['skuList']
    for sku in sku_list:
        name = sku.get("skuName", "未知")
        num = sku.get("salableQuantity", "未知")
        price = sku.get("priceText", "未知")
        print(f"{name} - 余票：{num} - 价格：{price}")
except Exception as e:
    print("解析失败，可能被封控：", e)
    print(resp.text)