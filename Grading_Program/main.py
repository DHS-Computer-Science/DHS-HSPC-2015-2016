import time
import queue
import datetime
import mysql.connector
from Grader import Grader
from configparser import ConfigParser
from ThreadGrader import ThreadGrader
from SubmissionWatcher import SubmissionWatcher
from watchdog.observers import Observer

def read_db_config(filename='config.ini', section='mysql'):
  """ Read database configuration file and return a dictionary object
  :param filename: name of the configuration file
  :param section: section of database configuration
  :return: a dictionary of database parameters
  """
  # create parser and read ini configuration file
  parser = ConfigParser()
  parser.read(filename)

  # get section, default to mysql
  db = {}
  if parser.has_section(section):
    items = parser.items(section)
    for item in items:
      db[item[0]] = item[1]
  else:
    raise Exception('{0} not found in the {1} file'.format(section, filename))

  return db

def main(args):
  grader_conf = {}
  if args.config:
    grader_conf = read_db_config(args.config, 'grader')
  
  #establish compitition start time
  start_time = time.time()
  #TODO - use config file
  end_time   = datetime.timedelta(hours=int(args.duration.partition(':')[0]),
                                  minutes=int(args.duration.partition(':')[2])).total_seconds() + start_time
  #create a queue
  q = queue.Queue()
  
  #connect to mysql server
  try:
    conf = {
      'user'    : args.username,
      'password': args.password,
      'host'    : args.host,
      'database': args.database
    }
    if args.config:
      conf.update(read_db_config(args.config))
    
    cnx = mysql.connector.connect(conf)
  except Error as e:
    print(e)
  finally:
    #close connection no matter what
    cnx.close()
  
  #file watcher
  observer = Observer()
  if 'submission_dir' in grader_conf.keys():
    observer.schedule(SubmissionWatcher(), path=grader_conf['submission_dir'])
  else:
    observer.schedule(SubmissionWatcher(), path=args.submission_dir)
  observer.start()
  
  #grader manager
  if 'table' in grader_conf.keys():
    grade_manager = ThreadGrader(q, cnx, grader_conf['table']) #create - w/ config file
  else:
    grade_manager = ThreadGrader(q, cnx, args.table) #create - w/o config file
  grade_manager.setDaemon(True)   #do not exit until all things needed to be graded are graded
  grade_manager.start()
  
  #wait until end of compitition
  while time.time() <= end_time + 50: #give 50 second leeway
    #TODO - get input here, so that it was possible to add time
    time.sleep(1)
  
  #end watchdog
  observer.stop()
  observer.join()
