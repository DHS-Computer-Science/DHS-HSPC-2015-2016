#!/usr/bin/env python3

import queue, datetime, re

try:
  from tkinter import *
except:
  from Tkinter import *

def time(s):
  if re.search('^\\d\\d:\\d\\d$', s):
    return datetime.datetime.strptime(datetime.date.today().isoformat()+s+':00',
                             '%Y-%m-%d%H:%M:%S')
  else:
    return datetime.datetime.strptime(datetime.date.today().isoformat()+s,
                             '%Y-%m-%d%H:%M:%S')

class Table(Frame):
  def __init__(self, root):
    Frame.__init__(self, root)
    self.scrollbar = Scrollbar(self)
    self.scrollbar.pack(side=RIGHT, fill=Y)
    self.lbox = Listbox(self, yscrollcommand=self.scrollbar.set, width=28)
    self.lbox.pack(side=LEFT)
    self.scrollbar.config(command=self.lbox.yview)

  def update(self, info_list):
    self.lbox.delete(0, END)
    for i in info_list:
      self.lbox.insert(END, i)

class App:
  def __init__(self, observer, queue, done, end, g):
    self.queue    = queue
    self.observer = observer
    self.done     = done
    self.end      = end
    self.grader   = g
    self.root = Tk()
    self.root.wm_title("DHS-HSPC Grader")
    self.root.geometry("688x280+200+200")
    self.root.bind_class("Text",  "<Control-a>", self.display_selectall)
    self.root.bind_class("Entry", "<Control-a>", self.entry_selectall)

    self.mainframe = Frame(self.root)
    self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    self.mainframe.columnconfigure(0, weight=1)
    self.mainframe.rowconfigure(0, weight=1)

    self.queue_table = Table(self.mainframe)
    self.queue_table.grid(row=1, column=0, rowspan=5)

    self.done_table = Table(self.mainframe)
    self.done_table.grid(row=1, column=4, rowspan=5)

    self.btn1 = Button(self.mainframe, text="Stop",
                       command=lambda: self.clicked('stop'))
    self.btn1.grid(row=6, column=4)

    self.timer_text  = StringVar()
    self.timer_text.set('Time Remaining: 00:00:00')
    self.timer_label = Label(self.mainframe, textvariable=self.timer_text)
    self.timer_label.grid(row=0, column=1, columnspan=3)

    self.grader_text  = StringVar()
    self.grader_text.set('Waiting')
    self.grader_label = Label(self.mainframe,
                              width=25,
                              textvariable=self.grader_text)
    self.grader_label.grid(row=2, column=3)

    self.time_frame = Frame(self.mainframe)
    self.time_frame.grid(row=6, column=0)
    self.time_input = StringVar()
    self.time_input.set('{:02}:{:02}:{:02}'.format(self.end.hour,
                                                   self.end.minute,
                                                   self.end.second))
    self.time_entry =Entry(self.time_frame,width=8,textvariable=self.time_input)
    self.time_entry.grid(row=0, column=0)

    self.btn2 = Button(self.time_frame, text="Set End Time",
                       command=lambda: self.clicked('time'))
    self.btn2.grid(row=0, column=1)

    self.update()

  def entry_selectall(self, event):
    event.widget.select_range(0, END)

  def display_selectall(self, event):
    event.widget.tag_add(SEL, '1.0', END)

  def clicked(self, button):
    if 'stop' in button.lower():
      self.observer.stop()
      self.observer.join()
    elif 'time' in button.lower():
      try:
        self.end = time(self.time_input.get())
      except ValueError:
        print("please go back to 1st grade and learn how to represent time")
    self.update()

  def update(self):
    queued_item = [i[0] for i in self.queue.queue]
    tmp = ['{:-24} {:02} ({:03})'.format(i['team_name'], i['problem_id'],
                                         i['attempts']) for i in queued_item]
    self.queue_table.update(['name                     p# (sbm)']+tmp)

    tmp = ['{:-24} {:02} ({:03}):   {}'.format(i['team_name'], i['problem_id'],
                                i['attempts'],  i['result']) for i in self.done]
    self.done_table.update(['name                     p# (sbm): grade']+tmp)

    if self.end < datetime.datetime.now():
      h = 0
      m = 0
      s = 0
      self.observer.stop()
      self.observer.join()
    else:
      sec = (self.end - datetime.datetime.now()).seconds
      h   = int(sec / 3600)
      m   = int(sec / 60) % 60
      s   = int(sec % 60)

    self.timer_text.set('Time Remaining: {:02}:{:02}:{:02}'.format(h, m, s))

    if self.grader and self.grader.status():
      self.grader_text.set('Grading\n'+self.grader.status())
    else:
      self.grader_text.set('Waiting')

    self.root.after(500, self.update)

  def mainloop(self):
    self.root.mainloop()

  def quit(self):
    self.root.quit()

obs = None
q = queue.Queue()
done = []
g = None
end = datetime.datetime.strptime(datetime.date.today().isoformat()+'23:00:00', '%Y-%m-%d%H:%M:%S')
app = App(obs, q, done, end, g)
app.mainloop()
print('I got Here')
