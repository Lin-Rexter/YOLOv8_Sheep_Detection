[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]()

<div align="center">

## Flask - YOLOv8 Sheep Detection
**使用Flask(async)製作的羊圈管理系統，可辨識羊隻身分ID、活動量(正常、躁動、睡覺)**

### ⚠️ | 功能尚未完善，持續開發中... 完成度(70%) |

</div>

---

<details>
  <summary>

## 運行 🚀

  </summary>

- ### [使用Poetry運行](https://python-poetry.org/docs/#installation)
	> **1. 編輯 [poetry 設定檔](https://python-poetry.org/docs/cli/#config)**
	>> 如果偏好將虛擬空間配置在專案目錄底下
	> ```bash
	> poetry config virtualenvs.in-project true
	> ```

	> **2. [安裝套件及依賴](https://python-poetry.org/docs/cli/#install)**
	> ```bash
	> poetry install
	> ```

	> **3. [啟用虛擬環境](https://python-poetry.org/docs/cli/#shell)**
	> * 使用 **預設** Python 版本
	>> ```bash
	>> poetry shell
	>> ```
	>
	> * 如果你想 **[指定 Python 版本](https://python-poetry.org/docs/managing-environments/#switching-between-environments)**
	>> ```bash
	>> poetry env use 3.9
	>> ```

	> **4. 修改所有yaml的path路徑(絕對路徑)**
	> * yaml位置
	>> ```bash
	>> .\yolo_v8 > yolo > yaml > *.yaml
	>> ```

	> **5. 運行Flask網頁**
	> * 如果上一個步驟有使用 `poetry shell`
	>> ```bash
	>> python ./app.py
	>> ```
	>
	> * 如果上一個步驟 **沒有使用** `poetry shell`
	>> ```bash
	>> poetry run python ./app.py
	>> ```

	> **6. 手動辨識(detection)**
	> * 前置作業
	>> + 已訓練好的結果資料(.\yolo_v8\yolo\runs\yolov8_ID_30)(非重要)
	>>> ```
	>>> 評估資料已壓縮，如要查看請先解壓縮，如不需要可刪除，再自行訓練，但權重檔(weights)未壓縮因此不影響辨識腳本運作。
	>>> ```	
	>> + 測試資料(羊隻身分辨識、羊隻活動量辨識)(重要)
	>>> ```
	>>> 位置: ".\yolo_v8\測試資料\羊隻身分辨識\" and ".\yolo_v8\羊隻活動量辨識\"
	>>>
	>>> 因檔案過大，已存放至雲端空間(有連結)，要使用時請再下載下來，也可存放自己的測試資料(mp4, jpg)。
	>>>
	>>> *影片檔(Video)請放至"羊隻活動量辨識"資料夾，目前只支援MP4，未來將改善。
	>>>
	>>> *圖片(Image)請放置"羊隻身分辨識"資料夾，目前只支援JPG，未來將改善。
	>>> ```
	>> + 權重檔(重要)
	>>> ```
	>>> 位置: ".\yolo_v8\yolo\runs\<訓練結果資料夾>\weights\\*.pt"
	>>> ```
	>
	> * 執行辨識羊隻身分ID腳本
	>>> 不需手動設置測試資料、權重檔路徑，會自動偵測並可在終端機選擇。
	>> ```bash
	>> Poetry run python .\modules\test_img.py
	>> ```
	>
	> * 執行辨識羊隻活動量腳本
	>>> 不需手動設置測試資料、權重檔路徑，會自動偵測並可在終端機選擇。
	>> ```bash
	>> Poetry run python .\modules\test_video.py
	>> ```

	> **7. 手動訓練(train)**
	> * 資料集datasets(.\yolo_v8\yolo\datasets)
	>> ```
	>> 因檔案過大，因此存放至雲端硬碟，要使用時請先下載下來，也可使用自己的資料集。
	>> ```
	>
	> * 資料集配置檔yaml(.\yolo_v8\yolo\yaml)
	>> ```
	>> 請記得修改path的路徑。
	>> ```
	>
	> * 預訓練YOLO模型(.\yolo_v8\yolo\pre_models)
	>> ```
	>> 只需放置pre_models資料夾即可。
	>> ```
	>
	> * 執行訓練腳本
	>>> 不需手動設置預訓練模型、資料集配置檔yaml路徑，會自動偵測並可在終端機選擇。
	>> ```bash
	>> Poetry run python .\modules\train.py
	>> ```

</details>

## License
**[MIT](https://github.com/Lin-Rexter/NPUST-RentRoom/blob/1b39ab0240b4e2440e34abccb242a9105669cf86/LICENSE)**


