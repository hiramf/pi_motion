# pi_motion
This is a slightly modified version of the surveillance program written by Adrian Rosenbrock over at [pimagesearch](http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/). Whereas the original program was configured for refrigerator surveillance,  this program is for outdoor surveillance. I wanted to capture images of wildlife (rabbits, squirrels) in order to train a Neural Network in the future (see Microsoft's [ELL project](https://github.com/Microsoft/ELL/blob/master/tutorials/vision/gettingStarted/README.md)). Additionally, the original program returned small images. I modified the program to return a small image with a bounding box, as well as the full-size original image. Images are uploaded to a Dropbox account. I also added a log file.

## Getting Started
You will need an understanding of Raspberry Pi, python, command line interface, ssh, and vim (or some other text editor). 
### Hardware Requirements
- Raspberry Pi 3
- PiCamera v2
- Monitor/TV
#### Optional
- Physical Keyboard
- Adjustable tripod
- [PiCamera tripod mount](https://www.adafruit.com/product/3253)
- [Extended camera cable](https://www.adafruit.com/product/2143)

### Software Requirements
- [OpenCV](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/) (this is complex)
- A Virtual Environment with Python 3 (the tutorial uses `virtualenv`, but I used [`miniconda3`](https://github.com/Microsoft/ELL/blob/master/tutorials/vision/gettingStarted/compiling-Pi3.md))
- [Working Camera](http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)

### Special Python Modules Used
- picamera
- imutils
- cv2
- dropbox

## Deployment
[Follow this guide for details.](http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/)

Configure Settings:
> - show_video : A boolean indicating whether or not the video stream from the Raspberry Pi should be displayed to our screen.
> - use_dropbox : Boolean indicating whether or not the Dropbox API integration should be used.
> dropbox_access_token: Access token from Dropbox App
> dropbox_base_path : The name of your Dropbox App directory that will store uploaded images.
> min_upload_seconds : The number of seconds to wait in between uploads. For example, if an image was uploaded to Dropbox 5m 33s after starting our script, a second image would not be uploaded until 5m 36s. This parameter simply controls the frequency of image uploads.
> min_motion_frames : The minimum number of consecutive frames containing motion before an image can be uploaded to Dropbox.
> camera_warmup_time : The number of seconds to allow the Raspberry Pi camera module to “warmup” and calibrate.
> delta_thresh : The minimum absolute value difference between our current frame and averaged frame for a given pixel to be “triggered” as motion. Smaller values will lead to more motion being detected, larger values to less motion detected.
> resolution : The width and height of the video frame from our Raspberry Pi camera.
> fps : The desired Frames Per Second from our Raspberry Pi camera.
> min_area : The minimum area size of an image (in pixels) for a region to be considered motion or not. Smaller values will lead to more areas marked as motion, whereas higher values of min_area  will only mark larger regions as motion.

```
source activate py34
python motion.py --conf conf_headless.json
```
When using headless mode (`show_video`), you may get an error `Out of resources` if you try to run the program after quitting. Restarting the Pi will fix this. I'm currently working on a better solution...

Increasing the GPU memory with `sudo raspi-config` to `256` or `512` may improve performance.

## Authors
* Hiram Foster

## Acknowledgements
* Adrian Rosenbrock (Initial work)
