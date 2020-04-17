#!/usr/bin/env python3
import cv2

def main_overlay(img, nfd, texp_us, gain, temp, settings):
    # Set exposure text
    if texp_us >= 1000000:
        text = "Exposure: %.3f s" % (float(texp_us) * 1e-6)
    elif (texp_us >= 1000) & (texp_us < 1000000):
        text = "Exposure: %.3f ms" % (float(texp_us) * 1e-3)
    elif texp_us < 1000:
        text = "Exposure: %.0f us" % float(texp_us)

    # Font names
    fontnames = [cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_DUPLEX,
                 cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_TRIPLEX, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                 cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, cv2.FONT_HERSHEY_SCRIPT_COMPLEX]

    # Line types
    linetypes = [cv2.LINE_AA, 8, 4]

    # Binning factor
    nbin = int(settings["bin"])
    
    # Extract font settings
    fontname = fontnames[int(settings["fontname"])]
    fontcolor = tuple(int(s) for s in settings["fontcolor"].split(" "))
    smallfontcolor = tuple(int(s) for s in settings["smallfontcolor"].split(" "))
    fontsize = float(settings["fontsize"])/float(nbin)
    fonttype = linetypes[int(settings["fonttype"])]
    fontline = int(settings["fontline"])//nbin
    
    # Text position
    x0, y0 = int(settings["textx"])//nbin, int(settings["texty"])//nbin
    yoff = int(30.0 * fontsize / 0.7)

    # Add freeform text
    cv2.putText(img, settings["text"], (x0, y0),
                fontname, fontsize, fontcolor, fontline, fonttype)

    # Add date
    if int(settings["time"]) == 1:
        y0 += yoff
        cv2.putText(img, nfd, (x0, y0),
                    fontname, fontsize, fontcolor, fontline, fonttype)
    # Add details
    if int(settings["showDetails"]) == 1:
        y0 += yoff
        cv2.putText(img, "Temperature: %.1f C" % temp, (x0, y0),
                    fontname, 0.8 * fontsize, smallfontcolor, fontline, fonttype)
        y0 += yoff
        cv2.putText(img, text, (x0, y0),
                    fontname, 0.8 * fontsize, smallfontcolor, fontline, fonttype)
        y0 += yoff
        cv2.putText(img, "Gain: %d" % gain, (x0, y0),
                    fontname, 0.8 * fontsize, smallfontcolor, fontline, fonttype)

    return
