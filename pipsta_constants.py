from escpos import constants, codepages, exceptions

ESC = b'\x1B'
GS = b'\x1D'

'''
Initialise
'''
INITIALISE = ESC + b'\x40'

'''
Data is stored in buffer until FormFeed or GS,L to exit spooling
is recieved, or paper feed button is pressed
'''
ENTER_SPOOLING = b'\x1B\x4C'

'''
Exit Spooling
'''
EXIT_SPOOLING = constants.GS + b'L'

'''
Underline 1BH,2DH,n:
if n is 0 then underline is off; otherwise on
'''
def underline(toggle:bool):
    UNDERLINE = b'\x1B\x2D' # Add n byte afterwards
    #If the parameter is True then turn on underline, otherwise turn it off
    if toggle == True:
        return UNDERLINE + b'\xFF'
    else:
        return UNDERLINE + b'\x00'

'''
Print and feed extra paper, final byte is number of 1/20 lines to feed.
'''
PRINT_AND_FEED_EXTRA_PAPER = b'\x1B\x4A'
def printFeedExtra(paper:bytes):
    return PRINT_AND_FEED_EXTRA_PAPER + paper

'''
Print and feed lines
'''
PRINT_AND_FEED_LINES = b'\x1B\x64'
def printAndFeedLines(lines:bytes):
    return PRINT_AND_FEED_LINES + lines

'''
Inverted Printing: ESC,"{",n
where n is a byte where bit 1 encodes for on/off
'''
def invertedPrinting(toggle:bool):
    if toggle == True:
        return ESC + b'{'+b'\xFF' 
    else:
        return ESC + b'{'+b'\x00'
    
'''
Barcode:
'''
def barcode(type:str,data:str):
    match type:
        case "UPC-A":
            numericType = b'\x00'
            terminator = b'\x00'
            alphanumeric = False
            numeric = True
        case "UPC-E":
            numericType = b'\x01'
            terminator = b'\x00'
            alphanumeric = False
            numeric = True
        case "EAN-13":
            numericType = b'\x02'
            terminator = b'\x00'
            alphanumeric = False
            numeric = True
        case "EAN-8":
            numericType = b'\x03'
            terminator = b'\x00'
            alphanumeric = False
            numeric = True
        case "Code 39":
            print("code39")
            numericType = b'\x04'
            terminator = b'\x00'
            alphanumeric = True
            numeric = False
        case "Int2 of 5":
            numericType = b'\x05'
            terminator = b'\x00'
            alphanumeric = False
            numeric = True
        case "Code 128A":
            numericType = b'\x06'
            terminator = b'\xFF'
            alphanumeric = True
            numeric = False
        case "Code 128B":
            numericType = b'\x07'
            terminator = b'\xFF'
            alphanumeric = True
            numeric = False
        case "Code 128C":
            numericType = b'\x08'
            terminator = b'\xFF'
            alphanumeric = False
            numeric = True
        case "Code 93":
            numericType = b'\x09'
            terminator = b'\xFF'
            alphanumeric = True
            numeric = False
    print(type)
    dataBytes = b''
    dataBytes = data.encode("ASCII")
    command = GS + b'\x6B' + numericType + dataBytes + terminator
    return command
