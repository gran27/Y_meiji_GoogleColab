import argparse

import itertools
import cv2
import numpy as np

from . import utils

# import utils


def getpoints_auto(file, playback_pos=0.5):
    cap = cv2.VideoCapture(file)

    if not cap.isOpened():
        print(f"Can't open {file}")
        exit()

    cap.set(
        cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * playback_pos)
    )
    ret, frame = cap.read()
    if ret:
        img = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kernel = np.ones((5, 5), np.uint8)
        _, img_binary = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
        img_ero = cv2.erode(img_binary, kernel, iterations=1)
        img_dil = cv2.dilate(img_ero, kernel, iterations=3)

        # find feature points
        corners = cv2.goodFeaturesToTrack(img_gray, 10, 0.05, 30)
        corners = np.int0(corners)

        # select 4 points from 10 points
        corners_reshape = []
        for corner in corners:
            x, y = corner.ravel()
            corners_reshape.append([x, y])
            x, y = corner.ravel()
            cv2.circle(img, (x, y), 6, (0, 150, 150), -1)
        x_min, y_min = np.argmin(corners_reshape, axis=0)
        x_max, y_max = np.argmax(corners_reshape, axis=0)

        corners_select = []
        for i in [x_min, y_min, x_max, y_max]:
            corners_select.append(corners_reshape[i])
            [x, y] = corners_reshape[i]
            cv2.circle(img, (x, y), 6, (100, 50, 100), -1)

        # find pairs of points
        first = True
        for (i1, v1), (i2, v2) in itertools.combinations(enumerate(corners_select), 2):
            if first:
                thickness = utils.dist_between(v1, v2)
                point_shortset = [i1, i2]
                first = False
            elif utils.dist_between(v1, v2) < thickness:
                thickness = utils.dist_between(v1, v2)
                point_shortset = [i1, i2]

        point_longset = []
        for i in range(4):
            if i not in point_shortset:
                point_longset.append(i)

        center_long = utils.interior_division(
            corners_select[point_longset[0]], corners_select[point_longset[1]], 1, 1
        )
        center_short = utils.interior_division(
            corners_select[point_shortset[0]], corners_select[point_shortset[1]], 1, 1
        )

        # calculate center point and 3 edge points
        # parameter for center = 1.7
        center = utils.interior_division(center_long, center_short, 1, 1.7)
        cv2.circle(img, (int(center[0]), int(center[1])), 6, (0, 0, 255), -1)
        pixelnum = 0
        pixelnum_valid = 0
        edges = []
        for i in range(3):
            edge = utils.rotation_point(center_short, center, 120 * i)
            edges.append(edge)
            cv2.circle(img, (int(edge[0]), int(edge[1])), 6, (255, 0, 0), -1)
            pixels = utils.pixel_between(center, edge)
            pixelnum += len(pixels)

            for pixel in pixels:
                if img_dil[pixel[1]][pixel[0]] == 255:
                    cv2.circle(
                        img, (int(pixel[0]), int(pixel[1])), 1, (39, 127, 255), -1
                    )
                    pixelnum_valid += 1

    cap.release()
    cv2.destroyAllWindows()

    return center, edges, pixelnum_valid / pixelnum


def show(file, center, edges):
    if "mp4" in file:
        out = file.replace("data", "result").replace("mp4", "jpg")
    elif "MTS" in file:
        out = file.replace("data", "result").replace("MTS", "jpg")

    # edges_name = ["A", "B", "C"]
    cap = cv2.VideoCapture(file)

    if not cap.isOpened():
        print(f"Can't open {file}")
        exit()

    ret, frame = cap.read()
    # print(ret, frame)
    if ret:
        # cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        img = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
        cv2.circle(img, (int(center[0]), int(center[1])), 6, (0, 0, 255), -1)
        for _, edge in enumerate(edges):
            cv2.circle(img, (int(edge[0]), int(edge[1])), 6, (128, 0, 128), -1)
            """
            cv2.putText(
                img,
                edges_name[i],
                (int(edge[0]) + 20, int(edge[1]) + 20),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=1.0,
                color=(128, 0, 128),
                thickness=2,
                lineType=cv2.LINE_4,
            )
            """
            pixels = utils.pixel_between(center, edge)
            for pixel in pixels:
                cv2.circle(img, (int(pixel[0]), int(pixel[1])), 1, (39, 127, 255), -1)
        cv2.imwrite(out, img)
        # cv2.imshow("", img)

        # print("何かキーを押してください")
        # cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()


def yes_no_input():
    while True:
        choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
        if choice in ["y", "ye", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False


def getpoints(file, yth):
    poss = np.arange(0.1, 1.0, yth)
    fit_degree_max = 0
    for pos in poss:
        # print(i, pos)
        center_ten, edges_ten, fit_degree = getpoints_auto(file, pos)
        if fit_degree > fit_degree_max:
            center, edges, fit_degree_max = center_ten, edges_ten, fit_degree
    # print(center, edges, fit_degree_max)
    # edges = np.roll(edges, 2, axis=0)
    show(file, center, edges)
    # print("ラインが迷路に沿っている場合は「y」、沿っていない場合は「n」を入力してEnterを押してください")
    print("resultフォルダ内の画像を確認しましたか？")
    if not yes_no_input():
        print("確認してから再実行してください")
        exit()
    return center, edges


def main(args):
    getpoints(args.file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluation for mouse Y_meiji experiment."
    )
    parser.add_argument(
        "file",
        type=str,
        # default="./data/01504.MTS",
        # default="../data/00892.MTS",
        help="video file path (ex: ./data/01504.MTS)",
    )
    args = parser.parse_args()
    # debug(args)
    main(args)
