import subprocess
import javalang
import tempfile
import fnmatch
import shutil
import time
import os, re

try:
  from subprocess import DEVNULL # py3k
except ImportError:
  import os
  DEVNULL = open(os.devnull, 'wb')

def is_text(fn):
  msg = subprocess.Popen(['file', fn, '-b', '--mime'], stdout=subprocess.PIPE).communicate()[0]
  return 'text' in msg

class Grader:
  def __init__(self, submission, test_dir, num, timeout):
    #the file that will be compared against
    self.test_output = '{test}/{num:02}/output'.format(test=test_dir, num=num)
    #the input file
    self.test_input  = '{test}/{num:02}/input'.format(test=test_dir, num=num)
    #the file where the output will be writen
    self.outfile     = ''

    #set the timeout
    self.timeout     = timeout

    #location to extract to
    self.submission_dir = tempfile.mkdtemp(prefix='grader_staging_')

    #copy dir
    os.rmdir(self.submission_dir)
    shutil.copytree(submission, self.submission_dir)

    #remove .class files
    for root, dirs, files in os.walk(self.submission_dir):
      for f in fnmatch.filter(files, '*.[cC][lL][Aa][sS][sS]'):
        os.remove(os.path.join(root, f))

    #the java file which will be run
    self.main_class  = ''

  '''
  outputs:
    True:  compiled
    False: didn't
  '''
  def compile(self):
    mycmd = ['javac',
             os.path.join(self.main_class[0], self.main_class[1]+'.java')]
    tester = subprocess.Popen(mycmd,          stdin=subprocess.PIPE,
                              stdout=DEVNULL, stderr=subprocess.STDOUT)
    while tester.poll() is None:
      time.sleep(1)
    return tester.returncode == 0

  '''
  outputs:
    True:  main was found
    False: not
  '''
  def extract_info(self):
    self.outfile = os.path.join(self.submission_dir, 'output')

    #find main java file
    for root, dirs, files in os.walk(self.submission_dir):
      for file in fnmatch.filter(files, '*.java'):
        if is_text(os.path.join(root, file)):
          with open(os.path.join(root, file), 'r') as f:
            source = f.read()
            tree = javalang.parse.parse(source)
            for klass in tree.types:
              if isinstance(klass, javalang.tree.ClassDeclaration):
                for m in klass.methods:
                  if m.name == 'main' and \
                     m.modifiers.issuperset({'public', 'static'}):
                       self.main_class = (root, klass.name)

    problem_number = -1 #place holder for errors
    team_id        = -1 #place holder for errors

    return self.main_class != ''

  '''
  outputs:
    True:  good
    False: baad
  '''
  def compare(self):
    status = 7
    with open(self.outfile, 'r') as user, \
         open(self.test_output, 'r') as test:
      u_out   = user.read().replace('\r', '\r')
      correct = test.read().replace('\r', '\r')

    if u_out == correct:
      status = 1
    elif re.sub('([\\s\n:]+|0*(?:[0-9]+)(\\.\\d*)?)', '', u_out.lower()) == \
         re.sub('([\\s\n:]+|0*(?:[0-9]+)(\\.\\d*)?)', '', correct.lower()):
      status = 2
    return status

  def get_dir(self):
    return self.submission_dir

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
  def run(self):
    mycmd = ['java', '-classpath', self.main_class[0], self.main_class[1]]
    try:
      with open(self.outfile, 'w') as outfile, \
           open(self.test_input, 'r') as infile:
        start  = time.time()
        tester = subprocess.Popen(mycmd, stdin=infile,
                                  stdout=outfile, stderr=DEVNULL)
        while tester.poll() is None:
          if (time.time() - start) > self.timeout:
            tester.kill()
            return 6
          time.sleep(0.5)
      if tester.returncode != 0:
        return 5
      else:
        return self.compare() #change it if you don't like it
    except IOError as e:
      #Should not happen, I think
      #Note I should watch my language in school related projects
      #  but then again, who's gonna read this?
      print('Error: {}'.format(e.strerror))
      return 9999
