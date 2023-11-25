# -*- coding: utf-8 -*-
import logging

# ====================================================================================================================
# 模块级别的日志记录器
log = logging.getLogger(__name__)


# 默认日志配置
def setup_logging(debug=False):
    log.setLevel(logging.DEBUG if debug else logging.CRITICAL)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(console_handler)


# 在初始化时进行一次日志配置
setup_logging(debug=False)
