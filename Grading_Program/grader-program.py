#!/usr/bin/env python3

import main
import sys
import argparse

if __name__ == '__main__':
  #read arguments from command line
  parser = argparse.ArgumentParser(description=__doc__)
  parser  .add_argument('submission_dir',   nargs='?', default='C:/xampp/submissions', help='directory to watch for submissions')
  parser  .add_argument('-c', '--config',              default=None,                   help='config file')
  parser  .add_argument('-e', '--duration',            default='04:00',                help='duration of cometition, format HH:MM')
  parser  .add_argument('-s', '--host',                default='localhost',            help='url of mysql server')
  parser  .add_argument('-u', '--username',            default='root',                 help='username to mysql server')
  parser  .add_argument('-p', '--password',            default='password',             help='password to mysql server')
  parser  .add_argument('-d', '--database',            default='teams',                help='database to connect to(of the mysql server)')
  parser  .add_argument('-t', '--table',               default='submissions',          help='table to update in database')
  #TODO - add test dir arg(ya'know 'e on' wit 'e pro'lems)

  #TODO use `vars(parser.parse_args())` to turn args into a dictionary
  args   = parser.parse_args()

  #TODO - mergre conf here
  main.main(args)
