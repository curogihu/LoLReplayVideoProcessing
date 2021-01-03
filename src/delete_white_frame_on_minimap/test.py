import cv2
import numpy
import os

import shutil


def main(movie_path: str, image_directory_path: str):
    cap = cv2.VideoCapture(movie_path)
    delay = 1
    window_name = 'frame'
    cnt = 0

    shutil.rmtree(image_directory_path)
    os.makedirs(image_directory_path, exist_ok=True)

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

    # print(os.path.exists(image_path))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    print(len(contours))

    for c in contours:
        area = cv2.contourArea(c)

        print(area)

        if area > 1973:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)


    # blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    # # canny = cv2.Canny(blurred, 120, 255, 1)
    # canny = cv2.Canny(blurred, 0, 30, 1)

    # # Find contours
    # cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # # Iterate thorugh contours and draw rectangles around contours
    # for c in cnts:
    #     x, y, w, h = cv2.boundingRect(c)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)


    # # Find contours
    # cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # # Iterate thorugh contours and draw rectangles around contours
    # for c in cnts:
    #     x, y, w, h = cv2.boundingRect(c)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)

    # # 輪郭を抽出
    # _, contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # font = cv2.FONT_HERSHEY_DUPLEX
    # rectangle = 0

    # for cnt in contours:
    #     approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    #     cv2.drawContours(img, [approx], 0, (0), 2)
    #     x = approx.ravel()[0]
    #     y = approx.ravel()[1]

    #     for cnt in contours:
    #         approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    #         cv2.drawContours(img, [approx], 0, (0), 2)
    #         x = approx.ravel()[0]
    #         y = approx.ravel()[1]

    #         if len(approx) == 4:
    #             # rectangle +=1
    #             cv2.putText(img, "rectangle{}".format(rectangle),  (x, y), font, 0.8, (0))?
    
    # 結果の画像作成
    cv2.imwrite('output.png',img)


if __name__ == '__main__':
    movie_file_path = '../../movie/target_movie.webm'
    image_directory_path = '../../images/'
    image_path = '../../images/001620.png'

    # main(movie_file_path, image_directory_path)

    detect_rectangle(image_path)