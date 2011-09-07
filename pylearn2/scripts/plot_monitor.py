#!/bin/env python
from pylearn2.utils import serial
import matplotlib.pyplot as plt
import numpy as N
import sys
from theano.printing import _TagGenerator

model = serial.load(sys.argv[1])
channels = model.monitor.channels


#Make a list of short codes for each channel so user can specify them easily
tag_generator = _TagGenerator()
codebook = {}
for channel_name in sorted(channels):
    code = tag_generator.get_tag()
    codebook[code] = channel_name


#if there is more than one channel in the monitor ask which ones to plot
prompt = len(channels.values()) > 0

if prompt:

    sorted_codes = sorted(codebook)

    #Display the codebook
    for code in sorted_codes:
        print code + '. ' + codebook[code]

    print

    response = raw_input('Enter a list of channels to plot (example: A, C,F-G)): ')

    #Remove spaces
    response = response.replace(' ','')

    #Split into list
    codes = response.split(',')

    final_codes = set([])

    for code in codes:
        if code.find('-') != -1:
            #The current list element is a range of codes

            rng = code.split('-')

            if len(rng) != 2:
                print "Input not understood: "+code
                quit(-1)

            found = False
            for i in xrange(len(sorted_codes)):
                if sorted_codes[i] == rng[0]:
                    found = True
                    break

            if not found:
                print "Invalid code: "+rng[0]
                quit(-1)

            found = False
            for j in xrange(i,len(sorted_codes)):
                if sorted_codes[j] == rng[1]:
                    found = True
                    break

            if not found:
                print "Invalid code: "+rng[1]
                quit(-1)

            final_codes = final_codes.union(set(sorted_codes[i:j+1]))
        else:
            #The current list element is just a single code
            final_codes = final_codes.union(set([code]))

else:
    final_codes ,= set(codebook.keys())

fig = plt.figure()
ax = plt.subplot(1,1,1)

# Shink current axis' width by 20% so legend will still appear in the window
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

plt.xlabel('# examples')


#plot the requested channels
for code in sorted(final_codes):

    channel_name= codebook[code]

    channel = channels[channel_name]

    plt.plot( N.asarray(channel.example_record), \
              N.asarray(channel.val_record), \
              label = channel_name)


plt.legend(bbox_to_anchor=(1.05, 1),  loc=2, borderaxespad=0.)

plt.show()