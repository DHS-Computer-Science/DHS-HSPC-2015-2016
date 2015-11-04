import time
import queue
import datetime
from Grader import Grader
from ThreadGrader import ThreadGrader
from SubmissionWatcher import SubmissionWatcher
from watchdog.observers import Observer
import mysql.connector

def main(args):
  #establish compitition start time
  start_time = time.time()
  end_time   = datetime.timedelta(hours=int(args.duration.partition(':')[0]),
                                  minutes=int(args.duration.partition(':')[2])).total_seconds() + start_time
  #create a queue
  q = queue.Queue()
  
  #connect to mysql server
  try:
    cnx = mysql.connector.connect(user=args.username, password=args.password,
                                  host=args.host,
                                  database=args.database)
  except Error as e:
    print(e)
  finally:
    #close connection no matter what
    cnx.close()
  
  #file watcher
  observer = Observer()
  observer.schedule(SubmissionWatcher(), path=args.submission_dir)
  observer.start()
  
  #grader manager
  grade_manager = ThreadGrader(q) #create
  grade_manager.setDaemon(True)   #do not exit until all things needed to be graded are graded
  grade_manager.start()
  
  #wait until end of compitition
  while time.time() <= end_time + 50: #give 50 second leeway
    time.sleep(1)
  
  #end watchdog
  observer.stop()
  observer.join()
