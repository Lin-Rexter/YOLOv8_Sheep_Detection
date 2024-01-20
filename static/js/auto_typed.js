function auto_write(tag_name, messages, ...config) {
    args = config[0]
    // 設定自動打字
    var typed = new Typed(
        tag_name, // 寫入位置的標籤名稱
        {
            strings: [...messages], // 訊息
            typeSpeed: args['speed'] ?? 70, // 打字速度
            backSpeed: args['del_speed'] ?? 60, // 刪除速度
            startDelay: args['delay'] ?? 1000, // 延遲開始
            backDelay: args['del_delay'] ?? 6000, // 延遲刪除
            cursorChar: args['cursor_style'] ?? "<", // 游標樣式
            smartBackspace: args['smart_del'] ?? true, // 預設，智慧刪除功能，隨意
            loop: args['loop'] ?? true  // 不斷重複
        }
    );
}