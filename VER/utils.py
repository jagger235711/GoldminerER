import cv2
import os
from PIL import Image
from moviepy.editor import *


def video2data(path, cuts=[], p=2, auto_cut=None):
    """
    path: mp4文件路径
    cut = [(begin, end), (begin, end), ...]: 视频分段剪切
    p: 定义每秒抽取的图片数目
    auto_cut: 自动切割参数，可以是整数（表示分割数量）或浮点数（表示每段时长）
    """
    _, mp4_name = os.path.split(path)
    mp4_name = mp4_name.split(".")[0]
    mp4 = VideoFileClip(path)
    duration = mp4.duration

    # 如果auto_cut被指定，则自动生成cuts
    if auto_cut is not None:
        if isinstance(auto_cut, int):
            # 根据分割数量自动切割
            num_segments = auto_cut
            segment_length = duration / num_segments
            cuts = []
            for i in range(num_segments):
                start = i * segment_length
                end = (i + 1) * segment_length
                cuts.append((start, end))
        elif isinstance(auto_cut, float):
            # 根据每段时长自动切割
            segment_length = auto_cut
            num_segments = int(duration / segment_length)
            cuts = []
            for i in range(num_segments):
                start = i * segment_length
                end = (i + 1) * segment_length
                cuts.append((start, end))
            # 处理最后一段
            if num_segments * segment_length < duration:
                cuts.append((num_segments * segment_length, duration))

    # 创建必要的目录
    os.makedirs("./Repo/video/sub_mp4/", exist_ok=True)
    os.makedirs("./Repo/data/audio/", exist_ok=True)
    os.makedirs("./Repo/data/img/", exist_ok=True)

    sub_mp4 = list()
    if not len(cuts):
        sub_mp4.append(mp4)
    for sub_clip in cuts:
        sub_mp4 = mp4.subclip(sub_clip[0], sub_clip[1])
        sub_mp4.write_videofile(os.path.join("./Repo/video/sub_mp4/", mp4_name + f"sub{sub_clip[0]}_{sub_clip[1]}.mp4"))
    mp4.close()

    # 切完,开抽
    img_path = "./Repo/data/img"
    audio_path = "./Repo/data/audio"

    # 音频抽取
    print("抽音...")
    for sub_mp4_name in os.listdir("./Repo/video/sub_mp4"):
        this_mp4_path = os.path.join("./Repo/video/sub_mp4/", sub_mp4_name)
        sub_mp4 = AudioFileClip(this_mp4_path)
        sub_mp4.write_audiofile(os.path.join("./Repo/data/audio/", sub_mp4_name.split(".")[0] + ".wav"))
        sub_mp4.close()
    print("抽音完成")
    
    # 图片抽取
    print(mp4_name, "抽帧...")
    idx = 0
    for sub_mp4 in os.listdir("./Repo/video/sub_mp4"):
        idx += 1
        c = 1
        save_tag = 1
        this_mp4_path = os.path.join("./Repo/video/sub_mp4/", sub_mp4)
        this_capture = cv2.VideoCapture(this_mp4_path)
        fps = this_capture.get(5)
        while True:
            ret, frame = this_capture.read()
            if ret:
                frame_rate = int(fps) // p
                if c % frame_rate == 0:
                    # 抽取
                    cv2.imwrite(os.path.join(r"./Repo/data/img/", sub_mp4.split(".")[0] + f"{idx}_{save_tag}.jpg"), frame)
                    save_tag += 1
                c += 1
                cv2.waitKey(0)
            else:
                print(sub_mp4, "抽帧完成")
                break


def img2gif(p):
    gif_dict = dict()
    for img_name in os.listdir(p.img_results_path):
        # 处理文件名格式：momsub03_10.jpg
        # 我们需要提取前面的部分作为key，最后的数字部分作为序号
        if img_name.endswith('.jpg') and '_' in img_name:
            # 分割文件名
            parts = img_name[:-4].split("_")  # 去掉.jpg后缀后分割
            if len(parts) >= 2:
                # 格式：momsub03_10 -> gif_key = "momsub03", sequence_num = 10
                gif_key = parts[0]
                try:
                    sequence_num = int(parts[-1])
                    img_path = os.path.join(p.img_results_path, img_name)
                    img = cv2.imread(img_path)
                    if img is not None:
                        if gif_key in gif_dict.keys():
                            gif_dict[gif_key].append((sequence_num, img))
                        else:
                            gif_dict[gif_key] = [(sequence_num, img)]
                except (ValueError, IndexError):
                    # 如果解析失败，跳过这个文件
                    continue

    for gif_key in gif_dict.keys():
        if gif_dict[gif_key]:  # 确保列表不为空
            # 使用第一张图片的尺寸
            first_img = gif_dict[gif_key][0][1]
            w = first_img.shape[1]
            h = first_img.shape[0]

            gif = cv2.VideoWriter(os.path.join(p.gif_results_path, str(gif_key) + ".avi"), cv2.VideoWriter_fourcc('I', '4', '2', '0'), 2, (w, h))

            img_list = gif_dict[gif_key].copy()
            img_list.sort(key=lambda x: x[0])

            for img in [item[1] for item in img_list]:
                gif.write(img)

            gif.release()

    cv2.destroyAllWindows()
