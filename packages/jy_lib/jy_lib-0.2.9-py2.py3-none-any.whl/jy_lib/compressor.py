# -*- coding: utf-8 -*-
import brotli
import zlib
import zstandard
from enum import Enum


class Compressor(Enum):
    IDENTITY = 'identity'
    DEFLATE = 'deflate'
    GZIP = 'gzip'
    ZLIB = 'zlib'
    BR = 'br'
    ZSTD = 'zstd'

    def get_compressor(self, level: int = 1):
        """获取流式压缩对象"""
        if self == self.DEFLATE:
            return zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=-zlib.MAX_WBITS)
        elif self == self.GZIP:
            return zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS | 16)
        elif self == self.ZLIB:
            return zlib.compressobj(level=level, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS)
        elif self == self.BR:
            return brotli.Compressor()
        elif self == self.ZSTD:
            return zstandard.ZstdCompressor(level)
