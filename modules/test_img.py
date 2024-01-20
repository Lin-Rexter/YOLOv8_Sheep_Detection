# coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))) # 解決app.py導入問題
import traceback  # 輸出詳細錯誤訊息
import time
from pathlib import Path
import json
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import (
    Annotator,
)
from utils import (
    search_path,  # search_path: 搜尋檔案或資料夾
    choose_ask,  # choose_ask: 將路徑列表轉成選擇選項
)


# YOLO_V8專案目錄
project_folder_path = Path(__file__).parents[1]


# 辨識羊隻身分ID
def identify_id(pt_file, image, show_img=False):
    """
    ## 辨識羊隻身分ID
    ---
    Args:
        - pt_file: 訓練好的權重檔路徑
        - image: 要測試的圖像路徑
        - show_img: 是否顯示圖像

    Returns:
        辨識結果圖像
    """
    try:
        # 載入訓練的權重檔
        model = YOLO(model=pt_file)

        # 讀取圖片
        img = cv2.imread(filename=str(image))

        if show_img:
            # 設定視窗名稱
            cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

        # 使用 YOLO 模型進行物件偵測
        results = model.predict(img, verbose=False)  # verbose=False: 停用詳細預測訊息

        # 設定紅色、綠色、藍色的 BGR 值
        colors = {
            "red": (0, 0, 255),  # red
            "green": (0, 255, 0),  # green
            "blue": (255, 0, 0),  # blue
        }

        result_detection_list = []  # 儲存每個偵測的物件資訊
        pred_name = "無偵測"  # 預測結果標籤名稱
        conf_score = 0  # 準確度
        # 繪製偵測框
        for info in results:
            if show_img:
                annotator = Annotator(img)
            boxes = info.boxes
            for box in boxes:
                b = box.xyxy[0]
                conf_score = round(float(box.conf[0]), 3)  # 信賴分數
                class_id = int(box.cls)
                pred_name = model.names[class_id]  # 預測結果標籤名稱

                sheeps = {
                    "class 1": "羊隻1",
                    "class 2": "羊隻2",
                    "class 3": "羊隻3",
                    "class 4": "羊隻4",
                    "class 5": "羊隻5",
                    "class6": "羊隻6",
                    "class 7": "羊隻7",
                    "class 8": "羊隻8",
                    "class 9": "羊隻9",
                }
                pred_name = sheeps[pred_name]

                color = colors["red"]

                if show_img:
                    # 繪製框
                    annotator.box_label(
                        box=b, label=f"{pred_name} {conf_score}", color=color
                    )

            # 辨識結果資訊
            info = {
                "image_path": str(image),
                "pred_name": pred_name,
                "conf_score": conf_score,
            }
            result_detection_list.append(info)

        if show_img:
            # 顯示偵測結果圖像
            img = annotator.result()
            cv2.imshow("frame", img)

            print(f"\n辨識結果:\n")
            for result_detection in result_detection_list:
                print(json.dumps(result_detection, indent=4, ensure_ascii=False))

            key = cv2.waitKey(0)  # OpenCV3.2版本後，預設會清除高位元資料，不需要將傳回值與 0xFF 做 & 運算了。
            if key == 27:  # ESC鍵退出
                return [True, "\n\n結束辨識..."]

            # 釋放視窗
            cv2.destroyAllWindows()

        return [True, result_detection_list]
    except Exception as e:
        return [False, traceback.print_exc()]


if __name__ == "__main__":
    # 搜尋訓練好的權重檔
    all_pt_list = search_path(
        search_path=project_folder_path.joinpath("yolo", "runs"),
        search_name="best.pt",
        deep=True,
    )
    if len(all_pt_list) == 0:
        raise ValueError("\n\n'yolo_v8/yolo/runs/'資料夾底下尚未有任何訓練好的權重檔!!")

    # 搜尋要測試的圖像
    all_image_list = search_path(
        search_path=project_folder_path.joinpath("測試資料", "羊隻身分辨識"),
        search_name="*.jpg",
        deep=True,
    )
    if len(all_image_list) == 0:
        raise ValueError("\n\n'yolo_v8/測試資料/羊隻身分辨識/'資料夾底下尚未有任何可測試的圖像!!")

    # 選擇權重檔、圖像
    while True:
        os.system("cls")
        try:
            # 選擇權重檔
            chosen_pt = choose_ask(
                path_list=all_pt_list,
                title="\n= = = = = 請選擇權重檔 = = = = =",
                ask="\n請輸入權重檔編號(不可選擇全部): ",
                answer="選擇的權重檔:",
            )

            # 選擇圖像
            chosen_image = choose_ask(
                path_list=all_image_list,
                title="\n= = = = = 請選擇測試圖像 = = = = =",
                ask="\n請輸入圖像編號(可選擇全部): ",
                answer="選擇的圖像:",
            )

            break
        except Exception:
            print("\n\n[Error]: 請輸入正確資料!!\n")
            os.system("pause")

    # 檢查是否選擇多張圖像(不顯示圖像)
    if len(chosen_image) > 1:
        for img in all_image_list:
            result = identify_id(pt_file=chosen_pt[0], image=img)
            if result[0]:
                print(f"\n{all_image_list.index(img)+1}. ")
                print(img)
                print(result[1])
    else:
        # 選擇單張(顯示圖像)
        result = identify_id(pt_file=chosen_pt[0], image=chosen_image[0], show_img=True)
        if result[0]:
            print(result[1])
        else:
            print(result[1])

"""
第七隻\643657_0.jpg: 0.89
第六隻\643647_0.jpg: 0.683
第九隻\643673_0.jpg: 0.463
"""
