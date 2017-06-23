import png
import sys

# get file names from command arguments or user input
if len(sys.argv) != 4:
    print(sys.argv[0], ' <carrier file> <payload file> <output file>')
    container = raw_input('Carrier File: ')
    hidden = raw_input('Payload File: ')
    output = raw_input('Output File: ')
else:
    container = sys.argv[1]
    hidden = sys.argv[2]
    output = sys.argv[3]

# process carrier file
contreader = png.Reader(file = open(container, 'rb'))
contread = contreader.read()
grid = []
for line in contread[2]:
    grid.append(line)
x = contread[0]
y = contread[1]
maxbits = x * y * (4 if contread[3]['alpha'] else 3)

# process payload file
hiddenreader = open(hidden, 'rb')
data = hiddenreader.read()

length = len(data)
di = 0 # data index
li = 0 # length index

if (length * 8) + 32 > maxbits: # check if file is too big
    print('Payload is too large for carrier.')
    exit()

# change the last bit of each channel of each pixel to encode the file
for line in grid:
    for i in xrange(0, len(line), 1):
        if li < 32: # write the header
            bit = 1 if length & (1 << (31 - i)) else 0
            line[i] &= 254
            line[i] |= bit
            li += 1
        elif di < length * 8: # write the content
            bytei = di // 8
            modi = di % 8
            bit = 1 if ord(data[bytei]) & (1 << (7 - modi)) else 0
            line[i] &= 254
            line[i] |= bit
            di += 1

out = open(output, 'wb') # output and close
outpng = png.Writer(x, y, alpha = contread[3]['alpha'], interlace = 0)
outpng.write(out, grid)
out.close()
