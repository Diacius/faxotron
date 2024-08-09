from escpos.printer import Usb
import time
import pipsta_constants
import os
import json
from pipsta_constants import ENTER_SPOOLING, EXIT_SPOOLING, ESC
from PIL import Image
from bitarray import bitarray
from time import sleep
import sys
from PIL import Image
USB_vendor = 0x0483
USB_product = 0xa19d
SET_FONT_MODE_3 = b'\x1b!\x00'
SET_LED_MODE = b'\x1bX\x2d'
FEED_PAST_CUTTER = b'\n' * 5
SELECT_SDL_GRAPHICS = b'\x1b*\x08'
USB_BUSY = 66
def pipsta_image(imageName, isFax):        
    '''
    Convert the image to 1bit black and white, and then create a bitarray of the
    1 bit data, then print it out in 48byte chunks @ 48B/line for 384 pixels of horizontal resolution!
    '''
    if isFax:
        os.system(f"convert {imageName} -resize 384x543\\! fixed.png")
        # reset the image name because we resized
        imageName = "fixed.png"
    # Create IO object from the passed in bytes and "open" it
    im = Image.open(imageName) # Open the colour image
    im = im.convert("1") # Make 1-bit monochrome
    im = im.resize(size=(384,im.height),resample=Image.Resampling.LANCZOS) # Resize the image so that it is the correct width!
    im.save("popo.png")
    pixellist = list(im.getdata()) # Generate a list containing every pixel as either 255 or 0.
    DOTS_PER_LINE = 384
    BYTES_PER_DOT_LINE = DOTS_PER_LINE//8 #(48)
    # ESC, *, 8(for dots), n1,n2,
    # first bit most significant, printed with first bit top-left
    # The number of bytes is given by (n1+ 256*n2)
    # Therefore we make  n1 for 48 bytes and n2 0
    DOTHEADER = ESC+b'*\x08\x30\x00'
    # Create a big endian bitarray, because the first bit gets printed first
    pixelarray1bit = bitarray(endian='big')
    # TODO: This is a little messy, can this be improved?
    for i in pixellist:
        # If the pixel is white it's a 0 for no dot
        if i == 255:
            pixelarray1bit.append(0)
        # If the pixel is black it's a 1 for a dot
        if i == 0:
            pixelarray1bit.append(1)
    # Convert the continous bitarray to bytes
    imgbytes = pixelarray1bit.tobytes()
    # Find the number of lines by dividing the number of bytes by the bytes per line value
    number_of_lines = len(imgbytes) // BYTES_PER_DOT_LINE
    # Create array to store the data that needs to be sent to the printer
    dataArray = []
    # Tell the printer to start spooling, so that processing does not cause the image to have gaps
    # For each line
    for i in range(number_of_lines):
        # Build the data to send to the printer from:
        # The header for dot-by-dot line printing
        # The image's bytes from: line number * bytes_per_line to that plus the bytes per line to get the data
        # in chunks for each line (usually 48 bytes)
        construct = DOTHEADER + imgbytes[i*BYTES_PER_DOT_LINE:(BYTES_PER_DOT_LINE*i)+BYTES_PER_DOT_LINE]
        # Send the built data to the printer as raw bytes using escpos' IO tools
        dataArray.append(construct)
        # TODO: A hardcoded sleep isn't paticularly sensible, the library supports reading the output
        # So lets work out how to wait until the data is processed correctly :)
        sleep(0.01)
    # Feed once  :)
    dataArray.append('\n')
    # Exit spooling mode which will print the buffer
    return dataArray
def imgsavetest(imageName):
    im = Image.open(imageName) # Open the colour image
    im = im.convert("1") # Make 1-bit monochrome
    # Resize the image so that it is the correct width!
    im.save("testoutp33ut.png")
# Change these to the correct values for your device
# You can find the values on linux using `lsusb`
USB_vendor = 0x0483
USB_product = 0xa19d

# Don't change this, it may break things
API_VERSION = 1

SET_FONT_MODE_3 = b'\x1b!\x00'
SET_LED_MODE = b'\x1bX\x2d'

# Newlines to get print above the tear bar - you may want to change this for your printer
feed_to_bar = '\n\n\n\n'

# If your printer is not a Pipsta/AP1400 SET THIS VALUE TO FALSE, otherwise image printing will be broken and may print large amounts of garbage.
# Setup a temporary connection to check we can connect to the printer

def image(filename):
    printerObject = Usb(USB_vendor, USB_product, 0, out_ep=0x2)
    printerObject._raw(pipsta_constants.ENTER_SPOOLING)
    printerObject.hw('INIT') 
    # Ensure that the printer is initialised, in case underline or other formatting is left on.
    #printerObject._raw(SET_FONT_MODE_3) # Set the font to 3, TODO: Is this needed? If so, why?
    # If we are using a pipsta use my code
    # Returns an array of raw data to send, one item per command
    printerObject._raw(pipsta_constants.invertedPrinting(False))
    printerObject._raw(pipsta_constants.underline(False))
    dataToSend = pipsta_image(filename, True)
    for command in dataToSend:
        printerObject._raw(command)
        time.sleep(0.01)
    printerObject._raw(pipsta_constants.EXIT_SPOOLING)
    printerObject.close()
image(sys.argv[1])