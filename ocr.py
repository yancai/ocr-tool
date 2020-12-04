#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import time
from os import path
from os.path import realpath, join

from core import get_logger, general_ocr
from settings import INPUT_DIR, EXTS


def convert2txt(files):
    """批量将图片进行OCR转换输出到文本

    :param files:
    :return:
    """
    for f in files:
        ext = path.splitext(f)[1].lower()
        dirname = path.dirname(f)
        if ext in EXTS:
            general_ocr(path.join(dirname, f))


def main():
    logger = get_logger()
    as_server = sys.argv[-1] == "server"
    # 如果是以server方式运行，则一直监听目录，否则只对目录中的文件进行一次转换
    if as_server:

        print(
            "\033[34m"
            "Welcome to use OCR server\n"
            "Put your image(jpg/jpeg/png/bmp) into `{}`\n\033[0m".format(
                realpath(INPUT_DIR)))

        before = dict([(f, None) for f in os.listdir(INPUT_DIR)])

        try:
            # 检测目录，如果有新增的图片文件，则使用OCR接口转换成文字
            while 1:
                time.sleep(1)
                after = dict([(f, None) for f in os.listdir(INPUT_DIR)])
                added = [f for f in after if f not in before]

                # 过滤只转换特定后缀名的图片
                added_img = [f for f in added if path.splitext(f)[-1] in EXTS]
                if added_img:
                    logger.info("Added file: {}".format(", ".join(added_img)))
                    fullpaths = [realpath(join(INPUT_DIR, f)) for f in added]
                    convert2txt(fullpaths)
                before = after
        except KeyboardInterrupt as e:
            print("\033[34mbye~")
            sys.exit(0)
    else:
        files = os.listdir(INPUT_DIR)
        fullpaths = [realpath(join(INPUT_DIR, f)) for f in files]
        convert2txt(fullpaths)


if __name__ == "__main__":
    main()
    pass
