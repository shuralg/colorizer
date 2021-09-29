#!/usr/bin/python3.7
import argparse
import numpy as np
import cv2
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--issure_video", "-i", type=str, default='', help="Путь к файлу источника")
parser.add_argument("--result_folder", "-o", type=str, default='', help="Папка с результатом")
parser.add_argument("--frames_step", "-f", type=int, default=1, help="Шаг выборки кадров")
parser.add_argument("--gaussian", "-g", type=int, default=3, help="Интенсивность размытия Гаусса")
parser.add_argument("--fx", "-fx", type=float, default=1., help="коэффициент изменения изображения по оси X")
parser.add_argument("--fy", "-fy", type=float, default=1., help="коэффициент изменения изображения по оси Y")

parser.add_argument("--start_frame_number", "-s", type=int, default=300, help="Номер начального кадра (отсчет с 0)")
parser.add_argument("--threshold", "-t", type=int, default=100, help="Порог чувствительности для контуров")
parser.add_argument("--end_frame_number", "-e", type=int, default=300,
                    help="Номер заключительного кадра")
opt = parser.parse_args()

# print("Путь к источнику: ", opt.issure_video)
file_name = opt.issure_video

vidcap = cv2.VideoCapture(file_name)

total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)  # amount frames

if opt.end_frame_number <= 0:
    opt.end_frame_number = total_frames + opt.end_frame_number
elif total_frames < opt.end_frame_number:
    opt.end_frame_number = total_frames

if opt.start_frame_number > total_frames \
        or opt.start_frame_number >= opt.end_frame_number:
    print('У Вас слишком короткое видео, не создано ни одного тестового набора')
    exit()

if opt.frames_step <= 0:
    opt.frames_step = 1

ret, frame = vidcap.read()
if ret:
    frame = cv2.resize(frame, (0, 0), fx=opt.fx, fy=opt.fy)
    print('Shape: ', frame.shape)
else:
    exit()

for num in tqdm(range(int(opt.start_frame_number), int(opt.end_frame_number), int(opt.frames_step))):
    vidcap.set(1, num)
    ret, frame = vidcap.read()
    if ret:
        frame = cv2.resize(frame, (0, 0), fx=opt.fx, fy=opt.fy)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (opt.gaussian, opt.gaussian), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(gray, opt.threshold, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        res_img = np.full(frame.shape, 255, dtype=np.uint8)

        cv2.drawContours(res_img, contours, -1, (0, 0, 0), 1, cv2.LINE_AA, hierarchy, 3)
        vis = np.concatenate((frame, res_img), axis=1)

        cv2.imwrite(opt.result_folder + '/' + str(num) + '.jpg', vis)
