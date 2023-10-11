# 使用方法
請先登入 iLearning3.0，取得以下資訊：

- lessons_id: ["lesson_id_1", "lesson_id_2", ...]
    
    登陸 iLearning 查看 lesson_id，如圖 22214 為電腦視覺的 id
    
    ![alt](https://i.imgur.com/N351HyV.png)

- lessons_name: ["lesson_name_1", "lesson_name_2", ...] 
    
    填入對應的 lesson_name，例如 lesson_id 為 ["22214", "lesson_id_2", ...] 則 lessons_name 為 ["電腦視覺", "lesson_name_2", ...]

- PHPSESSID: Yours

    cookie 取得方法:

    F12 -> Tab 選擇 Application -> Storage -> Cookies

    如圖：

    ![alt](https://i.imgur.com/u2e35AO.png)

- line_token: [申請教學](https://tools.wingzero.tw/article/sn/1224)

複製 .env.example，並重新命名為 .env ，將以上資訊填入

# 執行
```bash
pip install -r requirements.txt 
python craw_lesson.py
# 可以考慮使用 nohup & 使其背景執行 -> nohup python craw_lesson.py > output.log &
```

# TODO
Docker Container 形式執行
