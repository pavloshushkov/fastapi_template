from fastapi import BackgroundTasks


class Logging:
    def __init__(self, background_task: BackgroundTasks):
        # https://fastapi.tiangolo.com/tutorial/background-tasks/#using-backgroundtasks
        # background_task.add_task(self._send_log)
        pass

    async def _send_log(self):
        pass
