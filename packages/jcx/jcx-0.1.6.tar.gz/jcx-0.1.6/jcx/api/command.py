from dataclasses import dataclass
from pathlib import Path
from subprocess import getstatusoutput

from flask_restx import Api, fields  # type: ignore
from jcx.api.dao_item import ItemDao, add_item_resource
from jcx.time.dt import now_iso_str
from rustshed import Option, Null


@dataclass
class CommandInfo:
    """命令信息"""
    time: str = ''
    """时间"""
    output: str = ''
    """命令输出"""


class CommandDao(ItemDao):
    """数据源组数据访问对象"""

    def __init__(self, folder: Path, name: str, command: str):
        super().__init__(CommandInfo, folder, name)
        self._command = command

    def before_update(self, r: CommandInfo, _r0: CommandInfo):
        """更新之前"""
        r.time = now_iso_str()
        status, output = getstatusoutput(self._command)
        r.output = '%s, %s' % (status, output)
        return r


def command_model(api: Api, description):
    return api.model('Command', {
        'time': fields.String(description='命令执行结束时间，PUT时忽略'),
        'output': fields.String(description=description),
    })


@dataclass
class CommandParam:
    """命令参数"""

    time: str = ''
    """时间"""
    output: str = ''
    """输出?"""


def add_command_resource(api, ns, url, db_root: Path, cmd: str, desc: str, name: Option[str] = Null) -> None:
    """添加命令资源"""
    name1 = name.unwrap_or(Path(url).name)
    dao = CommandDao(db_root, name1, cmd)
    add_item_resource(ns, url, dao, command_model(api, desc))
