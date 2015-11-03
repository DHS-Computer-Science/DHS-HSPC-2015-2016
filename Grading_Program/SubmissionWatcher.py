import time  
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 

class SubmissionWatcher(PatternMatchingEventHandler):
  patterns = ["*.zip"]

  def on_created(self, event):
    self.process(event)
    #TODO - add submissions to queue
    #queue.put(<path to zip>) #TODO - attach path to zip 
