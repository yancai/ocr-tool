# OCR工具介绍

此工具为使用[通用文字识别](https://ai.baidu.com/tech/ocr/general)接口实现的文字识别工具。

## 使用方法

使用`start.bat`或`start.sh`启动服务

或

使用以下方式启动服务

```shell script
pipenv run python ocr.py server
```

启动服务后，将图片（支持jpg/jpeg/png/bmp格式）放在`INPUT_DIR`（`settings.py`中配置）目录中，服务会自动对图片做文本识别，并输出到文本文件中。


启动参数中不带`server`参数时，工具会对`INPUT_DIR`目录中的图片全部做文本识别并输出到文本文件中。
