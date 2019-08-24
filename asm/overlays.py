#!/usr/bin/env python3
import cv2

def main_overlay(img, nfd, texp_us, gain, temp, settings):
    # Set exposure text
    if texp_us>=1000000:
        text = "Exposure: %.3f s" % (float(texp_us)*1e-6)
    elif (texp_us>=1000) & (texp_us<1000000):
        text = "Exposure: %.3f ms" % (float(texp_us)*1e-3)
    elif texp_us<1000:
        text = "Exposure: %.3f us" % float(texp_us)

    # Font names
    fontnames = [cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_DUPLEX,
                 cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_TRIPLEX, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                 cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, cv2.FONT_HERSHEY_SCRIPT_COMPLEX]

    # Line types
    linetypes = [cv2.LINE_AA, 8, 4]
    
    # Extract font settings
    fontname = fontnames[int(settings["fontname"])]
    fontcolor = tuple(int(s) for s in settings["fontcolor"].split(" "))
    smallfontcolor = tuple(int(s) for s in settings["smallfontcolor"].split(" "))
    fontsize = float(settings["fontsize"])
    fonttype = linetypes[int(settings["fonttype"])]
    fontline = int(settings["fontline"])
    
    # Add text
    x0, y0 = int(settings["textx"]), int(settings["texty"])
    yoff = int(30.0*fontsize/0.7)

    cv2.putText(img, settings["text"], (x0, y0),
                fontname, fontsize, fontcolor, fontline, fonttype)
    if int(settings["time"]) == 1:
        cv2.putText(img, nfd, (x0, y0+yoff),
                    fontname, fontsize, fontcolor, fontline, fonttype)
    if int(settings["showDetails"]) == 1:
        cv2.putText(img, "Temperature: %.1f C" % temp, (x0, y0+2*yoff),
                    fontname, 0.8*fontsize, smallfontcolor, fontline, fonttype)
        cv2.putText(img, text, (x0, y0+3*yoff),
                    fontname, 0.8*fontsize, smallfontcolor, fontline, fonttype)
        cv2.putText(img, "Gain: %d" % gain, (x0, y0+4*yoff),
                    fontname, 0.8*fontsize, smallfontcolor, fontline, fonttype)

    return
