# Cameo Eco Query

這是一個專門用於環保查詢的服務，從 `enviRobot` 服務中拆分出來。

## 安裝

使用 pip 安裝：

```
pip install cameo_eco_query
```

## 使用方法

首先，確保您已經安裝了此套件和所需的環境變數。

接下來，您可以這樣使用 `get_event_gmap_info` 函數：

```
from cameo_eco_query import get_event_gmap_info  # 請依您的模組結構調整這個 import 語句

# 範例輸入字串，包含時間、地點和事件
input_str = "下星期五晚上七點，在台北101舉行的環保會議"

# 使用預設的 'CH'（中文）語言參數
result = get_event_gmap_info(input_str)

# 或者，您也可以指定語言和提詞文檔的路徑
result_with_custom_prompt = get_event_gmap_info(input_str, lang='EN', prompt_path="your_prompt_path.txt")

print(result)
print(result_with_custom_prompt)
```

這會回傳一個包含狀態、提示訊息、時間、地點、事件以及 Google 地圖 URL 的字典。

例如：

```
{
    "status": "success", 
    "message": "", 
    "data": {
        "time": "2023-11-10 19:00:00", 
        "location": "台北101", 
        "event": "環保會議", 
        "gmap": "https://www.google.com/maps?q=25.0339639,121.5644722"
    }
}
```

若輸入字串中無法判讀時間資訊, 則會回傳如下：
```
{
    "status": "error", 
    "message": "你的事件缺少具體發生時間. 請在'在台北101舉行環保會議'中適當位置加入'{事件發生時間}'", 
    "data": {
        "time": "", 
        "location": "台北101", 
        "event": "環保會議", 
        "gmap": "https://www.google.com/maps?q=25.0339639,121.5644722"
    }
}
```

## 設定環境變數

本服務需要以下環境變數：

- `OPENAI_KEY`: OpenAI API 金鑰
- `GOOGLE_API_KEY`: Google MAP API 金鑰

您可以在 `.env` 檔案中設定這些變數。

## 問題與反饋

如有任何問題或反饋，請在 [GitHub Issues](https://github.com/bohachu/cameo-eco-query/issues) 中提出。

## 開發者

- JcXGTcW ([@jcxgtcw](https://github.com/jcxgtcw))

## 授權

本專案使用 MIT 授權。
