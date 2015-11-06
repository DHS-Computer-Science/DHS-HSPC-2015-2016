import re
import sys
import time
import queue
import datetime
import mysql.connector
from Grader import Grader
from ThreadGrader import ThreadGrader
from SubmissionWatcher import SubmissionWatcher
from watchdog.observers import Observer

def main(args):
  #establish compitition start time
  start_time = time.time()
  #TODO - fix this ugly mess
  end_time   = datetime.timedelta(hours=int(args.duration.partition(':')[0]),
                                  minutes=int(args.duration.partition(':')[2])).total_seconds() + start_time
  #create a queue
  q = queue.Queue()

  #connect to mysql server
  try:
    conf = {
      'user'    : args['username'],
      'password': args['password'],
      'host'    : args['host'],
      'database': args['database']
    }

    cnx = mysql.connector.connect(conf)
  except Error as e:
    print(e)
  finally:
    #close connection no matter what
    cnx.close()

  #file watcher
  observer = Observer()
  observer.schedule(SubmissionWatcher(), path=args['submission_dir'])
  observer.start()

  #grader manager
  grade_manager = ThreadGrader(q, cnx,
                               arg['table'],
                               args['problems'])
  grade_manager.setDaemon(True) #do not exit until all things needed
  grade_manager.start()         #  to be graded are graded, and start it

  #wait until end of compitition
  while time.time() <= end_time + 50: #give 50 second leeway
    #TODO - get input here, so that it was possible to add time
    time.sleep(1)

  #end watchdog
  observer.stop()
  observer.join()
