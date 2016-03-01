import time, os
import shutil, re
import tempfile
import mysql.connector
from io import StringIO
from watchdog.events import PatternMatchingEventHandler

class SubmissionWatcher(PatternMatchingEventHandler):
  patterns = ["*.zip"]
  staging_dir = tempfile.mkdtemp(prefix='grader_staging_')

  def __init__(self, sql, table):
    PatternMatchingEventHandler.__init__(self)
    self.cursor = sql.cursor()
    self.table  = table

  def on_created(self, event):
    #self.process(event)
    file_name = os.path.basename(event.src_path)
    path_name = os.path.join(self.staging_dir, file_name)

    shutil.move(event.src_path, path_name)

    #get 8 char hash (generated by the Submission Program) from file name
    basename   = re.search('(.{8})\\.zip$', file_name).group(1)

    #self.cursor.execute(a)
    self.cursor.execute("SELECT * FROM {} WHERE submission_name = \'{}\'".format(self.table, basename))
    info = {'attempts':0}
    columns = tuple([d[0] for d in self.cursor.description])
    for row in self.cursor:
      info.update(dict(zip(columns, row)))

    self.cursor.execute("SELECT team_name FROM teams WHERE team_id = \'{}\'".format(info['team_id']))
    columns = tuple([d[0] for d in self.cursor.description])
    info.update(dict(zip(columns, row)))

    self.cursor.execute("SELECT * FROM {} WHERE (problem_id = \'{}\' AND team_id = \'{}\')".format(self.table, info['problem_id'], info['team_id']))
    for row in self.cursor:
      info['attempts'] += 1

    queue.put((path_name, info))
