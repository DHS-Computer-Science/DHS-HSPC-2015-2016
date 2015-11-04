import subprocess
import tempfile
import zipfile
import filecmp
import fnmatch
import os

class Grader:
  def __init__(self, path_to_zip):
    #the file that will be compared against
    self.test_output = 'problems/{num}/output'
    #the input file
    self.test_input  = 'problems/{num}/input'
    #the file where the output will be writen
    self.outfile     = ''
    
    #location to extract to
    self.submission_dir = tempfile.mkdtemp(prefix='grader_staging_')
    
    #extract files
    archexract = zipfile.ZipFile(path_to_zip)
    archexract.extractall(self.submission_dir)
    archexract.close()
    
    #remove .class files
    for root, dirs, files in os.walk(sefl.submission_dir):
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
  
  def extract_info(self):
    self.outfile = self.submission_dir+'.output'
    
    #find main java file
    #TODO - complain in no main was found
    for root, dirs, files in os.walk(self.submission_dir):
      for file in fnmatch.filter(files, '*.java'):
        with open(os.path.join(root, file), 'r') as f:
          if 'void main(String' in f.read():
            self.main_class = os.path.join(root, file)
    
    #TODO figure out problem number
    problem_number   = 4 #place holder
    self.test_output = self.test_output.format(num=problem_number)
    self.test_input  = self.test_input.format(num=problem_number)
    
    #TODO - should return team ID and problem #
    return (1, 1)
  
  '''
  outputs:
    True:  good
    False: baad
  '''
  def compare(self):
    filecmp.cmp(self.outfile, self.test_output)
  
  '''
  outputs:
    0: good job
    2: run time error
    1: outputs do not match(The world is a mess, just like my numbering)
    anything else: I don't know, figure it out yourself
    3: file error(note this should be on the line above)
    4: terminated, ran for too long
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
            return 4
          time.sleep(0.5)
        if tester.returncode != 0:
          return 2
        else:
          return (0 if self.compare() else 1) #change it if you don't like it
    except IOError as e:
      #Should not happen, I think
      #Note I should watch my language in school related projects
      #  but then again, who's gonna read this?
      print('Error: %s'.format(e.strerror))
      return 3
