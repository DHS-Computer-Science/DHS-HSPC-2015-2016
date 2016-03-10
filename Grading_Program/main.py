import re
import time
import queue
import datetime
import mysql.connector
from multiprocessing import Process
from Gui import App
from Grader import Grader
from ThreadGrader import ThreadGrader
from SubmissionWatcher import SubmissionWatcher
from watchdog.observers import Observer
import threading
import tempfile
import atexit
import shutil

temp_dir = tempfile.mkdtemp(prefix='grader_staging_')

def cleanup():
  shutil.rmtree(temp_dir)

atexit.register(cleanup)

def main(args):
  #create a queue
  q = queue.Queue()
  done = []

  #connect to mysql server
  conf = {
    'user'    : args['username'],
    'password': args['password'],
    'host'    : args['host'],
    'database': args['database'],
    'buffered': True
  }
  cnx = mysql.connector.connect(**conf)

  #file watcher
  observer = Observer()
  observer.schedule(SubmissionWatcher(cnx, args, q, temp_dir),
                    path=args['submission_dir'])
  observer.start()

  #grader manager
  grade_manager = ThreadGrader(q, cnx, done, args)
  grade_manager.setDaemon(True) #do not exit until all things needed
  grade_manager.start()         #  to be graded are graded, and start it

  #instatiate/start GUI
  app = App(observer, q, done, args['end_time'], grade_manager)
  app.mainloop()

  #close mysql
  cnx.close()

  #end watchdog - stop watching files apear in submission dir
  observer.stop()
  observer.join()
