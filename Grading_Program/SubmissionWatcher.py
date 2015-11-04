import time
import shutil
import tempfile
from watchdog.events import PatternMatchingEventHandler 

class SubmissionWatcher(PatternMatchingEventHandler):
  patterns = ["*.zip"]
  staging_dir = tempfile.mkdtemp(prefix='grader_staging_')
  
  def on_created(self, event):
    self.process(event)
    path_name = os.path.join(staging_dir, os.path.basename(event.src_path))
    
    shutil.move(event.src_path, path_name)
    queue.put(path_name)
