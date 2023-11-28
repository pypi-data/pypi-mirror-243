import os
import sys
from typing import Optional

from plumbum import local
from pyarrow.fs import HadoopFileSystem

from .user import current_user


def _maybe_set_hadoop_classpath() -> None:
    """from https://github.com/apache/arrow/blob/master/python/pyarrow/hdfs.py"""
    import re

    if re.search(r"hadoop-common[^/]+.jar", os.environ.get("CLASSPATH", "")):
        return

    if "HADOOP_HOME" in os.environ:
        if sys.platform != "win32":
            classpath = _derive_hadoop_classpath(os.environ["HADOOP_HOME"])
        else:
            hadoop_bin = "{}/bin/hadoop".format(os.environ["HADOOP_HOME"])
            classpath = _hadoop_classpath_glob(hadoop_bin)
    else:
        classpath = _hadoop_classpath_glob("hadoop")

    os.environ["CLASSPATH"] = classpath


def _derive_hadoop_classpath(hadoop_home: str) -> str:

    find = local["find"]
    find_jars = find["-L", hadoop_home, "-name", "hadoop-*.jar"]
    xargs = local["xargs"]
    jars = find_jars | xargs["echo"]
    jars = jars.replace(" ", ":")
    jars = jars.rstrip("\n")

    hadoop_conf = (
        os.environ["HADOOP_CONF_DIR"]
        if "HADOOP_CONF_DIR" in os.environ
        else "/etc/hadoop/conf"
    )

    return str((hadoop_conf + ":").encode("utf-8") + jars.encode("utf-8"))


def _hadoop_classpath_glob(hadoop_bin: str) -> str:
    hadoop = local[hadoop_bin]
    hadoop_classpath = hadoop["classpath", "--glob"]
    return str(hadoop_classpath())


class HDFS:
    def __init__(
        self,
        hdfs_host: str = "default",
        hdfs_port: int = 8020,
        hdfs_user: Optional[str] = None,
    ):
        self.hdfs_host = hdfs_host
        self.hdfs_port = hdfs_port
        self.hdfs_user = current_user() if hdfs_user is None else hdfs_user
        _maybe_set_hadoop_classpath()
        self.hdfs_fs = HadoopFileSystem(hdfs_host, hdfs_port, hdfs_user)

    def _setup_env(self) -> None:
        import os

        if "CLASSPATH" in os.environ:
            return

    def _check_config(self) -> None:
        if self.hdfs_host is None or self.hdfs_port is None or self.hdfs_user is None:
            raise Exception("HDFS configuration is not set")
