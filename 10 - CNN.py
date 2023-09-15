############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import numpy as np

############################################################
# Individual Functions
############################################################

def convolve_greyscale(image, kernel):
    (image_height, image_width) = image.shape

    kernel = np.flip(kernel)
    (kernel_height, kernel_width) = kernel.shape

    (y, x) = kernel_height // 2, kernel_width // 2
    image_pad = np.pad(image, ((y, y), (x, x)), mode='constant', constant_values=(0))

    output = np.zeros((image_height, image_width))
    for y in range(image_height):
        for x in range(image_width):
            output[y][x] = np.sum(kernel * image_pad[y : y + kernel_height, x : x + kernel_width])
    return output


def convolve_rgb(image, kernel):
    (image_height, image_width, image_depth) = image.shape

    output = np.zeros((image_height, image_width, image_depth))
    for channel in range(image_depth):
        output[:, :, channel] = convolve_greyscale(image[:, :, channel], kernel)
    return output


def pooling_helper(image, kernel, stride, max_pooling=True):
    (image_height, image_width) = image.shape
    (kernel_height, kernel_width) = kernel
    (stride_height, stride_width) = stride
    (output_height, output_width) = 1 + image_height - kernel_height, 1 + image_width - kernel_width

    output = []
    for y in range(0, output_height, stride_height):
        output_yx = []
        for x in range(0, output_width, stride_width):
            if (max_pooling):
                output_yx.append(np.max(image[y : y + kernel_height, x : x + kernel_width]))
            else:
                output_yx.append(np.average(image[y : y + kernel_height, x : x + kernel_width]))
        output.append(output_yx)
    return np.array(output)


def max_pooling(image, kernel, stride):
    return pooling_helper(image, kernel, stride)


def average_pooling(image, kernel, stride):
    return pooling_helper(image, kernel, stride, max_pooling=False)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))