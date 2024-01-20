# coding=utf-8
import os
from pathlib import Path


# 搜尋檔案或資料夾
def search_path(search_path, search_name, is_file=True, deep=False):
    """
    ## 搜尋檔案或資料夾
    ---
    Args:
        search_path: 搜尋的起始路徑
        search_name: 要搜尋的檔案或資料夾名稱
        is_file: 是否搜尋檔案，預設為True
        deep: 是否遞迴搜尋子資料夾，預設為False

    Returns:
        list: 返回搜尋到的所有路徑列表
    """
    path_list = []
    if deep:
        search_path = Path(search_path).rglob(search_name)
    else:
        search_path = Path(search_path).glob(search_name)
    for path in search_path:
        if is_file:
            if path.is_file():
                path_list.append(path)
        else:
            if path.is_dir():
                path_list.append(path)
    return path_list


# 將路徑列表轉成選擇選項方式
def choose_ask(path_list, title, ask, answer):
    """
    ## 將路徑列表轉成選項選擇方式
    ---
    Args:
        - data (list): 路徑列表
        - title (str): 標題
        - ask (str): 詢問標題
        - answer (str): 結果文字

    Returns:
        返回選擇的路徑
    """
    enc_path_list = [Path(path) for path in path_list if isinstance(path, Path)]  # 以防萬一先轉成pathlib的Path物件
    print(title)
    for i in range(len(enc_path_list)):
        print(f"{i+1}. {enc_path_list[i]}")
    data_ask = int(input(f"{ask}[輸入0選擇全部]: "))
    if data_ask == 0:
        return enc_path_list
    chosen_data = enc_path_list[data_ask - 1] if data_ask > 0 else enc_path_list[0]
    print(f"\n{answer}: \n\t名稱: {chosen_data.name}\n\t路徑: {chosen_data}")
    return [chosen_data]
