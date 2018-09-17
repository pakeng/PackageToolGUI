# -*- coding:UTF-8 -*-
import threading

from enum import Enum


class MachineState(Enum):
    NONE = 0  # 起始状态
    DECOMPILE = 1  # 正在解包
    COMPILE = 2  # 正在重打包
    WAITE = 3  # 等待中


# 状态机用来记录工具当前状态，因为设计到异步操作所以状态对工具整个运行流程具有重要意义。
class StateMachine(object):
    _instance_lock = threading.Lock()

    #  单例实现方式
    def __new__(cls, *args, **kwargs):
        if not hasattr(StateMachine, "_instance"):
            with StateMachine._instance_lock:
                if not hasattr(StateMachine, "_instance"):
                    StateMachine._instance = object.__new__(cls)
                    StateMachine._instance._state = MachineState.NONE
        return StateMachine._instance

    def __init__(self):
        pass

    def check(self, state):
        return state == self._instance._state

    def get_state(self):
        return self._instance._state

    def set_state(self, state):
        if state in MachineState:
            self._instance._state = state
        else:
            raise Exception("error unknown state")


# 测试方法
def test():
    machine = StateMachine()
    machine1 = StateMachine()
    StateMachine().get_state()
    if machine1.get_state() == MachineState.NONE:
        print 'Success'
        machine.set_state(MachineState.DECOMPILE)
    machine2 = StateMachine()
    if machine2.get_state() == MachineState.DECOMPILE:
        print "Success"
    print StateMachine().check(MachineState.DECOMPILE)
    # machine.set_state("UnknownState")


# 测试方法
if __name__ == '__main__':
    test()

