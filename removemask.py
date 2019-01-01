# -*- coding: utf8 -*-

__author__ = 'imagine'

import cv2
import numpy
import os
import traceback
import logging
from PIL import Image
from removewatermask.utils import verify_img_size
from concurrent.futures import ThreadPoolExecutor
BASE_DIR = os.path.dirname(__file__)
log = logging.getLogger(__name__)


def remove_mask(img_file, new_img_file):
    mask_file1 = os.path.join(BASE_DIR + "/mask_image_file/mask.png")
    mask_file2 = os.path.join(BASE_DIR + "/mask_image_file/mask2.png")
    n = 1
    print(11111111111111111111111111111)
    for val in os.listdir(img_file):
        try:
            img_size = Image.open(img_file+"/"+val).size
            if img_size in verify_img_size.keys():
                mask_file1 = os.path.join(BASE_DIR+"/mask_image_file/"+verify_img_size.get(img_size)[0])
                mask_file2 = os.path.join(BASE_DIR+"/mask_image_file/"+verify_img_size.get(img_size)[1])
            print(1111111111111111111111111111111111111111111111111111111)
            RemoveWaterMask(img_file+"/"+val, val, mask_file1, mask_file2, new_img_file)._load_img_file()
            print(11111111111111111)
            log.info("成功!!!!!    {}".format(n))
        except Exception as ex:
            print(1111111111111111111111111111111111111111111111111)
            with open(new_img_file+"/"+"error.text", 'a') as fx:
                fx.write("error_type: {0} \nerror_msg: {1} img_file_name: {2} \n\n\n".
                         format(type(ex).__name__, traceback.format_exc(), val))
            log.info("异常!!!!!    {}".format(n))
            n += 1
            continue
        n += 1


def threading_remove_mask(img_file, new_img_file):
    """
    @调用线程池处理数据, 水印背景图分发
    :param img_file: 原始图像数据路径
    :param new_img_file: 原始图像数据名称
    :return: 处理后的图像数据保存文件夹
    """
    # threading_pools = ThreadPoolExecutor(max_workers=6)
    # threading_pools.map(remove_mask(img_file, new_img_file))
    print(1111111)
    remove_mask(img_file, new_img_file)


class RemoveWaterMask(object):
    """去除水印"""
    def __init__(self, img_file, img_name, mask_1_file, mask_2_file, new_img_file):
        if not all([img_file, mask_1_file, mask_2_file, new_img_file, img_name]):
            raise StopIteration('data type error')
        self.img_file = img_file
        self.mask_1_file = mask_1_file
        self.mask_2_file = mask_2_file
        self.new_img_file = new_img_file
        self.img_name = img_name

    def _load_img_file(self):
        """
        @加载原始图片
        :return: ps取反清洗原始图片获得的对象
        """
        try:
            old_img = cv2.imread(self.img_file)
            mask_1_img = cv2.imread(self.mask_1_file)
        except Exception as ex:
            raise StopIteration('your img file not found img, errror detauls: {}'.format(ex))
        return self._remove_water_mask_for_img(old_img, mask_1_img)

    def _remove_water_mask_for_img(self, img, mask_img):
        """
        @清洗原始图片
        :param img: 原始图像数据
        :param mask_img: 水印图
        :return:
        """
        save = numpy.zeros(img.shape, numpy.uint8)
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                for channel in range(img.shape[2]):
                    if mask_img[row, col, channel] == 0:
                        val = 0
                    else:
                        reverse_val = 260 - img[row, col, channel]
                        val = 260 - reverse_val * 261 / mask_img[row, col, channel]
                        if val < 0:
                            val = 0
                    save[row, col, channel] = val
        cv2.imwrite(self.new_img_file+"/"+self.img_name, save)
        return self._inpaint_water_mask_for_img(self.new_img_file+"/"+self.img_name)

    def _inpaint_water_mask_for_img(self, img):
        """
        @对原始图片进行灰度处理
        :param img: 处理过的图像数据
        :return:
        """
        src = cv2.imread(img)
        mask = cv2.imread(self.mask_2_file, cv2.IMREAD_GRAYSCALE)
        dst = cv2.inpaint(src, mask, 3, cv2.INPAINT_TELEA)
        cv2.imwrite(self.new_img_file+"/"+self.img_name, dst)
        return self.new_img_file
