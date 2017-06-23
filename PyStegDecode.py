import png
import sys

# get file names from command arguments or user input
if len(sys.argv) != 3:
    print(sys.argv[0], ' <encoded file> <output file>')
    container = raw_input('Encoded File: ')
    output = raw_input('Output File: ')
else:
    container = sys.argv[1]
    output = sys.argv[2]

# process encoded file
contreader = png.Reader(file = open(container, 'rb'))
contread = contreader.read()
grid = []
for line in contread[2]:
    grid.append(line)
x = contread[0]
y = contread[1]

di = 0 # data index
li = 0 # length index
length = 0

data = []

# get the last bit of each channel of each pixel
for line in grid:
    for i in xrange(0, len(line), 1):
        if li < 32: # get the header
            bit = line[i] & 1
            length <<= 1
            length |= bit
            li += 1
        elif di < length * 8: # get the content
            if di % 8 == 0:
                data.append(0)
            data[di // 8] <<= 1
            data[di // 8] |= line[i] & 1
            di += 1

out = open(output, 'wb') # output and close
out.write(bytearray(data))
out.close()
