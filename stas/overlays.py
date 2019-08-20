#!/usr/bin/env python3
import cv2

def main_overlay(img, nfd, texp_us, gain, temp, settings):
    # Set exposure text
    if texp_us>=1000000:
        text = "Exposure: %.3f s" % texp_us*1e-6
    elif (texp_us>=1000) & (texp_us<1000000):
        text = "Exposure: %.3f ms" % (texp_us*1e-3)
    elif texp_us<1000:
        text = "Exposure: %.3f us" % float(texp_us)
        
    # Add text
    x0, y0 = int(settings["textx"]), int(settings["texty"])
    yoff = 40
    cv2.putText(img, settings["text"], (x0, y0),
                cv2.FONT_HERSHEY_SIMPLEX, int(settings["fontsize"]), (255, 255, 255), int(settings["fontline"]), cv2.LINE_AA)
    cv2.putText(img, nfd, (x0, y0+yoff),
                cv2.FONT_HERSHEY_SIMPLEX, int(settings["fontsize"]), (255, 255, 255), int(settings["fontline"]), cv2.LINE_AA)
    cv2.putText(img, "Temperature: %.1f C" % temp, (x0, y0+2*yoff),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8*int(settings["fontsize"]), (0, 0, 255), int(settings["fontline"]), cv2.LINE_AA)
    cv2.putText(img, text, (x0, y0+3*yoff),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8*int(settings["fontsize"]), (0, 0, 255), int(settings["fontline"]), cv2.LINE_AA)
    cv2.putText(img, "Gain: %d" % gain, (x0, y0+4*yoff),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8*int(settings["fontsize"]), (0, 0, 255), int(settings["fontline"]), cv2.LINE_AA)

    return
