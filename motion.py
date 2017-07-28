from tempimage import TempImage
import dropbox
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())

warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

dbx = dropbox.Dropbox("-Y6P1w4QzLAAAAAAAAAADkqIQsUOvQlGb1Q8NnEvKVA6N0Vng-NDtdxjOW8x92oo")

# initialize camera
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size = tuple(conf["resolution"]))

if conf["show_video"]:
	print("[INFO] Displaying feed. Press 'q' to quit.")
	
# allow camera to warm up, init avg frame, timestamp, motion counter
print("[INFO] camera warming...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# capture frames from cam
for f in camera.capture_continuous(rawCapture, format="bgr",
			 use_video_port=True, splitter_port=0):

	frame0 = f.array
	timestamp = datetime.datetime.now()
	text = "No Motion"

	# resize, grayscale, blur
	frame = imutils.resize(frame0, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21,21), 0)

	if avg is None:
		print("[INFO] Now Monitoring...")
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		continue	
	
	# compare frame averages
	# frameDelta = background_model - current_frame
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
	# thresh, dialate, find contours
	thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
			cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)

	cnts, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# loop over contours
	for c in contours:
		if cv2.contourArea(c) < conf["min_area"]:
			continue
		# compute the bounding box, draw, add text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
		text = "Motion Detected"

	# draw text and timestamp
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, "Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	# Dropbox
	if text == "Motion Detected":
		# has enough time passed?
		if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
			motionCounter += 1
		# is consistent motion high enough?
		if motionCounter >= conf["min_motion_frames"]:
			if conf["use_dropbox"]:
				t = TempImage()
				cv2.imwrite(t.path, frame)
				t0 = TempImage()
				cv2.imwrite(t0.path, frame0)
			with open('motion_log.txt', 'a') as text_file:
				print("[UPLOAD] {}".format(ts), file=text_file)
			path = "{base_path}/{timestamp}.jpg".format(
				base_path=conf["dropbox_base_path"], timestamp=ts)
			path0 = "{base_path}/{timestamp}_original.jpg".format(
				base_path=conf["dropbox_base_path"], timestamp=ts)	
			with open(t.path, "rb") as f:
				print("[MOTION DETECTED] File Uploaded: {}".format(ts))
				dbx.files_upload(f.read(), path)
			with open(t0.path, "rb") as f0:
				dbx.files_upload(f0.read(), path0)
			t.cleanup()
			t0.cleanup()			
			
			# update variables
			lastUploaded = timestamp
			motionCounter = 0
	else:
		motionCounter = 0

	# display on screen?
	if conf["show_video"]:
		cv2.imshow("Security Feed", frame)
		key = cv2.waitKey(1) & 0xFF
		# quit clause
		if key == ord("q"):
			print("Quitting...")
			camera.close()
			raise SystemExit()

	# clear stream in prep for next frame
	rawCapture.truncate(0)


