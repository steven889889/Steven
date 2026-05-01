import json
import os

DATA_FILE = "apis.json"


# 显示主菜单
def main_menu():
    print()
    print("=== API 接口管理器 ===")
    print("1. 添加接口")
    print("2. 查看接口目录")
    print("3. 查看接口详情")
    print("4. 删除接口")
    print("5. 修改接口")
    print("6. 保存并退出")


# 保存接口数据
def save_apis(apis):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(apis, file, ensure_ascii=False, indent=4)


# 读取接口数据
def load_apis():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# 添加一个新的 API 接口
def add_api(apis):
    print()
    print("=== 添加接口 ===")

    name = input("厂商名：")
    base_url = input("Base URL：")
    api_key = input("API Key：")
    note = input("备注：")

    api_info = {
        "name": name,
        "base_url": base_url,
        "api_key": api_key,
        "note": note
    }

    apis.append(api_info)
    save_apis(apis)

    print()
    print("接口添加成功！")
    print("厂商名：", api_info["name"])
    print("Base URL：", api_info["base_url"])


# 查看接口目录，只显示厂商名和 URL
def list_apis(apis):
    print()
    print("=== 接口目录 ===")

    if not apis:
        print("当前的 API 接口列表为空")
        return

    for index, api in enumerate(apis, start=1):
        print(f"{index}. {api['name']} | {api['base_url']}")


# 选择一个接口，返回它在列表中的下标
def select_api_index(apis, action_name):
    if not apis:
        print(f"当前没有任何接口可以{action_name}")
        return None

    list_apis(apis)

    choice = input(f"请输入要{action_name}的接口编号：")

    if not choice.isdigit():
        print("请输入有效的数字编号")
        return None

    index = int(choice) - 1

    if index < 0 or index >= len(apis):
        print("编号不存在，请重新选择")
        return None

    return index


# 查看某个接口的完整详情
def view_api_detail(apis):
    print()
    print("=== 查看接口详情 ===")

    index = select_api_index(apis, "查看")
    if index is None:
        return

    api = apis[index]

    print()
    print("=== 接口详情 ===")
    print("厂商名：", api["name"])
    print("Base URL：", api["base_url"])
    print("API Key：", api["api_key"])
    print("备注：", api["note"])


# 删除接口
def delete_api(apis):
    print()
    print("=== 删除接口 ===")

    index = select_api_index(apis, "删除")
    if index is None:
        return

    removed_api = apis.pop(index)
    save_apis(apis)

    print("已删除接口：", removed_api["name"])


# 修改接口
def edit_api(apis):
    print()
    print("=== 修改接口 ===")

    index = select_api_index(apis, "修改")
    if index is None:
        return

    target_api = apis[index]

    print()
    print("你正在修改：", target_api["name"])

    print("当前厂商名：", target_api["name"])
    new_name = input("新的厂商名（直接回车则不修改）：")
    if new_name != "":
        target_api["name"] = new_name

    print("当前 Base URL：", target_api["base_url"])
    new_url = input("新的 Base URL（直接回车则不修改）：")
    if new_url != "":
        target_api["base_url"] = new_url

    print("当前 API Key：", target_api["api_key"])
    new_key = input("新的 API Key（直接回车则不修改）：")
    if new_key != "":
        target_api["api_key"] = new_key

    print("当前备注：", target_api["note"])
    new_note = input("新的备注（直接回车则不修改）：")
    if new_note != "":
        target_api["note"] = new_note

    save_apis(apis)
    print("接口修改成功！")