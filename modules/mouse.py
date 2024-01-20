import pyautogui


def get_mouse_position():
    # 獲取當前鼠標位置
    x, y = pyautogui.position()
    return x, y


# 主程序
if __name__ == "__main__":
    print("請將鼠標移動到你想要獲取座標的位置...")

    try:
        while True:
            x, y = get_mouse_position()
            print(f"鼠標座標：({x}, {y})", end="\r")  # \r 用於覆蓋上一行的輸出
    except KeyboardInterrupt:
        print("\n程式結束。")
