import subprocess
import tempfile
import zipfile
import filecmp
import fnmatch
import os

class Grader:
  def __init__(self, path_to_zip, test_dir='problems', num):
    #the file that will be compared against
    self.test_output = '{test}/{num}/output'.format(test=test_dir, num=num)
    #the input file
    self.test_input  = '{test}/{num}/input'.format(test=test_dir, num=num)
    #the file where the output will be writen
    self.outfile     = ''

    #location to extract to
    self.submission_dir = tempfile.mkdtemp(prefix='grader_staging_')

    #extract files
    archexract = zipfile.ZipFile(path_to_zip)
    archexract.extractall(self.submission_dir)
    archexract.close()

    #remove .class files
    for root, dirs, files in os.walk(self.submission_dir):
      for file in fnmatch.filter(files, '*.class'):
        os.remove(os.path.join(root, file))

    #the java file which will be run
    self.main_class  = ''

  '''
  outputs:
    True:  compiled
    False: didn't
  '''
  def compile(self):
    mycmd = ['javac', self.main_class]
    tester = subprocess.Popen(mycmd)
    while p.poll() is None:
      time.sleep(1)
    return tester.returncode == 0

  '''
  outputs:
    True:  main was found
    False: not
  '''
  def extract_info(self):
    self.outfile = self.submission_dir+'.output'

    #find main java file
    for root, dirs, files in os.walk(self.submission_dir):
      for file in fnmatch.filter(files, '*.java'):
        with open(os.path.join(root, file), 'r') as f:
          if 'void main(String' in f.read():
            self.main_class = os.path.join(root, file)

    problem_number = -1 #place holder for errors
    team_id        = -1 #place holder for errors

    return self.main_class != ''
    
  '''
  outputs:
    True:  good
    False: baad
  '''
  def compare(self):
    filecmp.cmp(self.outfile, self.test_output)

  def get_dir():
    return self.submission_dir

  '''
  Values for result:
    0: not graded
    1: good(complete)
    2: compile error
    3: no main class found
    4: run time error
    5: ran for too long
    6: outputs do not match
    other: error
  '''
  def run(self):
    mycmd = ['java', re.sub('(?i)\\.java$', '', self.main_class)]
    try:
      with open(self.outfile, 'w') as outfile, \
           open(self.test_input, 'r') as infile:
        start  = time.time()
        tester = subprocess.Popen(mycmd, stdin=infile, stdout=outfile)
        while p.poll() is None:
          if (time.time() - start) < 60:
            p.kill()
            return 5
          time.sleep(0.5)
        if tester.returncode != 0:
          return 4
        else:
          return (1 if self.compare() else 6) #change it if you don't like it
    except IOError as e:
      #Should not happen, I think
      #Note I should watch my language in school related projects
      #  but then again, who's gonna read this?
      print('Error: %s'.format(e.strerror))
      return 7
