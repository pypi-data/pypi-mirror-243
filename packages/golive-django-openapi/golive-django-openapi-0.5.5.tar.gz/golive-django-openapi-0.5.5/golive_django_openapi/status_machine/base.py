# Author: kk.Fang(fkfkbill@gmail.com)

__all__ = [
    "StatusMachineValue",
    "SMV",
    "BaseStatusMachineKernel",
]

from collections import defaultdict
from typing import Union, Any

from ..utils.pydantic_utils import JSONSerializablePDM


class StatusMachineValue:

    def __init__(self,
                 name: str,
                 value=None,
                 next_status: Union[str, int, "StatusMachineValue", tuple, None] = (),
                 extra: dict | list | tuple | JSONSerializablePDM | None = None,
                 **kwargs):
        """
        :param name: 展示名
        :param value: 实际值。缺省使用当前状态机被赋值的引用名
        :param next_status: 直接下一步状态
        :param extra: 额外信息，可用于扩展逻辑。
        :param kwargs:
        """
        self.value = value
        self.name = name
        self.next_status: tuple["StatusMachineValue", ...] = next_status
        self.extra = extra

    @property
    def next_status_values(self) -> list:
        """next_status字段的文本值"""

        r = []

        def deal_with_single_value(v):
            if isinstance(i, (str, int)):
                r.append(i)
            elif isinstance(i, StatusMachineValue):
                r.append(i.value)
            else:
                assert 0, f"bad next status of {i}"

        for i in self.next_status:
            if isinstance(i, (tuple, list)):
                for j in i:
                    deal_with_single_value(j)
            else:
                deal_with_single_value(i)
        return r

    def to_dict(self, v: str = "value", n: str = "name", exclude_extra: bool = False) -> dict:
        """
        :param v:
        :param n:
        :param exclude_extra: 排除extra字段
        """
        exported_extra = self.extra
        if isinstance(exported_extra, JSONSerializablePDM):
            exported_extra = exported_extra.json_dict()
        r = {
            v: self.value,
            n: self.name,
            "next_status": self.next_status_values
        }
        if not exclude_extra:
            r["extra"] = exported_extra
        return r

    def __str__(self):
        return f"<StatusMachineValue - {self.value}: {self.name}>"


SMV = StatusMachineValue


class BaseStatusMachineKernel:

    # 允许的值的类型
    SUPPORTED_VALUE_TYPES: tuple = (str, int)

    def _referring_as(self, v, n: int):
        """引用次数为"""
        self._status_referred_time[v][1] = n

    def _referred_up(self, v):
        """被引用次数加1"""
        self._status_referred_time[v][0] += 1

    def _check_next_status(self, a_list: dict[Any, StatusMachineValue]):
        """
        检查/归档下层依赖
        """
        for smv in a_list.values():
            if smv.next_status is None:
                self._referring_as(smv.value, 0)
                smv.next_status = ()
            elif isinstance(smv.next_status, StatusMachineValue):
                self._referred_up(smv.next_status.value)
                self._referring_as(smv.value, 1)
                smv.next_status = (smv.next_status,)
            elif isinstance(smv.next_status, self.SUPPORTED_VALUE_TYPES):
                smv.next_status = (a_list[smv.next_status],)
                self._referred_up(smv.next_status[0].value)
                self._referring_as(smv.value, 1)
            elif isinstance(smv.next_status, (tuple, list)):
                r = []
                for i in smv.next_status:
                    if isinstance(i, self.SUPPORTED_VALUE_TYPES):
                        i = a_list[i]
                    elif isinstance(i, StatusMachineValue):
                        pass
                    else:
                        assert 0, f"bad type in {smv.next_status=}: {i}"
                    r.append(i)
                    self._referred_up(i.value)
                self._referring_as(smv.value, len(r))
                smv.next_status = tuple(r)
            else:
                assert 0, f"unsupported value type {type(smv)}"

    @classmethod
    def build_all_status_dict(cls, d: dict):
        r = {}
        for defined_value, smv in d.items():
            assert isinstance(smv, StatusMachineValue), \
                f"{smv} is not an instance of StatusMachineValue or its subclass."
            if smv.value is None:
                # 给smv配置默认的值
                smv.value = defined_value
            r[smv.value] = smv
        return r

    def __init__(self, origin_smv_dict: dict[Any, StatusMachineValue]):

        # 全部的smv dict
        self.ALL_STATUS_DICT: dict[Any, StatusMachineValue] = {}

        # 入口dict
        self.ENTRIES_DICT: dict[Any, StatusMachineValue] = {}

        # 出口dict
        self.EXIT_DICT: dict[Any, StatusMachineValue] = {}

        # 每个smv的：[被引用次数，引用别的的次数]
        # TODO 请注意被引用是可以循环的，因此这个数字只统计至少被引用的次数。
        #      统计这个数字的意义是找出谁是头谁是尾
        self._status_referred_time = defaultdict(lambda: [0, 0])

        self.ALL_STATUS_DICT = self.build_all_status_dict(origin_smv_dict)

        self._check_next_status(self.ALL_STATUS_DICT)

        for value, flag in self._status_referred_time.items():
            if flag[0] == 0:
                self.ENTRIES_DICT[value] = self.ALL_STATUS_DICT[value]
            if flag[1] == 0:
                self.EXIT_DICT[value] = self.ALL_STATUS_DICT[value]
