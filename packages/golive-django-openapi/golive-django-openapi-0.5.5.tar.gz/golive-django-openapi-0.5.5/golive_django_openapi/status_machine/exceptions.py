# Author: kk.Fang(fkfkbill@gmail.com)


class StatusMachineException(Exception):
    """状态机错误"""

    pass


class NoWayTurnToTarget(StatusMachineException):
    """无法跳转到目标状态"""

    pass


