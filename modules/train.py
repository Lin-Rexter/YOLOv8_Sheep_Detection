# coding=utf-8
import os
import traceback  # 輸出詳細錯誤訊息
import shutil
import time
from pathlib import Path
import multiprocessing  # 多執行緒套件
import torch  # pytorch
from ultralytics import YOLO  # YOLOV8套件
from modules.utils import (
    search_path,  # search_path: 搜尋檔案或資料夾
    choose_ask,  # choose_ask: 將路徑列表轉成選擇選項
)


# 訓練專案目錄
yolo_path = Path(__file__).parents[1].joinpath("yolo")


# 訓練YOLO模型
def train(
    pre_model,
    yaml,
    name,
    imgsz=640,
    epochs=30,
    patience=10,
    batch=16,
    project="runs",
):
    """
    ## 訓練YOLO模型
    ---
    Args:
        - pre_model: 預訓練模型名稱。
            - 建議存放路徑: `.\yolo_v8\yolo\pre_models\...`
        - yaml: yaml資料集配置檔名稱。
            - 建議存放路徑: `.\yolo_v8\yolo\yaml\...`
        - name: 訓練項目名稱。
            - 建議存放路徑: `.\yolo_v8\yolo\{project}\...`
        - imgsz: 影像大小，預設為640。
        - epochs: 訓練回合數，預設為30。
        - patience: 等待回合數，無改善則停止訓練，預設為10。
        - batch: 批次大小，每次訓練的樣本資料數量，預設為16。
        - project: 專案名稱，預設為"runs"。
            - 存放路徑: `.\yolo_v8\yolo\...`

    Returns:
        - list[bool, result]: 返回訓練結果。
            - list[0]: 為bool，代表訓練成功與否。
            - list[1]: 訓練結果，訓練失敗時為錯誤訊息。
    """
    # 檢查CUDA
    device = "cuda" if torch.cuda.is_available() else "cpu"
    GPU_IDs = None
    if device == "cuda":
        GPU_IDs = [i for i in range(torch.cuda.device_count())]

    # 檢查預訓練模型是否存在
    if not Path(pre_model).exists():
        return [False, "pre_model預訓練模型不存在! 建議存放至 '.\yolo_v8\yolo\pre_models' 資料夾底下"]

    # 載入預訓練模型
    model = YOLO(pre_model).to(device=device)

    # 檢查資料集配置檔是否存在
    if not Path(yaml).exists():
        return [False, "yaml資料集配置檔不存在! 建議存放至 '.\yolo_v8\yolo\yaml' 資料夾底下"]

    # 專案名稱(.\yolo_v8\yolo\...)
    project_name = yolo_path.joinpath(project)

    # 專案訓練項目名稱(後面接訓練回合數)
    train_name = f"{name}_{epochs}"
    train_path = project_name.joinpath(train_name)

    # 檢查是否存在相同項目(.\yolo_v8\yolo\runs\...)
    if train_path.exists():
        try:
            print("\n存在相同項目，進行刪除...")
            shutil.rmtree(train_path)  # 當存在相同項目時刪除
            print("刪除成功!\n")
        except Exception as e:
            print(f"刪除失敗! 原因: {e}\n")
            pass

    results = None
    try:
        results = model.train(
            data=yaml,  # 資料集配置檔
            imgsz=imgsz,  # 影像大小
            epochs=epochs,  # 訓練回合數
            patience=patience,  # 等待回合數，無改善則停止訓練
            batch=batch,  # 批次大小
            project=project_name,  # 專案名稱
            name=train_name,  # 訓練項目名稱
            device=GPU_IDs or "cpu",  # 使用GPU訓練，否則用CPU
        )
    except Exception as e:
        [False, traceback.print_exc()]

    return [True, results]


if __name__ == "__main__":
    # 避免多執行緒造成主程式重複執行
    multiprocessing.freeze_support()

    # 搜尋預訓練權重檔
    all_pre_pt_list = search_path(
        search_path=yolo_path.joinpath("pre_models"), search_name="*.pt"
    )
    if len(all_pre_pt_list) == 0:
        raise ValueError("\n\n'yolo_v8/yolo/pre_models/'資料夾底下尚未有任何預訓練權重檔!!")

    # 搜尋yaml檔
    all_yaml_path = search_path(yolo_path.joinpath("yaml"), search_name="*.yaml")
    if len(all_yaml_path) == 0:
        raise ValueError("\n\n'yolo_v8/yolo/yaml/'資料夾底下尚未有任何yaml資料集配置檔!!")

    epochs_ask = None
    while True:
        os.system("cls")
        try:
            # 設置訓練回合數
            epochs_ask = int(input("請輸入訓練回合數(按0預設30): "))
            if epochs_ask == 0:
                epochs_ask = 30

            # 選擇預訓練權重檔
            chosen_pre_model = choose_ask(
                path_list=all_pre_pt_list,
                title="\n= = = = = 請選擇預訓練權重檔 = = = = =",
                ask="\n請輸入預訓練權重檔編號(不可選擇全部): ",
                answer="選擇的預訓練權重檔:",
            )

            # 選擇yaml檔
            chosen_yaml = choose_ask(
                path_list=all_yaml_path,
                title="\n= = = = = 請選擇yaml檔 = = = = =",
                ask="\n請輸入yaml檔編號(不可選擇全部): ",
                answer="選擇的yaml檔:",
            )

            break
        except Exception:
            print("\n\n[Error]: 請輸入正確資料!!\n")
            os.system("pause")

    # 倒數
    print("\n即將開始訓練...\n")
    print("Ctrl+C結束訓練")
    for i in range(6, 0, -1):
        time.sleep(1)
        print(f"開始訓練將在{i}秒後開始...", end="\r")

    # 訓練Yolo模型
    result = train(
        pre_model=chosen_pre_model[0],
        yaml=chosen_yaml[0],
        epochs=epochs_ask,
        name=chosen_yaml[0].stem,  # stem: 移除副檔名的檔案名稱
        batch=16,
    )
    if result[0]:
        print("\n\n訓練成功!!")
    else:
        print(f"\n\n訓練失敗! 原因: {result[1]}")
