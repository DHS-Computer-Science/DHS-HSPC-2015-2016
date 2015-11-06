#!/usr/bin/env python3

import main
import sys
import argparse
from configparser import ConfigParser

def read_db_config(filename='config.ini', section='mysql'):
  """ Read database configuration file and return a dictionary object
  :param filename: name of the configuration file
  :param section: section of database configuration
  :return: a dictionary of database parameters
  """
  # create parser and read ini configuration file
  parser = ConfigParser()
  parser.read(filename)

  # get section, default to mysql
  db = {}
  if parser.has_section(section):
    items = parser.items(section)
    for item in items:
      db[item[0]] = item[1]
  else:
    raise Exception('{0} not found in the {1} file'.format(section, filename))

  return db

if __name__ == '__main__':
  #read arguments from command line
  parser = argparse.ArgumentParser(description=__doc__)
  parser  .add_argument('-c', '--config',              default=None,                   help='config file')
  parser  .add_argument('-e', '--duration',            default='04:00',                help='duration of cometition, format HH:MM')
  parser  .add_argument('-i', '--host',                default='localhost',            help='url of mysql server')
  parser  .add_argument('-u', '--username',            default='root',                 help='username to mysql server')
  parser  .add_argument('-p', '--password',            default='password',             help='password to mysql server')
  parser  .add_argument('-d', '--database',            default='teams',                help='database to connect to(of the mysql server)')
  parser  .add_argument('-t', '--table',               default='submissions',          help='table to update in database')
  parser  .add_argument('-o', '--problems',            default='C:/problems',          help='directory with problem input/output files')
  parser  .add_argument('-s', '--submission',          default='C:/xampp/submissions', help='directory to watch for submissions')
  parser  .add_argument('-a', '--archive',             default='C:/archive',           help='directory where graded submission end up')

  args = vars(parser.parse_args())

  if args['config']:
    args.update(read_db_config(args['config'], 'grader'))

  main.main(args)
