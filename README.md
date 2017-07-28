# pi_motion
This is a slightly modified version of the surveillance program written by Adrian Rosenbrock over at [pimagesearch](http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/). Whereas the original program was configured for refrigerator surveillance,  this program is for outdoor surveillance. I wanted to capture images of wildlife (rabbits, squirrels) in order to train a Neural Network in the future (see Microsoft's [ELL project](https://github.com/Microsoft/ELL/blob/master/tutorials/vision/gettingStarted/README.md)). Additionally, the original program returned small images. I modified the program to return a small image with a bounding box, as well as the full-size original image. Images are uploaded to a Dropbox account.

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
```
source activate py34
python motion.py --conf --conf.json
```
When using headless mode (`show_video`), you may get an error `Out of resources` if you try to run the program after quitting. Restarting the Pi will fix this. I'm currently working on a better solution...

Increasing the GPU memory with `sudo raspi-config` to `256` or `512` may improve performance.

## Authors
* Hiram Foster

## Acknowledgements
* Adrian Rosenbrock (Initial work)
