# Author: kk.Fang(fkfkbill@gmail.com)

__all__ = [
    "StatusMachineMeta",
    "StatusMachine",
]

from copy import deepcopy
from enum import StrEnum, Enum
from typing import Any, Type

from .base import *
from .exceptions import *
from ..utils.logger_utils import *


# 全部带有flag的状态机
EXPORTED_STATUS_MACHINES: dict[str, Type["StatusMachine"]] = {}

# 缓存生成的状态机pydantic模型
STATUS_MACHINE_ENUM_MODELS: dict[str, Type[Enum]] = {}


class StatusMachineMeta(LoggerMixin):

    def __repr__(cls):
        return f"<{cls.__name__}>"

    def __init__(cls, name, bases, attrs: dict):

        # 收集到的状态变更trigger
        cls.STATUS_TRIGGERS = {}

        origin_smv_dict = {k: v for k, v in attrs.items() if isinstance(v, StatusMachineValue)}
        # 存放的是原始选项定义的深拷贝
        cls._origin_smv_when_initializing = deepcopy(origin_smv_dict)

        # 请注意，origin_smv_dict引用的是代码中定义好的状态机选项。
        # 这些选项的对象可能会在代码的其他位置引用，因此这些对象倾向于使用原始的对象去创建，
        # 但是具体的next_status和value字段会在cls._check_next_status中进行验证和校正
        # cls._origin_smv_when_initializing中存放的是原始选项定义的深拷贝，
        # 这些深拷贝会在程序运行的时候用以重新生成状态机选项（附带额外的运行时定义字段）

        # 输出默认选项的状态机核
        # 状态机核是实际分析状态机选项以及其间先后关系的对象，该对象可以在实际使用中重新生成
        cls._kernel = BaseStatusMachineKernel(origin_smv_dict=origin_smv_dict)

        cls._check_export_flag()

        super().__init__(name, bases, attrs)

    def __iter__(cls):
        """用于适配django.model.field.choices"""
        yield from cls.all_items()


def status_convert_value(original_status, target_status):
    if isinstance(original_status, (str, type(None))):
        original_value = original_status
    elif isinstance(original_status, StatusMachineValue):
        original_value = original_status.value
    else:
        assert 0
    if isinstance(target_status, str):
        target_value = target_status
    elif isinstance(target_status, StatusMachineValue):
        target_value = target_status.value
    else:
        assert 0
    return original_value, target_value


