import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/softwares/tesseract/tesseract.exe'
import urllib.request
import time
# https://www.tcpjw.com/Content/Images/201908141842014385955.jpg
def get_full_name(pic_link, item_person):
    urllib.request.urlretrieve(pic_link, '%s.png' % item_person)
    image = cv2.imread('%s.png' % item_person, 1)

    #二值化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    cv2.waitKey(0)

    rows, cols = binary.shape
    scale = 40
    #识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(cols//scale,1))
    eroded = cv2.erode(binary,kernel,iterations = 1)
    # cv2.imshow("Eroded Image",eroded)
    dilatedcol = cv2.dilate(eroded,kernel,iterations = 1)

    #识别竖线
    scale = 20
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,rows//scale))
    eroded = cv2.erode(binary,kernel,iterations = 1)
    dilatedrow = cv2.dilate(eroded,kernel,iterations = 1)

    #标识交点
    bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)

    #标识表格
    merge = cv2.add(dilatedcol,dilatedrow)
    cv2.waitKey(0)

    #识别黑白图中的白色点
    ws,hs = np.where(bitwiseAnd>0)
    mylistw=[]
    mylisth=[]

    #通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值，我只取最后一点
    i = 0
    myxs=np.sort(hs)
    for i in range(len(myxs)-1):
        if(myxs[i+1]-myxs[i]>10):
            mylisth.append(myxs[i])
        i=i+1
    mylisth.append(myxs[i])


    i = 0
    myys = np.sort(ws)

    for i in range(len(myys)-1):
        if(myys[i+1]-myys[i]>10):
            mylistw.append(myys[i])
        i=i+1
    mylistw.append(myys[i])
    # hhhhhhhhhhhhhhhhhhh
    print(mylistw, len(mylistw))
    # wwwwwwwwwwwwwwwww
    print(mylisth,len(mylisth))

    # 银行承兑汇票情况1
    if len(mylistw) ==13 and len(mylisth) ==7:

        ROI = image[mylistw[0]:mylistw[4], mylisth[0]:mylisth[-1]]
        # print(mylistw[0],mylistw[4], mylisth[0], mylisth[-1])
        # 账号 1
        account_num_1 = image[mylistw[0]:mylistw[1], mylisth[2]:mylisth[3]]
        # 全称1
        full_name_1 = image[mylistw[1]:mylistw[2], mylisth[2]:mylisth[3]]
        # 开户行1
        bank_name_1 = image[mylistw[2]:mylistw[3], mylisth[2]:mylisth[3]]
        # 开户行号1
        bank_name_num_1 = image[mylistw[3]:mylistw[4], mylisth[2]:mylisth[3]]

        # 账号 2
        account_num_2 = image[mylistw[0]:mylistw[1], mylisth[5]:mylisth[6]]
        # 全称 2
        full_name_2 = image[mylistw[1]:mylistw[2], mylisth[5]:mylisth[6]]
        # 开户行 2
        bank_name_2 = image[mylistw[2]:mylistw[3], mylisth[5]:mylisth[6]]
        # 开户行号 2
        bank_name_num_2 = image[mylistw[3]:mylistw[4], mylisth[5]:mylisth[6]]

        # 账号 1
        x, y = account_num_1.shape[0:2]
        account_num_1 = cv2.resize(account_num_1, (int(2 * y), int(2 * x)))
        # 全称1
        x, y = full_name_1.shape[0:2]
        full_name_1 = cv2.resize(full_name_1, (int(2 * y), int(2 * x)))

        # 账号 2
        x, y = account_num_2.shape[0:2]
        account_num_2 = cv2.resize(account_num_2, (int(2 * y), int(2 * x)))
        # 全称2
        x, y = full_name_2.shape[0:2]
        full_name_2 = cv2.resize(full_name_2, (int(2 * y), int(2 * x)))
        # cv2.imshow("Cut Image", ROI)

        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_account_num_1.png' % item_person, account_num_1)
        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_full_name_1.png' % item_person, full_name_1)
        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_1.png' % item_person, bank_name_1)
        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_num_1.png' % item_person, bank_name_num_1)

        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_account_num_2.png' % item_person, account_num_2)
        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_full_name_2.png' % item_person, full_name_2)
        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_2.png' % item_person, bank_name_2)
        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s_bank_name_num_2.png' % item_person, bank_name_num_2)

        cv2.imwrite(r'C:\Users\admin\Desktop\TCPJW\certify_code\photos\%s.png' % item_person, ROI, )
        cv2.waitKey(0)

    else:
        account_num_1 = "无"
        full_name_1 = "无"
        account_num_2 = "无"
        full_name_2 = "无"


    print("---------------------出票人信息------------------------------------------")
    account_num_1 = pytesseract.image_to_string(account_num_1, lang='chi_sim')  #读取文字，此为默认英文
    print("账号1：%s" % account_num_1)
    full_name_1 = pytesseract.image_to_string(full_name_1, lang='chi_sim')  #读取文字，此为默认英文
    print("全称1：%s" % full_name_1)

    print("---------------------收款人信息------------------------------------------")
    account_num_2 = pytesseract.image_to_string(account_num_2, lang='chi_sim')  #读取文字，此为默认英文
    print("账号2：%s" % account_num_2)
    full_name_2 = pytesseract.image_to_string(full_name_2, lang='chi_sim')  #读取文字，此为默认英文
    print("全称2：%s" % full_name_2)

get_full_name(" https://www.tcpjw.com/Content/Images/201908141842014385955.jpg","CESHI")