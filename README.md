# DetectLight
Identifies the Xth percentile pixel value (e.g. the 95th) in each frame of .mp4 video files. This is useful to identify frames in which e.g. a light comes on in otherwise dark videos.

detectlight.py takes as input the path to the folder containing video files to be processed, and the desired percentile value. As output it provides one plot for each video file showing the percentile pixel value for each frame in the video to make it easy to identify frames where there is a change in pixel intensities. The percentile pixel values are also saved in .csv files so the plots can be recreated/data analysed more closely if necessary. 
All output is saved in the same folder as the inpupt folder.


### How to use
1. Install dependencies (e.g. pip install -r requirements.txt)
2. Specify the path to the folder containing video files and which percentile value to use in the "Input section" in detectlight.py (towards the end of the file)
3. Run detectlight.py
