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
  def __init__(self, q, sql, done, args):#set up variables
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
    return self.description #info on the submission curently being graded

  def run(self):
    while True:
      #grabs job from queue, when they appear
      file_name, info = self.queue.get()

      #set description(used by gui)
      self.description = '{} {:02} ({:03})'.format(info['team_name'],
                                                   info['problem_id'],
                                                   info['attempts'])

      #create a grader obj(to grade the submission)
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

      #possible return messages(should be a class thing)
      messages = ['not graded', 'complete', 'formatting error',
                  'compile error', 'no main class found', 'run time error',
                  'ran for too long', 'outputs do not match']

      #As I distrust Oracle, I have created a xml file to store in the archive
      xml = '''<submission>
  <team id=\"{team_id}\">{team_name}</team>
  <problem>{problem_id}</problem>
  <grade code={grade_code}>{grade_message}</grade>
  <attempt>{attempt}</attempt>
  <time>{submission_time}</time>
</submission>'''

      if submission.extract_info():#find main method(return true if found)
        if submission.compile():   #attempt to compile(true if comiles)
          result = submission.run()#run submission and get status(some number)
        else:
          result = 3 #could not compile
      else:
        result = 4 #main not found


      #set archive name for submission
      archive_name = '{team_id}_{problem_id}_{attempt}.zip'.format(
                      team_id=info['team_id'],
                      problem_id=info['problem_id'],
                      attempt=info['attempts'])
      #set absolute path for submission archive
      archive_name = os.path.join(self.archive_dir, archive_name)
      info_file    = tempfile.mkstemp()[1]#temporary xml file
      with open(info_file, 'w') as f:     #write to temp xml file
        f.write(xml.format(team_name=info['team_name'],
                           team_id=info['team_id'],
                           problem_id=info['problem_id'],
                           attempt=info['attempts'],
                           grade_code=result,
                           grade_message=messages[result] if result < 8 and \
                             result > 0 else 'Unknown ERROR(bad)',
                           submission_time=info['time']))


      zipper = zipfile.ZipFile(archive_name, 'w',zipfile.ZIP_DEFLATED)#open arch
      for root, dirs, files in os.walk(submission.get_dir()):#add files to arch
        for file in files:                                   # from submission
          zipper.write(os.path.join(root, file), arcname=file)
      zipper.write(info_file, arcname='info.xml')#add xml file to arch
      zipper.close()

      info['result'] = result#set the result
      self.done.append(info)#tell gui we done

      #delete tmp stuffs
      os.remove(info_file)#info file(inside of new archive)

      shutil.rmtree(file_name)#original submission(graded copy is in archive_dir)
      if os.path.exists(file_name):
        os.rmdir(file_name)

      shutil.rmtree(submission.get_dir())#grading dir(already in new archive)
      if os.path.exists(submission.get_dir()):
        os.rmdir(submission.get_dir())

      self.cursor = self.sql.cursor()#prepare to tell db the status of stuff
      #updates results into 'graded' column of /table/
      query = 'UPDATE {} SET grade=\'{}\' WHERE submission_name=\'{}\''
      self.cursor.execute(query.format(self.subs_table, result,
                                       info['submission_name']))

      #notification command for VM
      command = 'notify.sh {} {}'.format(info['problem_id'], info['result'])

      #send notification command to VM using ssh using pub key
      if 'submission_ip' in info.keys() and info['submission_ip']:
        ssh = subprocess.Popen(['ssh', '-i', 'client_rsa', '-o',
                               'StrictHostKeyChecking=no',
                               'guest@'+info['submission_ip'], command],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
      else:#if failure, print
        message= 'Please tell team \"{}\" that the result for problem {} is: {}'
        print(message.format(info['team_name'], info['problem_id'],
                             messages[result] if result < 8 and result > 0 \
                                              else 'Unknown ERROR(bad)'))

      self.cursor.close()
      self.sql.commit()#not sure, but this fixed an error
      #signals to queue job is done
      self.queue.task_done()
      self.description = None#not working on stuff anymore
