#!/usr/bin/env python3

import queue, datetime

try:
  from tkinter import *
except:
  from Tkinter import *

class Table(Frame):
  def __init__(self, root):
    Frame.__init__(self, root)
    self.scrollbar = Scrollbar(self)
    self.scrollbar.pack(side=RIGHT, fill=Y)
    self.lbox = Listbox(self, yscrollcommand=self.scrollbar.set)
    self.lbox.pack(side=LEFT)
    self.scrollbar.config(command=self.lbox.yview)

  def update(self, info_list):
    self.lbox.delete(0, END)
    for i in info_list:
      self.lbox.insert(END, i)

class App:
  def __init__(self, observer, queue, done, end):
    self.queue    = queue
    self.observer = observer
    self.done     = done
    self.end      = end
    self.root = Tk()
    self.root.wm_title("DHS-HSPC Grader")
    self.root.geometry("520x300+300+300")
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
    self.btn1.grid(row=6, column=3)

    self.timer_text  = StringVar()
    self.timer_text.set('Time Remaining: 00:00:00')
    self.timer_label = Label(self.mainframe, textvariable=self.timer_text)
    self.timer_label.grid(row=0, column=3)

    self.update()

  def entry_selectall(self, event):
    event.widget.select_range(0, END)

  def display_selectall(self, event):
    event.widget.tag_add(SEL, '1.0', END)

  def clicked(self, button):
    if 'stop' in button.lower():
      self.observer.stop()
      self.observer.join()
    elif 'stop' in button.lower():
      self.observer.stop()
      self.observer.join()

  def update(self):
    queued_item = [i[0] for i in self.queue.queue]
    tmp = ['{} - {}({})'.format(i['team_name'], i['problem_id'],
                                i['attempts']) for i in queued_item]
    self.queue_table.update(tmp)

    tmp = ['{} - {}({}): {}'.format(i['team_name'], i['problem_id'],
                                i['attempts'],  i['result']) for i in self.done]
    self.done_table.update(tmp)

    sec = (self.end - datetime.datetime.now()).seconds
    h   = int(sec / 3600)
    m   = int(sec / 60) % 60
    s   = int(sec % 60)

    self.timer_text.set('Time Remaining: {:02}:{:02}:{:02}'.format(h, m, s))

    self.root.after(500, self.update)

  def mainloop(self):
    self.root.mainloop()

  def quit(self):
    self.root.quit()
