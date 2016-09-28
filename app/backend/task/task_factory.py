import json
from app.backend.task.default_task import DefaultTask, CmdTask
from app.backend.task.roc_analysis import ROCAnalysis


class TaskFactory:
    def __init__(self): pass

    @staticmethod
    def create(type, params):
        if type == "default":
            return DefaultTask()
        elif type == "cmd":
            return CmdTask(params['command'])
        elif type == "roc-analysis":
            return ROCAnalysis(params['model_id'], params['data_set_id'])
        else:
            return NotImplemented