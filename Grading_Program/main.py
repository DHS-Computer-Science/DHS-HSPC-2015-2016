import sys
import queue
import Grader
import argparse
import ThreadGrader
import SubmissionWatcher

parser = argparse.ArgumentParser(description=__doc__)
parser  .add_argument('submission_dir',   nargs='?', default='.',         help='directory to watch for submissions')
parser  .add_argument('-s', '--url',                 default='localhost', help='url of mysql server')
parser  .add_argument('-u', '--username',            default='root',      help='username to mysql server')
parser  .add_argument('-p', '--password',            default='password',  help='password to mysql server')
parser  .add_argument('-d', '--database',            default='teams',     help='database to connect to(of the mysql server)')
                                            #TODO change teams ^ to the value that should be used
                                            #TODO add a config_file argument
args   = parser.parse_args()

q = queue.Queue()

#TODO create watcher and grader objects/threads/whatevers
