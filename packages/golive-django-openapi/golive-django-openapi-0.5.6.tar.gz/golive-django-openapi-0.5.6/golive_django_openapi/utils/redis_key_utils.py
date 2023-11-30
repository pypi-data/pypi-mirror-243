# Author: kk.Fang(fkfkbill@gmail.com)

__all__ = [
    "ValuedField",
    "RedisKeyTemplate",
]

import warnings
from copy import deepcopy
from typing import Type, Union, Optional

from pydantic import Field as pdm_field, constr, validator, PrivateAttr

from .pydantic_utils import *


class RedisKeyException(Exception):
    pass


class ValuedField(DictPDM):
    """填值字段"""

    name: constr(strip_whitespace=True, min_length=1, strict=True)
    field_type: Type = str
    description: str = None
    none_placeholder: constr(strip_whitespace=True) = pdm_field(default="", description="针对None值的占位")

    @validator("name")
    def validate_name(cls, value: str):
        if not value.isidentifier():
            raise RedisKeyException(f"valued_field name should be python identifier: {value}")
        return value

    def check_seperator(self, s: str):
        if s in self.name:
            raise RedisKeyException(f"valued_field contains the seperator of the template: {s}")


class TemplateValues(DictPDM):
    """填值后的模板"""
    pass


class RedisKeyTemplate(DictPDM):
    """redis键模板"""

    _DEFAULT_SEPERATOR: str = ":"

    fields: list[ValuedField | constr(strip_whitespace=True)]
    seperator: constr(strip_whitespace=True, min_length=1, max_length=1) = _DEFAULT_SEPERATOR
    _constructed: Type[TemplateValues] | None = PrivateAttr(default=None)

    @validator("fields")
    def validate_fields(cls, values: list[str | ValuedField]):
        if not values:
            raise RedisKeyException(f"at lease one field is required")
        valued_names = set()
        for v in values:
            if isinstance(v, str):
                continue
            if v.name in valued_names:
                raise RedisKeyException(f"duplicated names from valued_field {v}: {v.name=}")
            valued_names.add(v.name)
        return values

    @classmethod
    def build(cls, s: str, seperator: str = _DEFAULT_SEPERATOR) -> "RedisKeyTemplate":
        """通过format-str文本创建模板"""
        fields = []
        for v in s.split(seperator):
            if len(v) >= 3 and v[0] == "{" and v[-1] == "}":
                fields.append(ValuedField(name=v[1: -1]))
            else:
                fields.append(v)
        return cls(
            fields=fields,
            seperator=seperator
        )

    @property
    def template_value_pdm(self) -> Type[TemplateValues]:
        if not self._constructed:
            self._constructed = TemplateValues.sub({
                vf.name: Optional[vf.field_type] for vf in self.fields if isinstance(vf, ValuedField)
            })
        return self._constructed

    def parse(self, k: str) -> TemplateValues:
        """处理一条key，获取各个valued_fields的值"""
        values = {}
        split_k = k.split(self.seperator)
        for i, f in enumerate(self.fields):
            if isinstance(f, ValuedField):
                values[f.name] = split_k[i]
                if values[f.name] == f.none_placeholder:
                    values[f.name] = None
        return self.template_value_pdm(**values)

    def generate(self, **valued_keys) -> str:
        """输出key"""
        values = self.template_value_pdm(**valued_keys).dict()
        valued_fields = {f.name: f for f in self.fields if isinstance(f, ValuedField)}
        for k, v in values.items():
            if isinstance(v, str) and self.seperator in v:
                warnings.warn(f"incoming values containing the seperator, "
                              f"so when you retrieve this key and try to parse it, strange things may happen.")
            if k in valued_fields.keys() and v is None:
                values[k] = valued_fields[k].none_placeholder
        return self.get_template_str().format(**values)

    def get_template_str(self):
        """模板的format-str文本"""
        d = []
        for i in self.fields:
            if isinstance(i, str):
                d.append(i)
            elif isinstance(i, ValuedField):
                d.append("{" + i.name + "}")
        return self.seperator.join(d)

    def _append_field(self, f: str | ValuedField):
        """动态增加field，并且执行必要的校验"""
        self.fields.append(f)
        self.validate_fields(self.fields)
        self._constructed = None

    def __str__(self):
        """只有当前模板不包含任何valued_fields的时候才允许直接str()"""
        return self.generate()

    def __add__(self, other: Union[str, ValuedField, "RedisKeyTemplate"]):
        """模板后续追加字段，请注意追加的如果是填值字段，则共享该字段对象"""
        r = deepcopy(self)
        if isinstance(other, str):
            other = other.strip()
            assert len(other)
            r._append_field(other)
        elif isinstance(other, ValuedField):
            other.check_seperator(self.seperator)
            r._append_field(other)
        elif isinstance(other, self.__class__):
            for f in other.fields:
                r += f
        else:
            raise RedisKeyException(f"invalid + usage: {type(other)=}")
        return r


def test():
    t0 = RedisKeyTemplate.build("a", seperator="-")

    t1 = RedisKeyTemplate.build("a:b:qaz")
    print(str(t1))
    print(t1.parse("a:b:qaz"))

    t2 = RedisKeyTemplate.build("a:{zz}:1:emmmm:{b}")
    print(t2.get_template_str())
    print(t2.generate(zz=1, b="hahahah"))
    print(t2.parse("a:wo-shi-zz:1:emmmm:wo-shi-b"))

    t3 = t2 + "appendix" + ValuedField(name="appended_integer_field", field_type=int)
    print(t3.get_template_str())
    print(t3.generate(zz="xixi:", b="ceshi"))
    print(t3.parse("a:{zz}:1:emmmm:{b}:appendix:"))

    t4 = t1 + t2
    print(t4.get_template_str())
