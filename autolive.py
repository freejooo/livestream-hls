import requests
import json

API_KEY = 'AIzaSyDdLOC2SJOfww1THNB0wEo7uHJjUhw2xVM'

def get_live_chat_id(live_stream_id):
    url = f'https://www.googleapis.com/youtube/v3/liveBroadcasts?part=snippet&id={live_stream_id}&key={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    if 'items' in data and len(data['items']) > 0:
        live_chat_id = data['items'][0]['snippet']['liveChatId']
        return live_chat_id
    else:
        return None

def get_likes_count(live_chat_id):
    url = f'https://www.googleapis.com/youtube/v3/liveChat/messages?part=snippet&liveChatId={live_chat_id}&key={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    likes_count = 0
    if 'items' in data:
        for item in data['items']:
            if 'like' in item['snippet']['displayMessage']:
                likes_count += 1
    return likes_count

def get_live_stream_id():
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&key={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.text)
    if 'items' in data and len(data['items']) > 0:
        live_stream_id = data['items'][0]['id']['videoId']
        return live_stream_id
    else:
        return None

def automate_live_stream():
    live_stream_id = get_live_stream_id()
    if live_stream_id is None:
        print("No live stream found.")
        return
    live_chat_id = get_live_chat_id(live_stream_id)
    if live_chat_id is None:
        print("No live chat ID found.")
        return
    likes_count = get_likes_count(live_chat_id)
    print(f"Live Stream ID: {live_stream_id}")
    print(f"Likes Count: {likes_count}")

automate_live_stream()
