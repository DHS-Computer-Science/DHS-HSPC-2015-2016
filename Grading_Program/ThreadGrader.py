import os
import queue
import shutil
import zipfile
import threading
import tempfile
from Grader import Grader
import subprocess
import mysql.connector

class ThreadGrader(threading.Thread):
  """Threaded Url Grab"""
  def __init__(self, q, sql, done, args):
    threading.Thread.__init__(self)
    self.queue       = q
    self.subs_table  = args['subs_table']
    self.archive_dir = args['archive_dir']
    self.problem_dir = args['problems_dir']
    self.timeout     = args['timeout']
    self.sql         = sql
    self.done        = done
    self.description = None

  def status(self):
    return self.description

  def run(self):
    while True:
      #grabs job from queue
      file_name, info = self.queue.get()

      self.description = '{} {:02} ({:03})'.format(info['team_name'],
                                                   info['problem_id'],
                                                   info['attempts'])

      submission = Grader(file_name, self.problem_dir,
                          info['problem_id'], self.timeout)

      '''
      Values for result:
        0: not graded
        1: good(complete)
        2: formatting error
        3: compile error
        4: no main class found
        5: run time error
        6: ran for too long
        7: outputs do not match
        other: very very bad error
      '''

      messages = ['not graded', 'complete', 'formatting error',
                  'compile error', 'no main class found', 'run time error',
                  'ran for too long', 'outputs do not match']

      xml = '''<submission>
  <team id=\"{team_id}\">{team_name}</team>
  <problem>{problem_id}</problem>
  <grade code={grade_code}>{grade_message}</grade>
  <attempt>{attempt}</attempt>
  <time>{submission_time}</time>
</submission>'''

      if submission.extract_info():
        if submission.compile():
          result = submission.run()
        else:
          result = 3 #could not compile
      else:
        result = 4 #main not found


      archive_name = '{team_id}_{problem_id}_{attempt}.zip'.format(
                      team_id=info['team_id'],
                      problem_id=info['problem_id'],
                      attempt=info['attempts'])
      archive_name = os.path.join(self.archive_dir, archive_name)
      info_file    = tempfile.mkstemp()[1]
      with open(info_file, 'w') as f:
        f.write(xml.format(team_name=info['team_name'],
                           team_id=info['team_id'],
                           problem_id=info['problem_id'],
                           attempt=info['attempts'],
                           grade_code=result,
                           grade_message=messages[result] if result < 8 and \
                             result > 0 else 'Unknown ERROR(bad)',
                           submission_time=info['time']))


      zipper = zipfile.ZipFile(archive_name, 'w',zipfile.ZIP_DEFLATED)
      for root, dirs, files in os.walk(submission.get_dir()):
        for file in files:
          zipper.write(os.path.join(root, file), arcname=file)
      zipper.write(info_file, arcname='info.xml')
      zipper.close()

      info['result'] = result
      self.done.append(info)

      #delete
      os.remove(info_file)#info file(inside of new archive)

      shutil.rmtree(file_name)#original submission(graded copy is in archive_dir)
      if os.path.exists(file_name):
        os.rmdir(file_name)

      shutil.rmtree(submission.get_dir())#grading dir(already in new archive)
      if os.path.exists(submission.get_dir()):
        os.rmdir(submission.get_dir())

      self.cursor = self.sql.cursor()
      #updates results into 'graded' column of /table/
      query = 'UPDATE {} SET grade=\'{}\' WHERE submission_name=\'{}\''
      self.cursor.execute(query.format(self.subs_table, result,
                                       info['submission_name']))

      command = 'notify.sh {} {}'.format(info['problem_id'], info['result'])

      if 'submission_ip' in info.keys() and info['submission_ip']:
        ssh = subprocess.Popen(['ssh', '-i', 'client_rsa', '-o',
                               'StrictHostKeyChecking=no',
                               'guest@'+info['submission_ip'], command],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
      else:
        message= 'Please tell team \"{}\" that the result for problem {} is: {}'
        print(message.format(info['team_name'], info['problem_id'],
                             messages[result] if result < 8 and result > 0 \
                                              else 'Unknown ERROR(bad)'))

      self.cursor.close()
      self.sql.commit()
      #signals to queue job is done
      self.queue.task_done()
      self.description = None
