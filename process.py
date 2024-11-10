import numpy as np
import cv2


def show_image(title, image):
    cv2.imshow(title, image)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow(title)

img = cv2.imread('/home/bibrahim/PycharmProjects/Machine Learning/pdf_images/page_5.png')
show_image("image simple", img)

img_ = 255 - img
img_[img_ < 128] = 0
show_image("image simple 2", img_)


kernel = np.ones((5, 5), np.uint8)
img_dilation = cv2.dilate(img_, kernel, iterations=10)
show_image("image dilation", img_dilation)

gray = cv2.cvtColor(img_dilation, cv2.COLOR_BGR2GRAY)
show_image("image gray", gray)

thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (127, 12, 123), 3)

show_image("image contoured", img)