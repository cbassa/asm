#!/usr/bin/env python3
import argparse
import os
import sys
import json
import time
import cv2
import zwoasi as asi
import numpy as np
from stas.io import write_fits_file
from stas.overlays import main_overlay

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Capture all sky images from an ASI camera.")
    parser.add_argument("-s", "--settings", help="JSON file with settings", default=None)
    parser.add_argument("-p", "--path", help="Output path", default=None)
    parser.add_argument("-l", "--live", help="Display live view", action="store_true")
    args = parser.parse_args()

    # Check arguments
    if args.settings == None or args.path == None:
        parser.print_help()
        sys.exit()
        
    # Read settings
    try:
        with open(args.settings, "r") as fp:
            settings = json.load(fp)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Live view
    if args.live:
        live = True
    else:
        live = False
        
    # Check path
    path = os.path.abspath(args.path)

    # Intialize SDK library
    try:
        asi.init(os.getenv("ZWO_ASI_LIB"))
    except Exception as e:
        print(e)
        sys.exit(1)

    # Find cameras
    ncam = asi.get_num_cameras()
    if ncam == 0:
        print("No ZWO ASI cameras found")
        sys.exit(1)

    # Decode settings
    if settings["autoexposure"] == "1":
        auto_exp = True
    else:
        auto_exp = False
    if settings["autogain"] == "1":
        auto_gain = True
    else:
        auto_gain = False
    texp_us = 1000*int(settings["exposure"])
    texp_us_max = 1000*int(settings["maxexposure"])
    gain = int(settings["gain"])
    gain_max = int(settings["maxgain"])
    gain_min = 0

    # Set daytime
    nighttime = False

    # Stabilize
    stable = False
    
    # Initialize camera 0
    camera = asi.Camera(0)
    camera_info = camera.get_camera_property()

    # Set control values
    camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, int(settings["usb"]))
    camera.set_control_value(asi.ASI_EXPOSURE, texp_us, auto=auto_exp)
    camera.set_control_value(asi.ASI_AUTO_MAX_EXP, texp_us_max//1000)
    camera.set_control_value(asi.ASI_GAIN, gain, auto=auto_gain)
    camera.set_control_value(asi.ASI_AUTO_MAX_GAIN, gain_max)
    camera.set_control_value(asi.ASI_WB_B, int(settings["wbb"]))
    camera.set_control_value(asi.ASI_WB_R, int(settings["wbr"]))
    camera.set_control_value(asi.ASI_GAMMA, int(settings["gamma"]))
    camera.set_control_value(asi.ASI_BRIGHTNESS, int(settings["brightness"]))
    camera.set_control_value(asi.ASI_FLIP, int(settings["flip"]))
    camera.set_control_value(asi.ASI_AUTO_MAX_BRIGHTNESS, 80)
    camera.disable_dark_subtract()
    camera.set_roi(bins=1)

    # Start capture
    camera.start_video_capture()
    camera.set_image_type(asi.ASI_IMG_RAW8)
    
    # Forever loop
    while True:
        # Capture frame
        t0 = time.time()
        img = camera.capture_video_frame()
        
        # Get settings
        camera_settings = camera.get_control_values()

        # Stability tet
        if texp_us == camera_settings["Exposure"] and gain == camera_settings["Gain"]:
            stable = True

        # Extract settings
        texp_us = camera_settings["Exposure"]
        texp = float(texp_us)/1000000
        gain = camera_settings["Gain"]
        temp = float(camera_settings["Temperature"])/10.0

        # Exposure logic: change to auto gain if maximum exposure reached
        if (texp_us==texp_us_max) & (gain<gain_max) & (auto_gain==False) & (nighttime == False):
            auto_exp = False
            auto_gain = True
            nighttime = True
            camera.set_control_value(asi.ASI_GAIN, gain, auto=auto_gain)
            camera.set_control_value(asi.ASI_EXPOSURE, texp_us_max, auto=auto_exp)
            print("Setting auto gain!")
        # Switch to auto exp if minimum gain reached
        elif (gain==gain_min) & (auto_exp==False) & (nighttime == True):
            auto_exp = True
            auto_gain = False
            nighttime = False
            camera.set_control_value(asi.ASI_GAIN, gain_min, auto=auto_gain)
            camera.set_control_value(asi.ASI_EXPOSURE, texp_us_max, auto=auto_exp)
            print("Setting auto exposure!")

        # Format start time
        nfd = "%s.%03d" % (time.strftime("%Y-%m-%dT%T",
                           time.gmtime(t0)), int((t0-np.floor(t0))*1000))

        print(nfd, texp, gain, temp, nighttime, auto_exp, auto_gain)
        
        # Store FITS file
#        if nighttime == True:
#            write_fits_file(os.path.join(path, "%s.fits" % nfd), img, nfd, texp, gain, temp)
            
        # Get RGB image
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BAYER_BG2BGR)

        # Add overlay
        main_overlay(rgb_img, nfd, texp_us, gain, temp, settings)

        # Store image
        if stable:
            cv2.imwrite(os.path.join(path, settings["filename"]), rgb_img)
            cv2.imwrite(os.path.join(path, "%s.jpg" % nfd), rgb_img)
        
        # Show image
        if live and stable:
            ny, nx = img.shape
            cv2.imshow("Capture", cv2.resize(rgb_img, (nx//2, ny//2)))
            cv2.waitKey(1)

        # Execute daytime sleep
        if not nighttime and stable:
            t1 = time.time()

            # Compute sleep time
            tsleep = float(settings["daytimeDelay"])/1000.0-t1+t0
            time.sleep(tsleep)
        
    camera.stop_video_capture()
