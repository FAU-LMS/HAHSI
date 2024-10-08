import numpy as np

def xyz_from_xy(x, y):
    return np.array((x, y, 1-x-y))

def read_color_matching_functions():
    with open('../data/cie1931') as f:
        lines = f.readlines()

    x = []
    y = []
    z = []
    for line in lines:
        line = line.strip()
        split = line.split(' ')
        wavelength = int(split[0])
        if wavelength % 10 != 0:
            continue

        x.append(float(split[1]))
        y.append(float(split[2]))
        z.append(float(split[3]))

    xyz = np.array([np.array(x), np.array(y), np.array(z)])
    return xyz

def hs_video_to_rgb(hs_video):
    if hs_video is None:
        return None

    # HS to XYZ
    cmf_xyz = read_color_matching_functions()
    # interpolate to different channels
    cmf_xyz_new = np.zeros((cmf_xyz.shape[0], hs_video.shape[0]))
    step = (700 - 400)/(cmf_xyz_new.shape[1] - 1)
    for i in range(cmf_xyz_new.shape[1]):
        cur_wl = 400 + step * i
        orig_index = (cur_wl - 400)/10
        lower_wl = int(orig_index)
        upper_wl = int(np.ceil(orig_index))
        alpha = 1 - (orig_index - lower_wl)
        resulting_vector = alpha * cmf_xyz[:, lower_wl] + (1 - alpha) * cmf_xyz[:, upper_wl]
        cmf_xyz_new[:, i] = resulting_vector
    cmf_xyz = cmf_xyz_new

    # XYZ to RGB
    red = xyz_from_xy(0.708, 0.292) #from chromaticity diagram
    green = xyz_from_xy(0.170, 0.797) #from chromaticity diagram
    blue = xyz_from_xy(0.131, 0.046) #from chromaticity diagram
    white = xyz_from_xy(0.3127, 0.3290) #D65 from chromaticity diagram

    M = np.vstack((red, green, blue)).T
    MI = np.linalg.inv(M)
    wscale = MI @ white
    T = MI / wscale[:, np.newaxis]

    comb_matrix = T @ cmf_xyz

    orig_shape = hs_video.shape
    hs_video = np.reshape(hs_video, (hs_video.shape[0], -1))
    rgb_video = comb_matrix @ hs_video
    rgb_video = np.reshape(rgb_video.T, (orig_shape[1], orig_shape[2], orig_shape[3], 3))

    if np.any(rgb_video < 0):
        rgb_video -= np.min(rgb_video)

    return rgb_video

def hs_image_to_rgb(hs_image):
    if hs_image is None:
        return None

    rgb_video = hs_video_to_rgb(hs_image[:, None, ...])
    return rgb_video