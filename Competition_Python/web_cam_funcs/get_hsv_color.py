# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 读取图像
image = cv2.imread('../example_img/2024-04-29-015835_3840x2160_scrot.png')  # 替换为你的图像文件路径
print(image)

selected_pixels = []  # 用于保存鼠标点击的像素位置列表
hsv_values = []  # 用于保存对应的HSV值列表

# 定义鼠标点击事件的回调函数
def mouse_callback(event, x, y, flags, param):
    global selected_pixel, hsv_value

    if event == cv2.EVENT_LBUTTONDOWN:
        selected_pixel = (x, y)  # 记录鼠标点击的像素位置
        selected_pixels.append(selected_pixel)

        # 获取像素位置处的BGR值
        bgr_value = image[y, x]

        # 将BGR值转换为HSV值
        bgr_value = np.uint8([[bgr_value]])  # 将像素值转换为uint8类型的数组
        hsv_value = cv2.cvtColor(bgr_value, cv2.COLOR_BGR2HSV)
        hsv_values.append(hsv_value[0, 0])

        # 显示HSV值
        print("HSV value at pixel ({}, {}): {}".format(x, y, hsv_value[0, 0]))


# 显示图像并设置鼠标点击事件的回调函数
cv2.imshow('Image', image)
cv2.setMouseCallback('Image', mouse_callback)

while True:
    # 在图像上绘制选择的像素位置
    for pixel in selected_pixels:
        cv2.circle(image, pixel, 3, (255, 0, 0), -1)

    # 显示图像
    cv2.imshow('Image', image)

    # 按下'q'键计算平均值、最大值和最小值并退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if hsv_values:
            hsv_values_array = np.array(hsv_values)
            average_hsv = np.mean(hsv_values_array, axis=0)
            min_hsv = np.min(hsv_values_array, axis=0)
            max_hsv = np.max(hsv_values_array, axis=0)
            print("Average HSV:", average_hsv)
            print("Minimum HSV:", min_hsv)
            print("Maximum HSV:", max_hsv)
        break

# 释放资源并关闭窗口
cv2.destroyAllWindows()
