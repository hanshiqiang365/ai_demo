#author: hanshiqiang365 （微信公众号：韩思工作室）

import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image,ImageFont,ImageDraw
import time
import random

# 部分弹幕内容示例
barrages_all = [
    ('哈哈哈哈哈哈哈。萌翻了！', 1),
    ('秀', 2),
    ('小朋友们的演技都逆天了！！哭戏都演的超好啊！', 3),
    ('5189条.....', 12),
    ('真棒！', 5),
    ('每日三刷', 1),
    ('倾情演出', 7),
    ('《小戏骨》是湖南电视剧频道的一个“小孩学大剧”的综艺节目', 9),
    ('666', 4),
    ('与君初相识，犹如故人归。', 4),
    ('弹幕被清了好多', 21),
    ('翻拍经典的片子', 2),
    ('知心二叔么么哒', 17),
    ('哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈', 5),
    ('我没有', 12),
    ('38', 9),
    ('一股清流', 15),
    ('还是小白蛇好看、', 27),
    ('我是来看小白蛇的', 5),
    ('一星的制作，四星的表演', 2),
    ('似水年华', 49),
    ('回不去了', 60),
    ('法海，你不懂爱', 106),
    ('暂停成功', 218),
    ('开头见', 223),
    ('与君初相识，犹如故人归', 17),
    ('抱走猫酱', 92),
    ('突然害怕', 197),
    ('二十年生死两茫茫', 215),
    ('没弹幕', 18),
    ('白衣服的是我的，，', 155),
    ('这个我还是喜欢白衣服的，，', 117),
    ('白衣服是我的!', 177),
    ('娃娃神剧', 210),
    ('戏足自珠玑，情真催泪下', 40),
    ('美人如玉剑如虹', 173),
]

barrages_all.sort(key=lambda x:x[1])
colors = ['#600', '#060', '#006', '#066', '#606', '#660', '#666']

def get_fore(img):
    shape = img.shape[:]
    img = cv2.resize(frame,(int(img.shape[1] / 8), int(img.shape[0] / 8)), interpolation=cv2.INTER_CUBIC)
    mask = np.zeros(img.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect = (10, 10, img.shape[1]-10, img.shape[0]-10)
    try:
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    except:
        pass
    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    mask = cv2.resize(mask,(shape[1], shape[0]))
    return mask


cv2.namedWindow('AI Barrage - developed by hanshiqiang365', cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture('resources/babywhitesnake.mp4')

t = 0
ticks = 0
mask_history = []
barrages = barrages_all[:]
barrages_active = []

font = ImageFont.truetype('zhaozi.ttf', 18)

while cv2.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv2.waitKey()
        break
    mask = get_fore(frame)
    
    mask_count = np.count_nonzero(mask)
    if len(mask_history) > 0:
        avg_mask = sum(mask_history) / len(mask_history)
        mask_ratio = mask_count / avg_mask
        if mask_ratio < 0.5 or mask_ratio > 1.5:
            mask = lask_mask
        else:
            lask_mask = mask
    else:
        lask_mask = mask
    mask_history.append(mask_count)
    if len(mask_history) > 20:
        mask_history.pop(0)
    
    ticks += 1
    
    if len(barrages) > 0 and barrages[0][1] * 20 < ticks:
        b = {
            'text': barrages.pop(0)[0],
            'height': int(random.random() * frame.shape[0]),
            'width': frame.shape[1],
            'color': random.choice(colors)
        }
        barrages_active.append(b)
        
    im = Image.fromarray(frame)
    draw = ImageDraw.Draw(im)
    for b in barrages_active:
        draw.text((b['width'], b['height']), b['text'], b['color'], font=font)
        b['width'] -= 5

    if len(barrages_active) > 0 and barrages_active[0]['width'] < -400:
        barrages_active.pop(0)
    frame_with_text = np.array(im)

    img = frame_with_text * (1-mask)[:,:,np.newaxis] + frame * mask[:,:,np.newaxis]
    cv2.imshow('AI Barrage - developed by hanshiqiang365', img)

    t2 = cv2.getTickCount()
    elapsed = ((t2 - t) / cv2.getTickFrequency())
    rest = max(0.075 - elapsed, 0)

    time.sleep(rest)
    t = cv2.getTickCount()
