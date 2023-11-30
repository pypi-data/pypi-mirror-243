# Author: kk.Fang(fkfkbill@gmail.com)

__all__ = [
    "StatusMachineDocBuilder",
    "StatusMachineAPIBuilder",
]

from os import linesep
from typing import Type

from .status_machine import *


class StatusMachineDocBuilder:
    """状态机文档输出"""

    def __init__(self, sm: Type[StatusMachine]):
        assert sm.EXPORT_FLAG, f"using doc builder, the export_flag of the target StatusMachine is required."
        self.sm = sm

    def build_markdown(self) -> str:
        """输出markdown文档"""
        tags = ""
        if self.sm.TAGS:
            tags = f"* 关键词: {self.sm.TAGS}"
        doc = self.sm.__doc__
        if "\n" in doc:
            doc = "\n".join(["```", doc, "```"])
        else:
            doc = f"* {doc}"
        title = f"""
## {self.sm.EXPORT_FLAG}

{tags}

{doc}
"""
        content = [
            "|展示标签|值|值类型|下一步值|",
            "|----|----|----|----|",
        ]
        for v, smv in self.sm.ALL_STATUS_DICT.items():
            content.append(f"|{smv.name}|{smv.value}|{type(smv.value).__name__}|{smv.next_status_values}|")
        return linesep.join([title, linesep.join(content)])


class StatusMachineAPIBuilder:
    """全部状态机的接口输出列表"""

    def __init__(self, sms: dict[str, StatusMachine], exclude_extra: bool = False):
        self.sms = sms
        self.exclude_extra = exclude_extra

    @staticmethod
    def _build_tags_list(sm: StatusMachine) -> list[str]:
        tags = []
        if isinstance(sm.TAGS, str):
            tags = [sm.TAGS]
        elif isinstance(sm.TAGS, (list, tuple)):
            for i in sm.TAGS:
                if isinstance(i, str):
                    tags.append(i)
        else:
            assert 0, f"TAGS containing invalid content: {sm.TAGS=}"
        return tags

    def list_resp(self, export_flag: str | None = None) -> list[dict]:
        """
        接口返回信息
        :param export_flag: 仅返回指定状态机
        """
        r = []
        for sm in self.sms.values():
            if export_flag is not None and sm.EXPORT_FLAG != export_flag:
                continue
            r.append({
                "export_flag": sm.EXPORT_FLAG,
                "docstring": sm.__doc__,
                "smvs": [smv.to_dict(exclude_extra=self.exclude_extra) for smv in sm.ALL_STATUS_DICT.values()],
                "tags": self._build_tags_list(sm)
            })
        return r
