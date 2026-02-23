import os
import re
from pathlib import Path

# 定义支持的文件后缀
VALID_EXTENSIONS = {
    '.mkv', '.mp4', '.avi', '.rmvb', '.flv', '.wmv', '.mov', '.ts', '.webm',
    '.ass', '.srt', '.ssa', '.vtt', '.sub'
}


def get_episode_number(filename):
    """
    核心提取逻辑：从文件名中智能提取集数
    """
    # 1. 移除 [] 和 () 及其内容
    cleaned = re.sub(r'\[.*?\]|\(.*?\)', '', filename)
    # 2. 移除 v2/v3 等版本标识
    cleaned = re.sub(r'v\d+', '', cleaned, flags=re.IGNORECASE)
    # 3. 提取剩余文本中的所有数字
    numbers = re.findall(r'\d+', cleaned)

    if numbers:
        # 取最后一个数字作为集数
        try:
            return int(numbers[-1])
        except (ValueError, IndexError):
            return None
    return None


def generate_rename_plan(folder_path, show_name, season_num, format_str):
    """
    根据路径和规则，生成重命名任务列表
    :param folder_path: NAS 上的绝对路径
    :param show_name: 番剧名称
    :param season_num: 季数 (整数)
    :param format_str: 命名格式模板，例如 "{n} S{s}E{e}"
    :return: 包含任务字典的列表
    """
    plan = []
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        return {"error": "路径不存在或不是文件夹"}

    # 遍历并排序文件
    files = sorted([f for f in folder.iterdir() if f.is_file()])

    for file_path in files:
        if file_path.suffix.lower() in VALID_EXTENSIONS:
            ep_num = get_episode_number(file_path.name)

            if ep_num is not None:
                # 解析自定义格式
                new_stem = format_str.replace("{n}", show_name) \
                    .replace("{s}", f"{int(season_num):02d}") \
                    .replace("{e}", f"{int(ep_num):02d}")

                new_name = f"{new_stem}{file_path.suffix}"

                plan.append({
                    "old_name": file_path.name,
                    "new_name": new_name,
                    "status": "pending"  # 状态标记，方便前端展示
                })
            else:
                # 如果没识别到集数，原样保留或标记错误
                plan.append({
                    "old_name": file_path.name,
                    "new_name": "无法识别集数",
                    "status": "error"
                })

    return plan


def execute_rename_file(folder_path, old_name, new_name):
    """
    执行单个文件的重命名
    """
    try:
        old_path = Path(folder_path) / old_name
        new_path = Path(folder_path) / new_name

        if old_path.exists() and old_name != new_name:
            # 检查目标文件名是否已存在，防止覆盖
            if new_path.exists():
                return False, f"目标文件已存在: {new_name}"

            old_path.rename(new_path)
            return True, "成功"
        return False, "文件不存在或名称未改变"
    except Exception as e:
        return False, str(e)