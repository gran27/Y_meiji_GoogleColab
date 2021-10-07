import argparse

import csv
import cv2
import numpy as np
import torch

from . import detect_ymeiji
from . import detect_mouse
from . import utils


def detect_arm(img, center, coefs_line, radius_range, model):
    arms_name = ["A", "B", "C"]
    # mouse_pos = detect_mouse.get_mousepos(img)
    mouse_pos = detect_mouse.get_mousepos_model(img, model)

    if mouse_pos is not None:
        x, y, w, h = mouse_pos
        mouse_pos = [x + w / 2, y + h / 2]
        r = utils.dist_between(center, mouse_pos)
        if r >= radius_range[0] and r <= radius_range[1]:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            for i in range(3):
                d = utils.dist_point_line(mouse_pos, coefs_line[i])
                if i == 0:
                    d_min = d
                    arm = arms_name[i]
                elif d < d_min:
                    d_min = d
                    arm = arms_name[i]
        else:
            return img, None
    else:
        return img, None

    return img, arm


def create_armslist(
    file, center, edges, coefs_line, radius_range, start, end, outspeed
):
    arms = []
    prev_arm = ""
    set_arms = False
    edges_name = ["A", "B", "C"]

    model = torch.hub.load("ultralytics/yolov5", "custom", path="model/best.pt")
    model.conf = 0.5
    model.iou = 0.4

    cap = cv2.VideoCapture(file)

    if not cap.isOpened():
        print(f"Can't open {file}")
        exit()

    out = file.replace("data", "result")
    if "MTS" in file:
        out = out.replace("MTS", "mp4")
    # print(out)
    rst = cv2.VideoWriter(
        out, cv2.VideoWriter_fourcc("m", "p", "4", "v"), 30, (960, 540)
    )

    cnt = 0
    # print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if start:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(start * cap.get(cv2.CAP_PROP_FPS)))
    try:
        while True:
            ret, frame = cap.read()
            # print(ret, frame)
            if ret:
                frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
                frame_no = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                now_second = int(frame_no / cap.get(cv2.CAP_PROP_FPS))
                min, sec = divmod(now_second, 60)
                # print(frame_no, now_second)
                if frame_no > end * cap.get(cv2.CAP_PROP_FPS):
                    break
                w, h, _ = frame.shape
                frame, arm = detect_arm(frame, center, coefs_line, radius_range, model)
                if set_arms:
                    if prev_arm != arm and arm is not None:
                        arms.append(arm)
                        prev_arm = arm
                        print(arm)
                else:
                    if arm == "B":
                        coefs_line = np.roll(coefs_line, 2, axis=0)
                    elif arm == "C":
                        coefs_line = np.roll(coefs_line, 1, axis=0)
                    set_arms = True

                cv2.circle(
                    frame,
                    (int(center[0]), int(center[1])),
                    int(radius_range[0]),
                    (0, 0, 255),
                    2,
                )
                for i, edge in enumerate(edges):
                    cv2.putText(
                        frame,
                        edges_name[i],
                        (int(edge[0]) + 20, int(edge[1]) + 20),
                        fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1.0,
                        color=(39, 127, 255),
                        thickness=2,
                        lineType=cv2.LINE_4,
                    )
                cv2.putText(
                    frame,
                    f"{min}:{sec:02}",
                    org=(int(w * 0.05), int(h * 0.05)),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=1,
                    color=(255, 255, 255),
                    thickness=3,
                    lineType=cv2.LINE_4,
                )
                cv2.putText(
                    frame,
                    f"{min}:{sec:02}",
                    org=(int(w * 0.05), int(h * 0.05)),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=1,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4,
                )
                # arm_name
                cv2.putText(
                    frame,
                    prev_arm,
                    org=(int(w * 0.1), int(h * 0.2)),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=3.0,
                    color=(255, 255, 255),
                    thickness=10,
                    lineType=cv2.LINE_4,
                )
                cv2.putText(
                    frame,
                    prev_arm,
                    org=(int(w * 0.1), int(h * 0.2)),
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=3.0,
                    color=(0, 0, 0),
                    thickness=4,
                    lineType=cv2.LINE_4,
                )
                # cv2_imshow(frame)
                if cnt % outspeed == 0:
                    rst.write(frame)
                cnt += 1
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("中断されました")
                    exit()
            else:
                break
    except KeyboardInterrupt:
        print("中断されました")
        exit()

    cap.release()
    rst.release()
    cv2.destroyAllWindows()

    return arms


