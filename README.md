# DetectLight
Identifies the Xth percentile pixel value (e.g. the 95th) in each frame of .mp4 video files. This is useful to identify frames in which e.g. a light comes on in otherwise dark videos.

detectlight.py takes as input the path to the folder containing video files to be processed, and the desired percentile value. As output it provides one plot for each video file showing the percentile pixel value for each frame in the video to make it easy to identify frames where there is a change in pixel intensities. The percentile pixel values are also saved in .csv files so the plots can be recreated/data analysed more closely if necessary. 
All output is saved in the same folder as the inpupt folder.


### How to use
1. Install dependencies (e.g. pip install -r requirements.txt), use Python < 3.10.
3. Run detectlight.py: `python detectlight.py --initial_path=PATH`. For all possible options, run `python detectlight.py --help`.
