# -*- coding: utf-8 -*-
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import cv2
import numpy as np
from io import BytesIO
import time
import requests
import random


class CrackSlider(object):
    def __init__(self):
        self.phone_num = "15638749981"
        self.password = "syf11140725com"

        self.driver = webdriver.Chrome(executable_path=r'D:\softwares\chromedriver\chromedriver.exe')
        # self.browser = webdriver.Firefox(executable_path=r'C:/Users/YuFeiSun/Desktop/滑动验证码3/geckodriver.exe')
        # self.driver = webdriver.Edge()
        # self.wait = WebDriverWait(self.driver, 20)
    def password_login(self):
        self.driver.find_element_by_id("normalLogin").click()



    def open(self):
        self.driver.get("https://www.qichacha.com/user_login?back=%2F")
        time.sleep(1)
        self.driver.maximize_window()
        time.sleep(1)
        self.password_login()
        phone_num = self.driver.find_element_by_id("nameNormal")
        phone_num.send_keys(self.phone_num)
        password = self.driver.find_element_by_id("pwdNormal")
        password.send_keys(self.password)

    def get_geetest_button(self):
        botton = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "nc_iconfont btn_slide")))
        return botton

    def get_pic(self):
        """
        保存验证码图片
        """
        time.sleep(5)
        # target:得到验证图片
        # template:得到小滑块图片
        target = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mark"]/div/div/div[1]/div[1]/img')))
        template = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="slideBlock"]/img')))
        # 获取图片的链接
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        # 将图片保存在本地
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('target.jpg')
        template_img.save('template.png')
        # 对图片进行缩放，网页上的原版图片是230像素，和保存在本地之后的图像大小进行除法，得到缩放系数
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        self.zoom = 230 / int(size_loc[0])

    def get_tracks(self, distance):
        """
        模拟滑动轨迹
        """
        print(distance)
        # 移动的总距离增加x像素，我们会在移动过程中增加x像素的随机回退
        # 调整回退像素可以减少滑动时间，但是相应的错误率会增加。
        distance += 10
        forward_tracks = []
        current = 0
        # mid 设置减速阈值，加速滑动到减速滑动
        mid = distance * 3 / 4
        t = random.randint(2, 3) / 5
        v = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            # 保留整数部分的move
            forward_tracks.append(round(move))

        # 设置随机的回退
        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -2]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    @staticmethod
    def match(target, template):
        """
        识别图片应该移动的位置
        """
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        w, h = template.shape[::-1]
        print(w, h)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 10:
            run += 1
            threshold = (R + L) / 2

            print(threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            # print(len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2
        return loc[1][0]

    def crack_slider(self):
        """
        拖动鼠标进行滑动
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnSlide')))
        ActionChains(self.driver).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.driver).move_by_offset(xoffset=-4, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=4, yoffset=0).perform()
        time.sleep(0.5)

        ActionChains(self.driver).release().perform()

    def run(self):
        success = self.wait.until(
            EC.text_to_be_present_in_element((By.XPATH, '//*[@id="mark"]/div/div/div[1]/div[2]/p/text()'), '验证成功'))
        print(success)


if __name__ == '__main__':
    cs = CrackSlider()
    # 开始计时
    start = time.time()
    # 使用浏览器driver打开链接，输入手机号和密码
    cs.open()
    # 点击获取验证码
    cs.get_geetest_button().click()
    # 获取验证码图片target和小滑块图片template
    target = 'target.jpg'
    template = 'template.png'
    cs.get_pic()
    # 计算滑动距离
    distance = cs.match(target, template)
    # 模拟滑动轨迹
    tracks = cs.get_tracks((distance + 7) * cs.zoom)
    #滑动
    cs.crack_slider()
    # cs.run()
    end = time.time()
    # 计算用时
    print("滑动验证码用时： %s秒"%(str(int(end - start))))























