import struct
import sys

if len(sys.argv) > 1 and sys.argv[1].lower() == 'help':
  print('usage:\n  {} [db_name [num_problems]]\n')
  print('if both args are specified, only team names will be asked for')
  print('other entries will default to zero')
  print('if only 1 or zero args are specified, evrything that is not specified')
  print('(including attempts and times) will be asked for')
  sys.exit(0)

NUMBER_OF_PROBLEMS = int(sys.argv[2]) if len(sys.argv) > 2 else int(input("Number of problems: "))
NAME_SIZE          = 40 #characters

rec_num = 0

t1 = [b'swaga squad', 3,3367, 1,1945, 2,1063, 6,0, 0,0, 0,0, 0,0, 0,0, 1,0]

#open file for writing binary data
#thefile = open('scores.db', 'r+b') #read and write
db = open(sys.argv[1] if len(sys.argv) > 1 else input('Name of db file: '), 'wb')

#calculate size for 40 char team name and 9 entries
format_string = '{}p{}i'.format(NAME_SIZE, 2*NUMBER_OF_PROBLEMS)
record_size = struct.calcsize(format_string)

#seek 'rec_num' records into the file and unpack into 'field'
'''
db.seek(record_size * rec_num)
buffer = db.read(record_size)
field = list(struct.unpack(format_string, buffer))
'''

records = int(input('Number of records: '))
for i in range(records):
  t = []
  t += [input('Team {} name: '.format(i+1))[:NAME_SIZE].encode()]
  for j in range(NUMBER_OF_PROBLEMS):
    if len(sys.argv) > 2:
      t += [0, 0]
    else:
      trys = int(input('  Team {} problem {} attempts: '.format(i+1, j+1)))
      times = int(input('  Team {} problem {} times(sec): '.format(i+1, j+1)))
      t += [trys, times]
  #pack field back into a buffer
  buffer = struct.pack(format_string, *t)
  #return to beggining of field
  #db.seek(record_size * rec_num)
  db.write(buffer)

db.close()
