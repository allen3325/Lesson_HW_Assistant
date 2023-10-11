'''
curl "https://lms2020.nchu.edu.tw/course/homeworkList/24288" ^
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" ^
  -H "Accept-Language: zh-TW,zh;q=0.9,en;q=0.8" ^
  -H "Cache-Control: max-age=0" ^
  -H "Connection: keep-alive" ^
  -H "Cookie: PHPSESSID=lrimucrvkfmolaoep4mgnprbc4; locale=zh-tw; noteFontSize=100; noteExpand=0; citrix_ns_id=AAI7-MgKZTsklQAAAAAAADs1q9dOSa1g07j2O40F8FvPVG9hHneWxPw4yT22tvUeOw==DdAKZQ==drQ0q-QZT3SqrXcM4bLelIisIx4=; IPCZQX03846e843c=0100ca008c780df80728a508ed0771175aae222e;timezone=^%^2B0800" ^
  -H "Referer: https://lms2020.nchu.edu.tw/course/24288" ^
  -H "Sec-Fetch-Dest: document" ^
  -H "Sec-Fetch-Mode: navigate" ^
  -H "Sec-Fetch-Site: same-origin" ^
  -H "Sec-Fetch-User: ?1" ^
  -H "Upgrade-Insecure-Requests: 1" ^
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60" ^
  -H "sec-ch-ua: ^\^"Microsoft Edge^\^";v=^\^"117^\^", ^\^"Not;A=Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"117^\^"" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  --compressed
  '''
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json

load_dotenv()

lessons_id = json.loads(os.getenv('lessons_id'))
lessons_name = json.loads(os.getenv('lessons_name'))
PHPSESSID = os.getenv('PHPSESSID')
citrix_ns_id = os.getenv('citrix_ns_id')
IPCZQX03846e843c = os.getenv('IPCZQX03846e843c')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": f'PHPSESSID={PHPSESSID}; locale=zh-tw; noteFontSize=100; noteExpand=0; citrix_ns_id={citrix_ns_id}; IPCZQX03846e843c={IPCZQX03846e843c};timezone=^%^2B0800',
    "Referer": "https://lms2020.nchu.edu.tw/course/24288",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
    "sec-ch-ua": '^\^"Microsoft Edge^\^";v=^\^"117^\^", ^\^"Not;A=Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"117^\^""',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '^\^"Windows^\^""'
}


def fake_notify(hw_name,target_time):
   print(f"作業 {hw_name} 即將在 {target_time} 到期")

def parse_time(tag_text):
  date_string_with_year = "2023-" + tag_text
  date_format = "%Y-%m-%d %H:%M"
  try:
    target_time = datetime.strptime(date_string_with_year, date_format)
    return target_time
  except ValueError:
    print("無法解析日期時間")

def compare_time(hw_name, target_time):
  # 現在時間
  current_time = datetime.now()
  # current_time = parse_time("10-22 23:59")
  # 比較目標時間和現在時間的差異
  time_difference = target_time - current_time
  # 如果差異大於2天，調用自定義函數
  if time_difference <= timedelta(days=3):
      return True
  else:
      print(f"作業 {hw_name} 超過3天，應繳交時間為 {target_time}")
      return False

def check_lesson(lesson_id):
  res = requests.get(f"https://lms2020.nchu.edu.tw/course/homeworkList/{lesson_id}", headers = headers)
  html_code = BeautifulSoup(res.text, features="html.parser")
  count_element = 0
  should_draw = False
  for tag in html_code.find_all("div", class_='text-overflow'):
    if tag.text not in ['iLearning 3.0']:
      count_element += 1
      # HW Name
      if count_element % 7 == 2:
          hw_name = tag.text
          # print(hw_name)
      # HW Status Check Logo
      if count_element % 7 == 6:
          hw_status_tmp = tag.text
      # HW Score
      if count_element % 7 == 0:
          hw_status = tag.text
          if hw_status != '-':
            print(f"{hw_name} 已繳交")
            should_draw = False
          if should_draw:
            # Line
            fake_notify(hw_name, hw_target_time)
            print("通知Line")
      # HW Date
      if count_element % 7 == 5:
        # compare time
        hw_target_time = parse_time(tag.text)
        should_draw = compare_time(hw_name, hw_target_time)

# check a lesson
for idx, lesson_id in enumerate(lessons_id): 
  # print(lesson_id)
  print(f'{lessons_name[idx]}:')
  check_lesson(lesson_id)