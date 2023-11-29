#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/10/27 15:57
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : artifact_api_artifact.py
# @Software: PyCharm
"""
from typing import List, Optional, Dict, Any


class ArtifactContent:
    """
    artifact content class
    """
    def __init__(self, uri: Optional[str] = "",
                 description: Optional[str] = "",
                 alias: Optional[list] = list(),
                 tags: Optional[dict] = dict(),
                 metadata: Optional = None):
        """
        init
        Args:
            uri: uri 版本文件路径
            description: 版本描述
            alias: 版本别名，如default, latest
            tags: 版本标签 [key:value]
            metadata: 版本基本信息
        """
        self.uri = uri
        self.description = description
        self.alias = alias
        self.tags = tags
        self.metadata = metadata

