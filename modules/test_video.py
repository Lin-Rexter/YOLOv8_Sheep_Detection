# coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))) # 解決app.py導入問題
import traceback  # 輸出詳細錯誤訊息
import time
from pathlib import Path
import cv2
from ultralytics import YOLO, NAS
from ultralytics.utils.plotting import (
    Annotator,
)
from utils import (
    search_path,  # search_path: 搜尋檔案或資料夾
    choose_ask,  # choose_ask: 將路徑列表轉成選擇選項
)


# YOLO_V8專案目錄
project_folder_path = Path(__file__).parents[1]


# 辨識活動量
def identify_activity(pt_file, video, show_video=False):
    """
    ## 辨識活動量
    ---
    Args:
        - pt_file: 訓練好的權重檔路徑
        - video: 要測試的影片路徑

    Returns:
        辨識結果影像
    """
    try:
        # 載入訓練的權重檔(使用NAS模型請將YOLO改成NAS)
        model = YOLO(model=pt_file)
        classnames = ["sheep"]  # 辨識物件名稱

        # 測試影片檔
        cap = cv2.VideoCapture(filename=str(video))

        if show_video:
            # 設定視窗名稱
            cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

        # 設定紅色、綠色、藍色的 BGR 值
        colors = {
            "red": (0, 0, 255),  # red
            "green": (0, 255, 0),  # green
            "blue": (255, 0, 0),  # blue
        }

        # 設定偵測範圍
        area = [(600, 150), (600, 650), (1200, 150), (1200, 650)]

        while True:
            ret, frame = cap.read()
            time.sleep(0.01)  # 延遲0.01秒

            # 檢查frame是否正常
            if not ret:
                break

            # 在這裡加入檢查，確保 frame 不為空
            if not frame.size:  # 或者使用 if frame.size == 0:
                continue

            # 使用 YOLO 模型進行物件偵測
            results = model.predict(frame, verbose=False)  # verbose=False: 停用詳細預測訊息

            # 繪製偵測框
            for info in results:
                annotator = Annotator(frame)  # 使用內建的自動註解
                boxes = info.boxes  # 每個幀的所有偵測框
                # 繪製每個偵測框
                for box in boxes:
                    b = box.xyxy[0]
                    conf_score = round(float(box.conf[0]), 3)  # 信賴分數
                    class_id = int(box.cls)
                    pred_name = model.names[class_id]  # 預測結果標籤名稱

                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # 框座標

                    # 根據偵測框的位置決定顏色
                    if (
                        area[0][0] < (x1 + x2) // 2 < area[3][0]
                        and area[0][1] < (y1 + y2) // 2 < area[3][1]
                    ):
                        color = colors["red"]  # 在紅色範圍內
                    else:
                        color = colors["green"]  # 不在紅色範圍內

                    # 當信賴分數小於0.4則跳過，不繪製框
                    if conf_score < 0.4:
                        continue

                    # 繪製框
                    annotator.box_label(
                        box=b,
                        label=f"{pred_name} {conf_score}",
                        color=color,
                    )

            # = = = = = = = = 繪製偵測範圍 = = = = = = = =
            # 左半邊(綠色)
            cv2.line(frame, (385, 246), (600, 246), (0, 255, 0), 5)  # 上
            cv2.line(frame, (248, 660), (600, 650), (0, 255, 0), 5)  # 下
            cv2.line(frame, (385, 237), (248, 666), (0, 255, 0), 5)  # 左
            cv2.line(frame, (595, 244), (595, 650), (0, 255, 0), 5)  # 右

            # 右半邊(紅色)
            cv2.line(frame, (600, 246), (889, 244), (0, 0, 255), 5)  # 上
            cv2.line(frame, (600, 650), (1097, 627), (0, 0, 255), 5)  # 下
            cv2.line(frame, (600, 244), (600, 650), (0, 0, 255), 5)  # 左
            cv2.line(frame, (889, 244), (1097, 627), (0, 0, 255), 5)  # 右

            # 顯示偵測結果影像
            img = annotator.result()
            if show_video:
                cv2.imshow("frame", img)

                key = cv2.waitKey(1)  # OpenCV3.2版本後，預設會清除高位元資料，不需要將傳回值與 0xFF 做 & 運算了。
                if key == 27:  # ESC鍵退出
                    return [True, "\n結束辨識..."]

            #return [True, img]

        # 釋放影片檔和視窗
        cap.release()
        if show_video:
            cv2.destroyAllWindows()
    except Exception as e:
        return [False, traceback.format_exc()]


if __name__ == "__main__":
    # 搜尋訓練好的權重檔
    all_pt_list = search_path(
        search_path=project_folder_path.joinpath("yolo", "runs"),
        search_name="*.pt",
        deep=True,
    )
    if len(all_pt_list) == 0:
        raise ValueError("\n\n'yolo_v8/yolo/runs/'資料夾底下尚未有任何訓練好的權重檔!!")

    # 搜尋要測試的影片檔
    all_video_list = search_path(
        search_path=project_folder_path.joinpath("測試資料", "羊隻活動量辨識"),
        search_name="*.mp4",
        deep=True,
    )
    if len(all_video_list) == 0:
        raise ValueError("\n\n'yolo_v8/測試資料/羊隻活動量辨識/'資料夾底下尚未有任何可測試的影片檔!!")

    # 選擇權重檔、影片
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

            # 選擇影片
            chosen_video = choose_ask(
                path_list=all_video_list,
                title="\n= = = = = 請選擇測試影片檔 = = = = =",
                ask="\n請輸入影片檔編號: ",
                answer="選擇的影片檔:",
            )

            break
        except Exception:
            print("\n\n[Error]: 請輸入正確資料!!\n")
            os.system("pause")

    # 檢查是否選擇多張圖像(不顯示圖像)
    if len(chosen_video) > 1:
        for video in chosen_video:
            result = identify_activity(
                pt_file=chosen_pt[0], video=video, show_video=True
            )
            if result[0]:
                index = chosen_video.index(video) + 1
                print(f"\n{index}. 辨識影片{index}...")
                print(result[1])
    else:
        # 選擇單張(顯示圖像)
        result = identify_activity(
            pt_file=chosen_pt[0], video=chosen_video[0], show_video=True
        )
        if result[0]:
            print(result[1])
        else:
            print(result[1])
