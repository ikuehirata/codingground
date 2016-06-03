# -*- coding: utf-8 -*-

#import string
import sys

# factor px to mm
fc = 25.4/90

# offset for date strings
datestringsoffset = [1.48, 2.08, 2.32, 2.92, 3.52, 4.12, 4.72, 5.32]

# y offset
offsety = 7.16

def main():
        if len(sys.argv) < 3:
                print 'input file name and date needed'
                return
        else:
                fname = sys.argv[1]
                datestring = sys.argv[2]
        if len(datestring) != 8:
                print 'date format incorrect'
                return

        # file type definition
        if not fname.split('.')[-1] == 'ptn':
                print 'This file is not supported.'
                return

        # open existing file to get pattern data
        f = open(fname, 'r')
        lines = f.readlines()
        f.close()
        before = lines[:-3]
        after = lines[-3:]

        # setup number data
        for num in range(1,10):
                f = open(datestring + '-' + str(num) + fname, 'w')
                # header
                for elm in before:
                        # check width
                        if elm.find('<Width>') > -1:
                                w0 = elm.strip().replace('<Width>', '')
                                w = w0.replace('</Width>', '')
                                if float(w) < 8:
                                        f.write('<Width>8</Width>')
                                else:
                                        f.write(elm)
                        # check height
                        elif elm.find('<Height>') > -1:
                                w0 = elm.strip().replace('<Height>', '')
                                w = float(w0.replace('</Height>', ''))
                                f.write('<Height>%f</Height>'%(w+0.1))
                        else:
                                f.write(elm)
                # date drops
                for (n, o) in zip(datestring, datestringsoffset):
                        f.write(drops(int(n), o)) 
                # number drops
                f.write(drops(num, 6.28))
                # footer
                for elm in after:
                        f.write(elm)
                f.close()

def drops(num, offsetx):
        prt = []
        # setup bars
        a = [0, 0, 0.400, 0.020]
        b = [0, 0, 0.040, 0.440]
        c = [0.360, 0, 0.040, 0.440]
        d = [0, 0.440, 0.400, 0.020]
        e = [0, 0.440, 0.040, 0.480]
        f = [0.360, 0.440, 0.040, 0.480]
        g = [0, 0.920, 0.400, 0.020]

        if num == 0:
                prt = [a,b,c,e,f,g]
        elif num == 1:
                prt = [c,f]
        elif num == 2:
                prt = [a,c,d,e,g]
        elif num == 3:
                prt = [a,c,d,f,g]
        elif num == 4:
                prt = [b,c,d,f]
        elif num == 5:
                prt = [a,b,d,f,g]
        elif num == 6:
                prt = [a,b,d,e,f,g]
        elif num == 7:
                prt = [a,c,f]
        elif num == 8:
                prt = [a,b,c,d,e,f,g]
        elif num == 9:
                prt = [a,b,c,d,f,g]

        s = ""
        for elm in prt:
                s = s + """	<Drop>
		<StartX>%f</StartX>
		<StartY>%f</StartY>
		<XWidth>%f</XWidth>
		<YHeight>%f</YHeight>
	        </Drop>
""" % (elm[0]+offsetx, elm[1]+offsety, elm[2], elm[3])
        return s

main()
