import cv2
import numpy
import os

import shutil
from glob import glob


def extract_image_from_replay(movie_path: str, image_directory_path: str):
    cap = cv2.VideoCapture(movie_path)
    delay = 1
    window_name = 'frame'
    cnt = 0

    # shutil.rmtree(image_directory_path)
    # shutil.rmtree('output')

    os.makedirs(image_directory_path, exist_ok=True)
    os.makedirs('../../output', exist_ok=True)

    if not cap.isOpened():
        exit()

    while True:
        ret, frame = cap.read()

        if ret:
            cv2.imshow(window_name, frame)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

            if cnt % 60 == 0:
                cv2.imwrite(f'{image_directory_path}{cnt:06d}.png', frame[535:, 1095:])
            
            cnt += 1

        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    cv2.destroyWindow(window_name)


def detect_rectangle(image_path: str):
    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # print(len(contours))

    max_cnt = max(contours, key=lambda x: cv2.contourArea(x))

    if cv2.contourArea(max_cnt) > 100:
        x, y, w, h = cv2.boundingRect(max_cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
   

    # for c in contours:
    #     area = cv2.contourArea(c)

    #     print(area)

    #     if area > 26.9:
    #         x, y, w, h = cv2.boundingRect(c)
    #         cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)
    
    # 結果の画像作成
    # cv2.imwrite('output.png', img)
    cv2.imwrite(image_path.replace('images', 'output'), img)


def create_movie(movie_path: str, image_paths: list):
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    video  = cv2.VideoWriter(movie_path, fourcc, 30.0, (185, 185))

    print('len: ', len(image_paths))

    for image_path in image_paths:
        img = cv2.imread(image_path)

        # print(img.shape)
        video.write(img)

        # print(image_path)

    video.release()



if __name__ == '__main__':
    movie_file_path = '../../movie/target_movie.webm'
    output_movie_file_path = '../../movie/output.mp4'
    image_directory_path = '../../images/'
    # image_path = '../../images/001200.png'

    extract_image_from_replay(movie_file_path, image_directory_path)

    image_paths = sorted(glob('../../images/*.png'))

    for image_path in image_paths:
        detect_rectangle(image_path)

    create_movie(output_movie_file_path, sorted(glob('../../output/*.png')))

    print('finished.')