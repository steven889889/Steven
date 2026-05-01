import tkinter as tk
import tkinter.font as tkfont
from functions import load_apis
from gui_functions import (
    create_input,
    refresh_api_list,
    add_api_from_entries,
    show_selected_api,
    delete_selected_api,
    load_selected_api_to_entries,
    save_edited_api
)


# 读取已有接口数据
apis = load_apis()


# 创建主窗口
window = tk.Tk()
window.title("API 接口管理器")
window.geometry("630x480")

# 设置全局字体
default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(family="Microsoft YaHei UI", size=10)

# 设置主窗口背景色
window.configure(bg="#f3f4f6")

editing_index = tk.IntVar(value=-1)  # 记录当前正在修改哪一条接口，-1 表示未进入修改状态

# 按钮样式
BUTTON_FONT = ("Microsoft YaHei UI", 10)
NORMAL_BUTTON = {
    "width": 12,
    "font": BUTTON_FONT,
    "bg": "#2563eb",
    "fg": "white",
    "activebackground": "#1d4ed8",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0
}

SAVE_BUTTON = {
    "width": 12,
    "font": BUTTON_FONT,
    "bg": "#16a34a",
    "fg": "white",
    "activebackground": "#15803d",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0
}

DANGER_BUTTON = {
    "width": 26,
    "font": BUTTON_FONT,
    "bg": "#dc2626",
    "fg": "white",
    "activebackground": "#b91c1c",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0
}


# 创建主布局区域
main_frame = tk.Frame(window, bg="#f3f4f6")
main_frame.pack(padx=6, pady=6)


left_frame = tk.LabelFrame(
    main_frame,
    text="接口目录",
    bg="#f3f4f6",
    padx=8,
    pady=8
)
left_frame.grid(row=0, column=0, padx=6, pady=2)

right_frame = tk.LabelFrame(
    main_frame,
    text="接口信息",
    bg="#f3f4f6",
    padx=8,
    pady=4
)
right_frame.grid(row=0, column=1, padx=6, pady=2)

detail_frame = tk.LabelFrame(
    window,
    text="接口详情",
    bg="#f3f4f6",
    padx=8,
    pady=1
)
detail_frame.pack(padx=6, pady=1)


# 最下方区域：操作状态
status_frame = tk.Frame(window, bg="#f3f4f6")
status_frame.pack(padx=6, pady=2)


# 左侧：接口目录
api_listbox = tk.Listbox(left_frame, width=32, height=12)
api_listbox.pack()



# 右侧：输入区域
name_entry = create_input(right_frame, "厂商名：")
url_entry = create_input(right_frame, "Base URL：")
key_entry = create_input(right_frame, "API Key：")
note_entry = create_input(right_frame, "备注：")


# 右侧：按钮区域
button_frame = tk.Frame(right_frame)
button_frame.pack(pady=6)


# 添加按钮
add_button = tk.Button(
    button_frame,
    text="添加接口",
    command=lambda: add_api_from_entries(
        apis,
        name_entry,
        url_entry,
        key_entry,
        note_entry,
        api_listbox,
        result_label,
        editing_index
    ),
    **NORMAL_BUTTON
)
add_button.grid(row=0, column=0, padx=3, pady=3)


# 保存修改按钮
save_edit_button = tk.Button(
    button_frame,
    text="保存修改",
    command=lambda: save_edited_api(
        apis,
        name_entry,
        url_entry,
        key_entry,
        note_entry,
        api_listbox,
        result_label,
        editing_index
    ),
    **NORMAL_BUTTON
)
save_edit_button.grid(row=0, column=1, padx=3, pady=3)


# 删除按钮
remove_button = tk.Button(
    button_frame,
    text="删除接口",
    command=lambda: delete_selected_api(api_listbox, apis, result_label, detail_text),
    **DANGER_BUTTON
)
remove_button.grid(row=1, column=0, columnspan=2, padx=3, pady=3)


# 下方：接口详情文本框，可以选中复制

detail_text = tk.Text(
    detail_frame,
    height=5,
    width=68,
    bg="#f9fafb",          # 浅灰白背景
    fg="#111827",          # 深灰文字
    font=("Microsoft YaHei UI", 10),
    relief="flat",         # 去掉默认凹陷边框
    padx=8,                # 文本框内部左右留白
    pady=8,                # 文本框内部上下留白
    wrap="word"            # 按单词/文字自然换行
)
detail_text.pack()


# 最下方：操作结果提示
result_label = tk.Label(status_frame, text="等待操作")
result_label.pack()


# 单击接口列表：自动显示详情
api_listbox.bind(
    "<<ListboxSelect>>",
    lambda event: show_selected_api(api_listbox, apis, result_label, detail_text)
)


# 双击接口列表：自动载入修改
api_listbox.bind(
    "<Double-Button-1>",
    lambda event: load_selected_api_to_entries(
        api_listbox,
        apis,
        name_entry,
        url_entry,
        key_entry,
        note_entry,
        result_label,
        editing_index
    )
)


# 程序启动时，先刷新一次接口目录
refresh_api_list(api_listbox, apis)


# 让窗口持续运行
window.mainloop()