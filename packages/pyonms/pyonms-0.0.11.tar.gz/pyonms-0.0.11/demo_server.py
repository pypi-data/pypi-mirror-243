# test.py
# cSpell:disable
# pylama:ignore=W0611,E501

# import json
import os

from dotenv import load_dotenv
from tqdm import tqdm

from pyonms import PyONMS
from pyonms.dao.nodes import NodeComponents

load_dotenv()


my_server = PyONMS(
    hostname=os.getenv("onms_host"),
    username=os.getenv("onms_user"),
    password=os.getenv("password"),
)
print(my_server.health.probe())
if __name__ == "__main__":
    for _ in range(25):
        alarms = my_server.alarms.get_alarms(limit=100, fiql="severity!=Cleared")
        for alarm in tqdm(alarms):
            if alarm:
                my_server.alarms.clear_alarm(id=alarm.id)
    pass
