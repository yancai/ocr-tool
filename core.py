#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64
import logging
from os import path

import requests

from settings import AK, SK

_logger = None
_access_token = None


def get_logger(name="root"):
    """获取日志

    :return:
    """
    global _logger
    if _logger is not None:
        return _logger
    else:
        _logger = logging.getLogger()

        formatter = logging.Formatter(
            '%(asctime)s %(name)s %(filename)s:%(lineno)d [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        channel = logging.StreamHandler()
        channel.setFormatter(formatter)
        _logger.addHandler(channel)
        _logger.setLevel(logging.INFO)
        return _logger


def get_access_token():
    """从百度获取access_token

    :return:
    """
    global _access_token
    if _access_token is not None:
        return _access_token
    else:
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'.format(
            ak=AK,
            sk=SK
        )
        response = requests.get(host)
        if response:
            _access_token = response.json().get("access_token")
            return _access_token


def general_ocr(filepath):
    """通用文字识别

    对指定的图片文件使用百度通用文字识别接口进行OCR识别，文本输出到.txt文件中
    :return:
    """
    logger = get_logger()

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(filepath, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_access_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        data = response.json()
        if "error_msg" in data:
            logger.error("convert file: {} failed! error_msg: {}".format(
                filepath, data.get("error_msg")
            ))
            return
        words = [i["words"] for i in response.json().get("words_result")]
        name = path.basename(filepath) + ".txt"
        output_dir = path.dirname(filepath)
        output_filename = path.join(output_dir, name)
        with open(output_filename, "w", encoding="utf-8") as f:
            for line in words:
                f.write(line)
                f.write("\n")

            logger.info("convert {} to {}".format(filepath, output_filename))


if __name__ == "__main__":
    pass
