import uuid
from .Task import Task
import sys
sys.path.append('..')
from utils.Utils import *

class Query(object):
    status_arr = ['None', 'Sent', 'Done', 'Error']
    
    # Generates ID automatically
    def __init__(self, client, json_str, stream=None):
        self._id = str(uuid.uuid4())
        self._client = client
        self._json_str = json_str
        self._stream = stream
        self._status = 'None'

        # For counting the tasks generated by this query
        self._generated_task_ids = []
        self._payload = []

        # An array of tasks under this query
        self._tasks = []

    def add_task_id(self, task_id):
        self._generated_task_ids.append(task_id)

    def remove_task_id(self, task_id):
        self._generated_task_ids.remove(task_id)

    def add_task(self, task):
        self._tasks.append(task)

    def remove_task(self, task):
        self._tasks.remove(task)

    def task_id_count(self):
        return len(self._generated_task_ids)

    def update_status(self, new_status):
        self._status = Query.status_arr[new_status]

    def are_tasks_done(self):
        done = 0
        for task in self._tasks:
            if task._status == Query.status_arr[2]:
                done += 1
        
        if done == len(self._tasks):
            return True
        return False

    def send_response(self, response):
        print("Sending response:{}".format(response))
        self._stream.send_multipart([encode(self._client), encode(response)])

    def __str__(self):
        # return str(self._generated_task_ids)
        task_ids = ''
        # task_ids += ["{}:{}\n".format(i, t) for i, t in enumerate(self._generated_task_ids)]
        for i, t in enumerate(self._generated_task_ids):
            task_ids += "\t{}:{}\n".format(i + 1, t)
        return "Q_id: {} \n{}".format(self._id, task_ids)