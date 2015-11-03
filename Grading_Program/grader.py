import subprocess
import zipfile
import os

class Grader:
  def __init__(self):
    self.output_file = 'out' #TODO
    self.input_file  = 'in'  #TODO
    self.main_class  = ''    #Guess what? TODO
  
  '''
  
  '''
  def compile(self):
    ;#TODO
  
  def extract_info(self):
    ;#TODO - everything
    #also give error if no main class is found
  
  '''
  outputs:
    True:  good
    False: baad
  '''
  def compare(self):
    ;#TODO - this has to do stuff
  
  '''
  outputs:
    0: good job
    2: run time error
    1: outputs do not match(The world is a mess, just like my numbering)
    anything else: I don't know, figure it out yourself
    3: file error(note this should be on the line above)
  '''
  def run(self):
    mycmd = ['java', self.main_class]
    try:
      with open('out', 'w') as outfile, open('in', 'r') as infile:
        start  = time.time()
        tester = subprocess.Popen(mycmd, stdin=infile, stdout=outfile)
        while (time.time() - start) < 60 and p.poll() is None:
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
