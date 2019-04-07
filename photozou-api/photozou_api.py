import sys
import os
import time
import json
import requests
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import quote

# 画像を保存するディレクトリを作成・取得する関数


def get_save_dir(save_name):
    # 画像を保存するディレクトリを指定
    save_dir = "./image/" + save_name
    # 画像を保存するディレクトリを作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir

# 画像を保存するパスを取得する関数


def get_save_path(save_dir, save_name, id):
    num = "{0:04d}".format(id)
    save_path = "{0}/{1}.jpg".format(save_dir, save_name+str(num))
    return save_path

# 画像のURLを取得する関数


def get_image_url_list(query, n):
    endpoint = 'https://api.photozou.jp/rest/search_public.json'
    # queryをutf-8にデコード
    request = "{0}?keyword={1}&limit={2}".format(
        endpoint, quote(query.encode("utf-8")), n)
    response = urlopen(request).read()
    resources = json.loads(response)
    # 画像のurlを入れるリストを準備
    url_list = []
    # 画像のURLを抜き取る
    for resource in resources['info']['photo']:
        url = resource['image_url']
        # オリジナル
        #url = resource['original_image_url']
        # サムネイル
        #url = resource['thumbnail_image_url']
        url_list.append(url)
    return url_list

# 画像をダウンロードする関数


def download_image(img_url_list, query, save_name, n):
    # 画像を保存するディレクトリを取得
    save_dir = get_save_dir(save_name)
    # デバック
    print("[Debug] Query = \"{0}\", n = {1}".format(query, n))
    # 初期化
    id = 1
    # ダウンロード成功した回数
    success_cnt = 0
    # ダウンロード失敗した回数
    error_cnt = 0
    # ダウンロード失敗した画像のURLを入れるリストを準備
    error_url_list = []
    for img_url in img_url_list:
        try:
            save_path = get_save_path(save_dir, save_name, id)
            # 写真をダウンロード
            urlretrieve(img_url, save_path)
            success_cnt += 1
            # 1秒スリープ
            time.sleep(1)
            # デバック
            print("[Download] {0} {1}/{2}".format(query, id, n))
        except Exception as e:
            error_url_list.append(img_url)
            error_cnt += 1
            # デバック
            print("[Error] {0} {1}/{2} {3}".format(query, id, n, img_url))
        id += 1
    # デバック
    print("[Result] {0} success:{1}/{2}".format(query,
                                                success_cnt-error_cnt, success_cnt+error_cnt))
    if n != success_cnt+error_cnt:
        print("[Warning] URL Is Insufficient.")
    # ダウンロード失敗した画像のURL
    for error_url in error_url_list:
        print("[Failed URL] {0}".format(error_url))
    # 改行
    print("")
