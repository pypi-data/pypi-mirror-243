import re

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def get_redirected_url(short_url):
    try:
        response = requests.get(short_url, headers=HEADERS, allow_redirects=True)
        final_url = response.url
        return final_url
    except requests.exceptions.RequestException as e:
        print(f"发生错误：{e}")
        return None


def get_video_id_by_short_url(short_url):
    """
    从抖音短连接获取视频id
    """
    # 使用正则表达式提取视频id
    pattern = r'/video/(\d+)[\/\?]'

    # 获取跳转后的地址
    redirected_url = get_redirected_url(short_url)
    print(redirected_url)

    if redirected_url:
        match = re.search(pattern, redirected_url)
        if match:
            video_id = match.group(1)
            return video_id


def get_iframe_data_by_video_id(video_id):
    """
    该接口用于通过视频 VideoID 获取 IFrame 代码。视频 VideoID 可以通过 PC 端视频播放地址中获取
    该接口无需申请权限。

    注意：
    该接口以 https://open.douyin.com/ 开头
    请求地址
    GET /api/douyin/v1/video/get_iframe_by_video

    docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/iframe-player/get-iframe-by-video
    """
    url = f"https://open.douyin.com/api/douyin/v1/video/get_iframe_by_video?video_id={video_id}"
    response = requests.get(url, )
    if response.status_code == 200:
        response_data = response.json()
        data = response_data["data"]
        # print(url, response_data)
        return data
    else:
        print("get_iframe_data_by_video_id Error:", response.status_code)
        return None
