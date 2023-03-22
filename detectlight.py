# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 20:26:30 2021
@author: ragnhiij

Identifies the Xth percentile pixel value (e.g. the 95th) in each frame of .mp4 video files. 
This is useful to identify frames in which e.g. a light comes on in otherwise dark videos.
    - Loads .mp4 files from input folder specified towards the end of this script
    - Plots a percentile pixel value (specified towards the end of this script) for each frame, one plot per video file
    - Saves the percentile pixel values for each video file in a .csv file 
"""

# Import necessities
import pathlib  # For dealing with path and filenames
import numpy as np
import matplotlib.pyplot as plt
import imageio  # For dealing with video files
from tqdm import tqdm
import csv
import fire
from typing import Tuple, List, Iterable, Dict, Any


# Functions
def identify_files(path: pathlib.Path) -> Tuple[List[pathlib.Path], int]:
    '''
    Identifies .mp4 files in the specified folder

    Parameters
    ----------
    path          : pathlib.Path
                    path to the folder to look for .mp4 files in
                        
    Returns
    -------
    video_files   : list
                    the path (including file name) of the identified .mp4 files
    no_files      : int
                    the number of .mp4 files found in the folder
    '''

    video_files = list(path.glob('*.mp4'))
    no_files = len(video_files)  # Number of mp4 files
    return video_files, no_files


def get_frame_values(video_files: Iterable[pathlib.Path], percentile_value: int) -> List[Dict[str, Any]]:
    '''
    Gets one pixel value (defined by the set percentile_value) per frame in a video file

    Parameters
    ----------
    video_files       : list
                        path of the file (inluding the name of the file)
    percentiile_value : int
                        the desired percentile pixel value to obtain from each frame

    Returns
    -------
    video_data        : list 
                        a list of dictionaries containing the path of the video file (same as the video_files parameter),
                        the calculated pixel value for each frame in the video file
                        and the percentile value used to calculate those values

    '''
    # Make sure the video_files argument is actually a list
    assert type(video_files) == list, "video_files is not a list"

    video_data = []  # Define a list to store the values from each video in

    for fname in tqdm(video_files):  # Loop through each video file (each filename)
        vid = imageio.get_reader(fname, 'ffmpeg')  # Read the video file

        temp_video_data = []  # Define a list to temporarily store pixel values in
        for frame in vid.iter_data():  # Loop through each frame in the video
            temp_video_data.append(np.percentile(frame,
                                                 percentile_value))  # Calculate and save the desired percentile value from the frame

        value_dict = {
            "fname": fname,
            "values": temp_video_data,
            "percentile": percentile_value
        }
        video_data.append(
            value_dict)  # Save the values from all the frames into the dictionary, indexed the path to the video file in question
    return video_data


def plot_frame_values(path: pathlib.Path, video_data: Iterable[Dict[str, Any]]) -> None:
    '''
    Plots the frame values for each frame (if frame_value contains multiple files, one plot is generated per file)
    and saves the frame values in a .csv file (one .csv file per video file)

    Parameters
    ----------
    path               : pathlib.Path
                         the path to the folder in which the plots should be saved
    
    video_data         : list
                         a list of dictionaries that each contain the path of the video file (inluding the name of the file),
                         the associated values (one value per frame in the file)
                         and the value used to calculate those values (i.e. a percentile)

    Returns
    -------
    image              : png
                         a plot showing the value (y-axis) of each frame (x-axis)

    file               : csv
                         a .csv file containing the (y-axis) values used to generate the plot mentioned above
    '''
    for video_dict in video_data:  # Loop through the dictionaries in the list
        figure = plt.figure()  # Create a plot
        ax = figure.add_subplot(111)

        ax.plot(video_dict["values"])  # Plot the frame values

        ax.set_ylabel(f'{video_dict["percentile"]}th percentile pixel intensity (AU)')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xlabel("Frame number")

        ax.set_title(video_dict["fname"])  # Set the path of the file as the title

        # Save the figure in the folder defined, with the name of the original file and the percentile value used
        plt.savefig(path / f'{video_dict["fname"]}_{video_dict["percentile"]}.png', dpi=300)

        # Save the values in a .csv file in the folder defined, with the name of the original file and the percentile value used
        with open(f'{video_dict["fname"]}_{video_dict["percentile"]}.csv', 'w',
                  newline='') as csvfile:  # Create/open a csv file to save the data in
            writer = csv.writer(csvfile)  # Prepare to write to the csv file
            for value in video_dict["values"]:
                writer.writerow([value])  # Save the values to the csv file


# Main code
def main(initial_path: str = "", percentile: int = 95) -> None:
    """Detect light

    Parameters
    ----------
    initial_path (string): Folder with video files in it
    percentile (int): The percentile value to use

    Returns
    -------
    None
    """
    if not initial_path:
        initial_path = r"C:\Users\rjaco\Desktop\test"

    # Make the path understandable
    path = pathlib.Path(initial_path)

    print("")
    print("Running...")

    video_files, no_files = identify_files(path)  # Identify .mp4 files in the folder
    video_data = get_frame_values(video_files, percentile)  # Get the chosen percentile pixel value for each frame
    plot_frame_values(path,
                      video_data)  # Plot the pixel value for each frame and save the plot in the same folder as the video files along with a .csv file containing the values

    print("")
    print("Finished!")


if __name__ == "__main__":
    fire.Fire(main)
