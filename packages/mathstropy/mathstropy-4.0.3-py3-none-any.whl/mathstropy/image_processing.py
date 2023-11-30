import cv2
import numpy as np

def load_image(path):
    """
    This function read image from local directory.

    Parameters:
    - path (str): path to image file

    Return:
    - numpy.array: 3D array of image
    """
    image = cv2.imread(path)
    return image


def get_colors(frame):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_thresh = {
        "red": [[0, 100, 45], [4, 255, 255]],
        "green": [[50, 50, 45], [102, 255, 255]],
        "blue": [[108, 50, 45], [130, 255, 255]],
        "yellow": [[16, 100, 100], [39, 255, 255]],
        "black": [[0, 0, 0], [180, 255, 42]],
        "white": [[0, 0, 230], [180, 48, 255]],
    }

    colors = list(color_thresh.keys())

    color_data_rgb = {}
    color_channel_data_binary = {}
    for i, color in enumerate(colors):
        feat_mask = cv2.inRange(
            hsv_image,
            np.array(color_thresh[color][0]),
            np.array(color_thresh[color][1]),
        )

        if color == "red":
            feat_mask = feat_mask | cv2.inRange(
                hsv_image,
                np.array([175, 70, 50]),
                np.array([180, 255, 255]),
            )

        color_channel_data = cv2.bitwise_and(frame, frame, mask=feat_mask)

        color_channel_data = color_channel_data.sum(axis=2).astype(np.uint8)
        color_channel_data_binary[color] = cv2.threshold(
            color_channel_data, 0, i + 1, cv2.THRESH_BINARY
        )[1]

        color_data_rgb[color] = color_channel_data.copy()

    color_final = np.zeros(color_channel_data_binary["red"].shape)
    # Make sure there is no color overlap
    for i in range(len(colors)):
        color_final += color_channel_data_binary[colors[i]]

    return color_final, color_data_rgb


def get_edges(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_frame, 100, 200, apertureSize=3)

    grad_x = cv2.Sobel(edges, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(edges, cv2.CV_64F, 0, 1, ksize=3)

    grad_mag = cv2.magnitude(grad_x, grad_y)
    grad_mag = cv2.normalize(grad_mag, None, 0, 255, cv2.NORM_MINMAX)
    grad_dir = np.arctan2(grad_x, grad_y) * 180 / np.pi

    # edge quantization
    edge_thresholds = {
        "0": [-15, 15],
        "45": [30, 60],
        "90": [75, 105],
        "135": [-60, -30],
    }
    edge_dir = {}
    for i, (direction, th) in enumerate(edge_thresholds.items()):
        edge_dir[direction] = np.bitwise_and(grad_dir >= th[0], grad_dir <= th[1])
        edge_dir[direction] = np.bitwise_and(edge_dir[direction], grad_mag > 200)
        edge_dir[direction] = edge_dir[direction].astype(np.uint8) * (i + 1)

    return edge_dir["0"] + edge_dir["45"] + edge_dir["90"] + edge_dir["135"]


def get_edge_features(edges_data):
    num_edges = get_edge_count(edges_data)

    # TODO: calculate the edge percentage
    edge_feature = [0, 0, 0, 0]
    for i in range(4):
        edge_feature[i] = num_edges[i] / sum(num_edges)

    return edge_feature


def get_edge_count(frame):
    """
    This function counts the number of horizontal, vertical and diagonal edges in an image.

    Parameters:
    - frame(np.array): 3D array of image

    Return:
    - dict: dictionary of count of edges
    """
    num_edge_dict = {
        "horizontal": 0,
        "fwd-diag": 0,
        "vertical": 0,
        "bkwd-diag": 0,
    }  # RGBY

    # parse edge info
    edges_data = get_edges(frame)

    for i in range(edges_data.shape[0]):
        for j in range(edges_data.shape[1]):
            if edges_data[i][j] == 1:
                num_edge_dict["horizontal"] = num_edge_dict["horizontal"] + 1
            elif edges_data[i][j] == 2:
                num_edge_dict["fwd-diag"] = num_edge_dict["fwd-diag"] + 1
            elif edges_data[i][j] == 3:
                num_edge_dict["vertical"] = num_edge_dict["vertical"] + 1
            elif edges_data[i][j] == 4:
                num_edge_dict["bkwd-diag"] = num_edge_dict["bkwd-diag"] + 1

    return num_edge_dict


def get_color_features(colors_data):
    # number of
    num_colors = get_color_count(colors_data)

    # TODO: calculate the color percentage
    N = colors_data.size  # number of all pixels
    color_feature = [0, 0, 0, 0]
    for i in range(4):
        color_feature[i] = num_colors[i] / N

    return color_feature


def get_color_count(frame, output_type="np-array", unified=False):
    """
    This function counts the number of each color

    Parameters:
    - frame(np.array): 3D array of image
    - output_type(str): type of output
    - unified(bool): flag if to unify count

    Return:
    - dict: dictionary of count of RGBY
    """
    colors_data, _ = get_colors(frame)
    num_colors_dict = {
        "red": 0,
        "green": 0,
        "blue": 0,
        "yellow": 0,
        "black": 0,
        "white": 0,
    }  # RGBYKW

    for i in range(colors_data.shape[0]):
        for j in range(colors_data.shape[1]):
            if colors_data[i][j] == 1:
                num_colors_dict["red"] = num_colors_dict["red"] + 1
            elif colors_data[i][j] == 2:
                num_colors_dict["green"] = num_colors_dict["green"] + 1
            elif colors_data[i][j] == 3:
                num_colors_dict["blue"] = num_colors_dict["blue"] + 1
            elif colors_data[i][j] == 4:
                num_colors_dict["yellow"] = num_colors_dict["yellow"] + 1
            elif colors_data[i][j] == 5:
                num_colors_dict["black"] = num_colors_dict["black"] + 1
            elif colors_data[i][j] == 6:
                num_colors_dict["white"] = num_colors_dict["white"] + 1

    return num_colors_dict


def resize_max(frame, max_size):
    max_dim = max(frame.shape[0], frame.shape[1])

    scale_h = frame.shape[0] / max_dim
    scale_w = frame.shape[1] / max_dim

    if scale_h == 1:
        scale = max_size / frame.shape[0]
    elif scale_w == 1:
        scale = max_size / frame.shape[1]

    return cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))