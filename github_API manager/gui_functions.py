import tkinter as tk
from functions import save_apis


# 创建一组“标签 + 输入框”
def create_input(window, label_text):
    label = tk.Label(window, text=label_text)
    label.pack()

    entry = tk.Entry(window)
    entry.pack()

    return entry


# 刷新接口列表
def refresh_api_list(api_listbox, apis):
    api_listbox.delete(0, tk.END)

    for api in apis:
        api_listbox.insert(tk.END, api["name"] + " | " + api["base_url"])


# 清空所有输入框
def clear_entries(name_entry, url_entry, key_entry, note_entry):
    name_entry.delete(0, tk.END)
    url_entry.delete(0, tk.END)
    key_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)


# 添加接口
def add_api_from_entries(
    apis,
    name_entry,
    url_entry,
    key_entry,
    note_entry,
    api_listbox,
    result_label,
    editing_index
):
    if editing_index.get() != -1:
        result_label.config(text="当前正在修改接口，请点击“保存修改”，或先清空输入框")
        return
    
    name = name_entry.get()
    base_url = url_entry.get()
    api_key = key_entry.get()
    note = note_entry.get()

    if name == "" and base_url == "" and api_key == "" and note == "":
        result_label.config(text="请先填写接口信息，再点击添加")
        return


    api_info = {
        "name": name,
        "base_url": base_url,
        "api_key": api_key,
        "note": note
    }

    apis.append(api_info)
    save_apis(apis)

    clear_entries(name_entry, url_entry, key_entry, note_entry)
    refresh_api_list(api_listbox, apis)

    result_label.config(text="接口添加成功：" + name + " | " + base_url)


  # 查看选中接口的详情
def show_selected_api(api_listbox, apis, result_label, detail_text):
    selected = api_listbox.curselection()  # 获取当前选中的列表项

    if not selected:  # 如果没有选中任何接口
        result_label.config(text="笨蛋！你要先选一个呀QAQ！")
        return

    index = selected[0]  # 取出选中项的下标
    selected_api = apis[index]  # 找到选中的接口卡片

    detail_text.delete("1.0", tk.END)  # 清空旧详情内容
    detail_text.insert(tk.END, "厂商名：" + selected_api["name"] + "\n")
    detail_text.insert(tk.END, "Base URL：" + selected_api["base_url"] + "\n")
    detail_text.insert(tk.END, "API Key：" + selected_api["api_key"] + "\n")
    detail_text.insert(tk.END, "备注：" + selected_api["note"])

    result_label.config(text="已显示接口详情：" + selected_api["name"])


  # 删除选中的接口
def delete_selected_api(api_listbox, apis, result_label, detail_text):
    selected = api_listbox.curselection()

    if not selected:
        result_label.config(text="笨蛋！你要先选一个呀QAQ！")
        return

    index = selected[0]

    removed_api = apis.pop(index)
    save_apis(apis)
    refresh_api_list(api_listbox, apis)

    detail_text.delete("1.0", tk.END)  # 删除后清空详情框

    result_label.config(text="已删除接口：" + removed_api["name"])


# 把选中的接口信息载入到输入框
def load_selected_api_to_entries(
    api_listbox,
    apis,
    name_entry,
    url_entry,
    key_entry,
    note_entry,
    result_label,
    editing_index
):
    selected = api_listbox.curselection()

    if not selected:
        result_label.config(text="笨蛋！你要先选一个呀QAQ！")
        return

    index = selected[0]
    target_api = apis[index]

    editing_index.set(index)  # 记住当前正在修改哪一条接口

    clear_entries(name_entry, url_entry, key_entry, note_entry)

    name_entry.insert(0, target_api["name"])
    url_entry.insert(0, target_api["base_url"])
    key_entry.insert(0, target_api["api_key"])
    note_entry.insert(0, target_api["note"])

    result_label.config(text="已载入接口：" + target_api["name"])


# 保存修改后的接口
def save_edited_api(
    apis,
    name_entry,
    url_entry,
    key_entry,
    note_entry,
    api_listbox,
    result_label,
    editing_index
):
    index = editing_index.get()  # 取出当前正在修改的接口下标

    if index == -1:
        result_label.config(text="请先载入一个接口再修改")
        return

    apis[index]["name"] = name_entry.get()
    apis[index]["base_url"] = url_entry.get()
    apis[index]["api_key"] = key_entry.get()
    apis[index]["note"] = note_entry.get()

    save_apis(apis)
    refresh_api_list(api_listbox, apis)
    clear_entries(name_entry, url_entry, key_entry, note_entry)

    editing_index.set(-1)  # 修改完成后，退出修改状态

    result_label.config(text="接口修改成功！")