def get_coefs(center, edges):
    coefs = np.zeros((3, 3))

    for i in range(3):
        coefs[i] = utils.coors_to_linearfunction(center, edges[i], form="general")
        r = utils.dist_between(center, edges[i])
        if i == 0:
            r_max = r
        elif r < r_max:
            r_max = r
    r_min = r_max * 0.15
    radius_range = [r_min, r_max]

    return coefs, radius_range


def check_filelen(file, shift):
    eightmin = 8 * 60  # second
    cap = cv2.VideoCapture(file)

    if not cap.isOpened():
        print(f"Can't open {file}")
        exit()

    fps = cap.get(cv2.CAP_PROP_FPS)
    count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    start = shift * fps
    end = (shift + eightmin) * fps
    try:
        assert start < count and end < count, "動画が8分未満になるため評価を開始できません"
    except AssertionError as err:
        print("AssertionError :", err)
    cap.release()
    return shift, shift + eightmin


def has_duplicates(seq):
    return len(seq) != len(set(seq))


def evaluation(arms):
    activity = len(arms) - 1
    working_memory = 0
    for i in range(len(arms) - 2):
        # print(i, arms[i : i + 3])
        if not has_duplicates(arms[i : i + 3]):
            working_memory += 1
    working_memory = working_memory * 100 / (activity - 1)

    return activity, working_memory


def save(file, arms, activity, working_memory):
    activity = str(activity)
    working_memory = str(working_memory)
    header = ["route", "activity", "working_memory"]
    contents = [arms, activity, working_memory]

    if "csv" in file:
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            contents = [arms[0], activity, working_memory]
            writer.writerow(contents)
            for i in range(1, len(arms)):
                contents = [arms[i], "", ""]
                writer.writerow(contents)

    elif "txt" in file:
        contents = ["".join(arms), activity, working_memory]
        with open(file.replace("csv", "txt"), "w") as f:
            writer = csv.writer(f)
            for i in range(len(header)):
                f.write(f"{header[i]}:\n{contents[i]}\n\n")

    print(f"Saved result to {file}")


def main(args):
    file = args.file
    shift = args.shift
    outspeed = args.outspeed
    yth = args.yth

    outfile = file
    ext = outfile.rsplit(".", 1)[-1]
    outfile = outfile.replace(ext, args.output).replace("data", "result")

    start, end = check_filelen(file, shift)  # second
    center, edges = detect_ymeiji.getpoints(file, yth)
    coefs_line, radius_range = get_coefs(center, edges)
    arms = create_armslist(
        file, center, edges, coefs_line, radius_range, start, end, outspeed
    )
    activity, working_memory = evaluation(arms)
    print("activity:", activity)
    print("working_memory:", f"{working_memory:.2f}")
    save(outfile, arms, activity, working_memory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluation for mouse Y_meiji experiment."
    )
    parser.add_argument(
        "file",
        type=str,
        help="video file path (ex: ./data/01504.MTS)",
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=["csv", "txt"],
        default="csv",
        help="format of output file",
    )
    parser.add_argument(
        "--shift",
        type=float,
        default=0,
        help="video shift",
    )
    parser.add_argument(
        "--outspeed",
        type=int,
        default=1,
        help="X speed for output video file",
    )
    parser.add_argument(
        "--yth",
        type=float,
        default=0.1,
        help="If smaller, accuracy to find Y-meiji edges is better (Default: 0.1)",
    )
    args = parser.parse_args()
    main(args)
