from threading import Thread, Lock as thread_lock
from queue import Queue
import csv
import time

# Source : https://medium.com/@shashwat_ds/a-tiny-multi-threaded-job-queue-in-30-lines-of-python-a344c3f3f7f0


db_lock = thread_lock()


class TaskQueue(Queue):

    threads = []

    def __init__(self, nb_workers=1):
        Queue.__init__(self)
        self.num_worker_threads = nb_workers
        self.start_workers()

    def add_task(self, task, *args, **kwargs):
        self.put((task, args, kwargs))

    def start_workers(self):
        for _ in range(self.num_worker_threads):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()
            TaskQueue.threads.append(t)

    def stop_workers(self):
        self.join()
        for i in range(self.num_worker_threads):
            self.put(None, [], {})
        for t in TaskQueue.threads:
            t.join()

    def worker(self):
        """
        Keeps getting the topmost task from the queue 
        and running it along with its arguments
        """
        while True:
            exec_task, args, kwargs = self.get()
            if exec_task is None:
                break
            else:
                exec_task(*args, **kwargs)
                self.task_done()


def insert_gtfs_feed(feed_filename, model, Session, limit=0):
    # import random

    # rand = random.randint(3,15)
    # print(feed_filename,'\t',rand, flush=True)
    # for nb in range(rand):
    #     print(feed_filename, '\t', 'PROCESS ... ', nb, flush=True)
    #     time.sleep(1)
    # print(feed_filename,'\t',rand,'\t','DONE', flush=True)
    Session(expire_on_commit=False)
    for counter, feed in enumerate(_read_gtfs_feed(feed_filename)):

        # if 'stop_times' in feed_filename:
        #     q = session.query(model).filter_by(
        #         trip_id=feed['trip_id'],
        #         stop_id=feed['stop_id'])

        #     exists = session.query(
        #         model.id).filter(q.exists()).scalar()
        #     print(exists)
        #     if not exists:
        #         gtfs_feed = model(**feed)
        #         session.add(gtfs_feed)
        #         session.commit()
        #     continue

        gtfs_feed = model(**feed)
        Session.add(gtfs_feed)

        if counter % limit == 0:
            db_lock.acquire()
            Session.commit()
            Session.close()
            db_lock.release()

    if Session.is_active:
        db_lock.acquire()
        Session.commit()
        Session.close()
        db_lock.release()

    Session.remove()


def _read_gtfs_feed(feed_file_name):
    with open(feed_file_name, "r") as gtfs_file:
        gtfs_reader = csv.reader(gtfs_file)
        head = next(gtfs_reader)

        for row in gtfs_reader:
            new_line = dict(zip(head, row))
            new_line = dict((k, v)
                            for k, v in new_line.items() if v != '')
            yield new_line
