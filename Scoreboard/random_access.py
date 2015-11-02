import struct

NUMBER_OF_PROBLEMS = 9
NAME_SIZE          = 40 #characters

rec_num = 0

t1 = [b'swaga squad', 3,3367, 1,1945, 2,1063, 6,0, 0,0, 0,0, 0,0, 0,0, 1,0]

#open file for writing binary data
#thefile = open('scores.db', 'r+b') #read and write
db = open('scores.db', 'wb')

#calculate size for 40 char team name and 9 entries
format_string = '{}p{}i'.format(NAME_SIZE, 2*NUMBER_OF_PROBLEMS)
record_size = struct.calcsize(format_string)

#seek 'rec_num' records into the file and unpack into 'field'
'''
db.seek(record_size * rec_num)
buffer = db.read(record_size)
field = list(struct.unpack(format_string, buffer))
'''

#pack field back into a buffer
buffer = struct.pack(format_string, *t1)
#return to beggining of field
db.seek(record_size * rec_num)
db.write(buffer)

db.close()
