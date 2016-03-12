#!/usr/bin/env python3

import queue, datetime, re

try:
  from tkinter import *
  from tkinter.ttk import *
  import tkinter.font as tkFont
except:
  from Tkinter import *
  import Tkinter.font as tkFont
  from Tkinter.ttk import *

def time(s):
  if re.search('^\\d\\d:\\d\\d$', s):
    return datetime.datetime.strptime(datetime.date.today().isoformat()+s+':00',
                             '%Y-%m-%d%H:%M:%S')
  else:
    return datetime.datetime.strptime(datetime.date.today().isoformat()+s,
                             '%Y-%m-%d%H:%M:%S')

class MultiColumnListbox(Frame):
  """use a TreeView as a multicolumn ListBox"""

  def __init__(self, root, header):
    Frame.__init__(self, root)
    self.tree      = None
    self.header    = header
    self.info_list = []
    self._setup_widgets()
    self._build_tree()

  def _setup_widgets(self):
    s = """\click on header to sort by that column
to change width of column drag boundary
    """
    # create a treeview with dual scrollbars
    self.tree = Treeview(self, columns=self.header, show="headings")
    vsb = Scrollbar(self, orient="vertical",
                          command=self.tree.yview)
    hsb = Scrollbar(self, orient="horizontal",
                          command=self.tree.xview)
    self.tree.configure(yscrollcommand=vsb.set,
                        xscrollcommand=hsb.set)
    self.tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)

  def update(self, new_list):
    self.info_list = new_list
    self._build_tree()

  def _build_tree(self):
    self.tree.delete(*self.tree.get_children())
    for col in self.header:
      self.tree.heading(col, text=col.title(),
        command=lambda c=col: self.sortby(self.tree, c, 0))
      # adjust the column's width to the header string
      self.tree.column(col,
        width=tkFont.Font().measure(col.title()))

    for item in self.info_list:
      self.tree.insert('', 'end', values=item)
      # adjust column's width if necessary to fit each value
      for ix, val in enumerate(item):
        col_w = tkFont.Font().measure(val)
        if self.tree.column(self.header[ix],width=None)<col_w:
          self.tree.column(self.header[ix], width=col_w)

  def sortby(self, tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
      for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
      tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
      int(not descending)))

class App:
  def __init__(self, observer, queue, done, end, g):
    self.queue    = queue
    self.observer = observer
    self.done     = done
    self.end      = end
    self.grader   = g
    self.root = Tk()
    self.root.wm_title("DHS-HSPC Grader")
    self.root.geometry("900x304+200+200")
    self.root.bind_class("Text",  "<Control-a>", self.display_selectall)
    self.root.bind_class("Entry", "<Control-a>", self.entry_selectall)

    self.mainframe = Frame(self.root)
    self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    self.mainframe.columnconfigure(0, weight=1)
    self.mainframe.rowconfigure(0, weight=1)

    header = ['Team Name', 'Problem Number', 'Attempt', 'Grade']
    self.queue_table = MultiColumnListbox(self.mainframe, header[:3])
    self.queue_table.grid(row=1, column=0, rowspan=5)

    self.done_table = MultiColumnListbox(self.mainframe, header)
    self.done_table.grid(row=1, column=4, rowspan=5)

    self.btn1 = Button(self.mainframe, text="Stop",
                       command=lambda: self.clicked('stop'))
    self.btn1.grid(row=6, column=4)

    self.timer_text  = StringVar()
    self.timer_text.set('Time Remaining: 00:00:00')
    self.timer_label = Label(self.mainframe, textvariable=self.timer_text)
    self.timer_label.grid(row=0, column=1, columnspan=3)

    self.separator1 = Separator(self.mainframe, orient='horizontal')
    self.separator1.grid(row=2, column=3, sticky='ew')

    self.grader_text  = StringVar()
    self.grader_text.set('Waiting')
    self.grader_label = Label(self.mainframe, width=25, anchor='center',
                              textvariable=self.grader_text)
    self.grader_label.grid(row=3, column=3)

    self.separator2 = Separator(self.mainframe, orient='horizontal')
    self.separator2.grid(row=4, column=3, sticky='ew')

    messages = 'Values for result:\n0: not graded\n1: good(complete)\n' \
               '2: formatting error\n3: compile error\n' \
               '4: no main class found or syntax error\n5: run time error\n' \
               '6: ran for too long\n7: outputs do not match\n' \
               'other: very very bad error\n'

    self.grade_values = Label(self.mainframe, anchor='center', text=messages)
    self.grade_values.grid(row=5, column=3)

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
      self.end = datetime.datetime.now()
      self.observer.stop()
      self.observer.join()
    elif 'time' in button.lower():
      try:
        tmp = time(self.time_input.get())
        if self.end > datetime.datetime.now():
          self.end = tmp
      except ValueError:
        print("please go back to 1st grade and learn how to represent time")
    self.update()

  def update(self):
    tmp = [(i[1]['team_name'], i[1]['problem_id'],
            i[1]['attempts']) for i in self.queue.queue]
    self.queue_table.update(tmp)

    tmp = [(i['team_name'], i['problem_id'],
            i['attempts'],  i['result']) for i in self.done]
    self.done_table.update(tmp)

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
    if not self.queue.empty() or (self.grader and self.grader.status()):
      return
    self.observer.stop()
    self.observer.join()
    self.root.quit()

'''
obs = None
q = queue.Queue()
q.put(('a', {'team_name':'team_1', 'problem_id':3, 'attempts':2}))
done = [{'team_name':'another team', 'problem_id':2, 'attempts':1, 'result':5}]
g = None
end = datetime.datetime.strptime(datetime.date.today().isoformat()+'23:00:00',
                                 '%Y-%m-%d%H:%M:%S')
app = App(obs, q, done, end, g)
app.mainloop()
print('I got Here')
'''