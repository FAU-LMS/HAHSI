import numpy as np
import os
from tools import Color, PGMImageIO
import time
import cv2 as cv

def load_video(hs_image_folder, start_frame=0, end_frame=-1):
    start = time.time()
    channel_folders = os.listdir(hs_image_folder)
    channels = 0
    for folder in channel_folders:
        if folder.startswith('Cam-'):
            channels += 1
    load_frames = -1
    hs_video = None
    for channel in range(channels):
        print("Load channel " + str(channel))
        channel_folder = os.path.join(hs_image_folder, 'Cam-' + str(channel))
        if load_frames == -1:
            actual_end_frame = len(os.listdir(channel_folder)) - 1
            if end_frame >= 0:
                actual_end_frame = np.minimum(end_frame, actual_end_frame)

            load_frames = actual_end_frame - start_frame + 1
            print("Loading " + str(load_frames) + " frames...")

        for frame in range(start_frame, start_frame + load_frames):
            path = channel_folder + '/frame_' + str(frame) + '.pgm'
            print(path)
            img = PGMImageIO.load(path)
            if hs_video is None:
                hs_video = np.zeros((channels, load_frames, img.shape[0], img.shape[1]), dtype=np.uint8)

            hs_video[channel, frame - start_frame, ...] = img

    print("Loading took: ", time.time() - start)

    start = time.time()
    rgb_video = np.zeros((load_frames, hs_video.shape[2], hs_video.shape[3], 3), dtype=np.uint8)
    max_values = np.zeros(load_frames)
    for frame in range(hs_video.shape[1]):
        result = Color.hs_image_to_rgb(hs_video[:, frame])
        max_values[frame] = np.max(result)
        rgb_video[frame] = cv.convertScaleAbs(result, alpha=255/max_values[frame], beta=0)

    max_max_value = np.max(max_values)
    for frame in range(hs_video.shape[1]):
        rgb_video[frame] = cv.convertScaleAbs(rgb_video[frame], alpha=max_values[frame]/max_max_value, beta=0)
    hs_video = np.swapaxes(hs_video, 0, 1)
    print("Converting took: ", time.time() - start)
    return hs_video, rgb_video