import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
import time
import schedule

load_dotenv()

lessons_id = json.loads(os.getenv('lessons_id'))
lessons_name = json.loads(os.getenv('lessons_name'))
PHPSESSID = os.getenv('PHPSESSID')
line_token = os.getenv('line_token')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": f'PHPSESSID={PHPSESSID}; locale=zh-tw; noteFontSize=100; noteExpand=0; timezone=^%^2B0800',
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
  url = "https://notify-api.line.me/api/notify"

  payload = f'message={hw_name}在{target_time}到期'
  headers = {
    'Authorization': f'Bearer {line_token}',
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  time.sleep(1)

  if response.status_code == 200:
    print("發送成功")
  else:
     print(f"發送失敗，作業 {hw_name} 即將在 {target_time} 到期")

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
  # 如果差異大於3天，調用自定義函數
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

def check_task():
  for idx, lesson_id in enumerate(lessons_id): 
    print(f'{lessons_name[idx]}:')
    check_lesson(lesson_id)

# 定義一個函數來安排任務
def schedule_task():
    # 每天的00:00和12:00執行my_task函數
    schedule.every().day.at("00:01").do(check_task)
    schedule.every().day.at("12:01").do(check_task)

if __name__ == '__main__':
  # 開始排程
  schedule_task()

  # 保持腳本運行，以便任務可以被執行
  while True:
      schedule.run_pending()
      time.sleep(1)