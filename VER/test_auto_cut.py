#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import video2data

def test_auto_cut():
    """测试自动切割功能"""

    # 测试视频路径
    test_video_path = os.path.join("./Repo/video/mp4/", "mom.mp4")

    if not os.path.exists(test_video_path):
        print(f"测试视频文件不存在: {test_video_path}")
        return

    print("测试自动切割功能...")

    # 测试1: 自动切割为5段
    print("\n测试1: 自动切割为5段")
    try:
        video2data(path=test_video_path, auto_cut=5, p=2)
        print("✓ 自动切割为5段成功")
    except Exception as e:
        print(f"✗ 自动切割为5段失败: {e}")

    # 清理生成的文件
    import shutil
    if os.path.exists("./Repo/video/sub_mp4/"):
        shutil.rmtree("./Repo/video/sub_mp4/")
    if os.path.exists("./Repo/data/audio/"):
        shutil.rmtree("./Repo/data/audio/")
    if os.path.exists("./Repo/data/img/"):
        shutil.rmtree("./Repo/data/img/")

    # 测试2: 自动切割为每段10秒
    print("\n测试2: 自动切割为每段10秒")
    try:
        video2data(path=test_video_path, auto_cut=10.0, p=2)
        print("✓ 自动切割为每段10秒成功")
    except Exception as e:
        print(f"✗ 自动切割为每段10秒失败: {e}")

    print("\n自动切割功能测试完成!")

if __name__ == "__main__":
    test_auto_cut()
