import os

from typing import Any, Optional


class PathConfig:
    __instance__: Any
    # 日志文件目录
    log_url: str
    # 数据文件目录
    data_url: Optional[str]
    # 输出文件目录
    output_url: Optional[str]
    # 测试文件目录
    test_url: Optional[str]
    # 临时文件目录
    tmp_url: Optional[str]

    @classmethod
    def load(
            cls, base_url: str, log_url: str,
            data_url: Optional[str] = None,
            output_url: Optional[str] = None,
            test_url: Optional[str] = None,
            tmp_url: Optional[str] = None,
    ):
        cls.log_url = os.path.join(base_url, log_url)
        if data_url: cls.data_url = os.path.join(base_url, data_url)
        if output_url: cls.output_url = os.path.join(base_url, output_url)
        if test_url: cls.test_url = os.path.join(base_url, test_url)
        if tmp_url: cls.tmp_url = os.path.join(base_url, tmp_url)
