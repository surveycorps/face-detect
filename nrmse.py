import numpy

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def nrmse(im1, im2):
    im1 = rgb2gray(im1)
    im2 = rgb2gray(im2)

    a, b = im1.shape

    rmse = numpy.sqrt(numpy.sum((im2 - im1) ** 2) / float(a * b))
    max_val = max(numpy.max(im1), numpy.max(im2))
    min_val = min(numpy.min(im1), numpy.min(im2))
    return 1 - (rmse / (max_val - min_val))

