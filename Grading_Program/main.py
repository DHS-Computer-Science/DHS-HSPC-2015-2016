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

#this may not do anything
temp_dir = tempfile.mkdtemp(prefix='grader_staging_')

def cleanup():#delete the thing that may not do anything, at exit
  shutil.rmtree(temp_dir)

atexit.register(cleanup)#be 100% sure it will be deleted

def main(args):
  #create a queue for the subs to be processed
  q = queue.Queue()
  done = []#list of things graded

  #connect to mysql server - I should'a used pymysql
  conf = {
    'user'    : args['username'],
    'password': args['password'],
    'host'    : args['host'],
    'database': args['database'],
    'buffered': True
  }
  cnx = mysql.connector.connect(**conf)#magic(connecting)

  #file watcher, wait for the webserver to put subs on disk
  observer = Observer()
  observer.schedule(SubmissionWatcher(cnx, args, q, temp_dir),
                    path=args['submission_dir'])
  observer.start()

  #grader manager, when queue is not working - grades stuff
  grade_manager = ThreadGrader(q, cnx, done, args)
  grade_manager.setDaemon(True) #do not exit until all things needed
  grade_manager.start()         #  to be graded are graded; and start it

  #instatiate/start GUI - since some people find the commandline not pretty/hard
  app = App(observer, q, done, args['end_time'], grade_manager)
  app.mainloop()#start the gui

  #close mysql, when the gui exits
  cnx.close()

  #end watchdog - stop watching files appear in submission dir
  observer.stop()
  observer.join()
