# Author: kk.Fang(fkfkbill@gmail.com)

from golive_django_openapi.status_machine import *


class sm(StatusMachine):
    """ccc"""

    EXPORT_FLAG = "asasa"
    TAGS = "cs-tag"

    a = SMV("name-a", next_status=2)
    b = SMV("name-b", value=2, next_status="a")


print(StatusMachineDocBuilder(sm).build_markdown())

