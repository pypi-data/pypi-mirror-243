import geocoder

def get_gmap_url(location, google_key):
    location_data = geocoder.google(location, key=google_key)
    try:
        return location_data["lat"], location_data["lng"], f'https://www.google.com.tw/maps/search/{location_data["lat"]},{location_data["lng"]}'
    except TypeError:
        return None, None, f'抱歉, Google查詢經緯度的程式遇到了{location_data.status}問題, 但可以提供你如下參考網址: https://www.google.com/maps?q={location}'