class StatusMachine(metaclass=StatusMachineMeta):

    # 导出用的唯一标识
    # 状态机导出后，可被用于输出文档，重载等。
    # 如果不配置此参数，即不会输出到接口
    EXPORT_FLAG: str | None = None

    # 可扩展状态机的关键词标签，用于归类
    TAGS: str | tuple[str, ...] | None = None

    @classmethod
    def _check_export_flag(cls):
        """
        判断是否需要导出状态机。
        导出状态机需要指定一个全局唯一的状态机标识，如有冲突则失败
        """
        if cls.EXPORT_FLAG:
            assert cls.EXPORT_FLAG not in EXPORTED_STATUS_MACHINES.keys(), \
                f"duplicated exported StatusMachine with {cls.EXPORT_FLAG=} in {cls}"
            EXPORTED_STATUS_MACHINES[cls.EXPORT_FLAG] = cls

    # 下面三个核心字段，支持重载已封装其他状态机可用值的逻辑
    # TODO 除了下面三个字段内部，请勿直接使用cls._kernel对象。
    #      cls._kernel对象是一次分析枚举的结果，但是为了让字段可以灵活变更，该对象可能在运行过程中多次变化
    @classmethod
    @property
    def ALL_STATUS_DICT(cls) -> dict:
        return cls._kernel.ALL_STATUS_DICT

    @classmethod
    @property
    def ENTRIES_DICT(cls) -> dict:
        return cls._kernel.ENTRIES_DICT

    @classmethod
    @property
    def EXIT_DICT(cls) -> dict:
        return cls._kernel.EXIT_DICT

    @classmethod
    @property
    def enums_for_help_text(cls) -> str:
        """用于输出到字段备注的枚举信息"""
        return str(cls.all_items())

    @classmethod
    def build_char_field(cls, **kwargs):
        """
        生成一个Django.CharField字段
        """
        from django.db.models import CharField
        kwargs["help_text"] = f"{cls.__doc__} 枚举:{cls.enums_for_help_text}"
        kwargs["choices"] = cls
        return CharField(**kwargs)

    @classmethod
    def build_int_field(cls, **kwargs):
        """
        生成一个Django.IntegerField字段
        """
        from django.db.models import IntegerField
        kwargs["help_text"] = f"{cls.__doc__} 枚举:{cls.enums_for_help_text}"
        kwargs["choices"] = cls
        return IntegerField(**kwargs)

    @classmethod
    def all(cls) -> tuple[StatusMachineValue, ...]:
        return tuple(cls.ALL_STATUS_DICT.values())

    @classmethod
    def all_items(cls) -> tuple[tuple[Any, str], ...]:
        return tuple([(smv.value, smv.name) for smv in cls.all()])

    @classmethod
    def all_values(cls) -> tuple[str, ...]:
        return tuple(cls.ALL_STATUS_DICT.keys())

    @classmethod
    def entries(cls) -> tuple[StatusMachineValue, ...]:
        return tuple(cls.ENTRIES_DICT.values())

    @classmethod
    def entries_values(cls) -> tuple[str, ...]:
        return tuple(cls.ENTRIES_DICT.keys())

    @classmethod
    def enum(cls):
        """返回当前status_machine的enum"""
        n = f"{cls.__name__}__StrEnum"
        m = STATUS_MACHINE_ENUM_MODELS.get(n, None)
        if not m:
            m = StrEnum(n, {i: i for i in cls.all_values()})
            m.__doc__ = cls.__doc__
            STATUS_MACHINE_ENUM_MODELS[n] = m
        return m

    @classmethod
    def get(cls, v: str | StatusMachineValue | None) -> StatusMachineValue | None:
        if isinstance(v, StatusMachineValue):
            return v
        r = cls.ALL_STATUS_DICT.get(v, None)
        if not r:
            raise NameError(f"invalid status machine item {cls}: {v}, "
                            f"this may be out-dated data and need to be migrated(or deleted).")
        return r

    @classmethod
    def get_by_name(cls, name: str):
        reversed_dict = {smv.name: smv for smv in cls.ALL_STATUS_DICT.values()}
        return reversed_dict.get(name, None)

    @classmethod
    def turn(cls,
             original_status: str | StatusMachineValue | None,
             target_status: str | StatusMachineValue, **kwargs) -> str | None:
        """
        操作状态变更
        :param original_status:
        :param target_status:
        :return: 如果状态变更允许，则返回target_status的状态值（str），如果不允许直接抛出异常
        """
        original_status = cls.get(original_status)
        target_status = cls.get(target_status)
        st = status_convert_value(original_status, target_status)
        if original_status and target_status not in cls.get(original_status).next_status:
            raise NoWayTurnToTarget(f"{cls} - {original_status} to {target_status}")
        else:
            cb = cls.STATUS_TRIGGERS.get(st, None)
            if cb:
                cls.logger.info(f"{cls} - {original_status} to {target_status}: {cb}")
                cb(**kwargs)
            else:
                cls.logger.info(f"{cls} - {original_status} to {target_status}: no triggers")
            return target_status.value

    @classmethod
    def as_trigger(
            cls,
            original_status: StatusMachineValue | None,
            target_status: StatusMachineValue):
        """修改状态的时候触发"""

        def outer(func):

            cls.STATUS_TRIGGERS[(getattr(original_status, "value", None), target_status.value)] = func
            return func
        return outer

    @classmethod
    def ensure_get_to_dict(cls, v, *args, **kwargs) -> dict:
        """
        执行cls.get并.to_dict，输出一个字典，如果对象不存在，则输出空字典
        :param v:
        :param args:
        :param kwargs:
        :return:
        """
        obj = cls.get(v)
        if not obj:
            return {}
        return obj.to_dict(*args, **kwargs)

    # 下述方法用于适配pydantic-v1
    def __init__(self, v):
        self.v = v

    @classmethod
    def all_items_openapi(cls) -> str:
        r = [f"{v}:{l}" for v, l in cls.all_items()]
        return ", ".join(r)

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(
            type="string",
            format=cls.all_items_openapi(),
            description=cls.__doc__,
            enum=cls.all_values()
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        assert v in cls.all_values(), f"{v} is not a status of {cls}, choices are: {cls.all_values()}"
        return v
