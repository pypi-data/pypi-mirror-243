import hashlib
import os
import sys
import traceback
from pathlib import Path

import av


def import_class(import_str):
    mod_str, _sep, class_str = import_str.rpartition(".")
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError(
            f"Class {class_str} cannot be found ({traceback.format_exception(*sys.exc_info())})"
        )


def convert_audio(filepath, ext):
    filepath = Path(filepath)
    in_path = str(filepath)
    out_path = str(filepath.parent / f"{filepath.stem}.{ext}")

    codec = "pcm_s16le" if ext == "wav" else ext
    with av.open(in_path, "r") as in_av:
        with av.open(out_path, "w") as out_av:
            out_stream = out_av.add_stream(codec)
            for frame in in_av.decode(in_av.streams.audio[0]):
                for packet in out_stream.encode(frame):
                    out_av.mux(packet)
            for packet in out_stream.encode(None):
                out_av.mux(packet)
    return out_path


def zero_copy(in_fd, out_fd):
    ret = 0
    offset = 0
    while True:
        ret = os.sendfile(in_fd, out_fd, offset, 65536)
        offset += ret
        if ret == 0:
            break


def md5_content_hex(path):
    md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()
