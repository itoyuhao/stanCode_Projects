"""
File: stanCodoshop.py
----------------------------------------------
SC101_Assignment3
Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.

-----------------------------------------------
SC101_Assignment3
Name: Kevin Chen
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): color distance between red, green, and blue pixel values

    """
    # color distance formula
    dist = ((red - pixel[0])**2 + (green - pixel[1])**2 + (blue - pixel[2])**2)**(1/2)
    return dist


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    # Create 3 variables for calculating
    total_r = 0
    total_g = 0
    total_b = 0
    for pixel in pixels:
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        # The RGB of each pixel will be summed
        total_r += r
        total_g += g
        total_b += b
    # Assign the average R, G, B to rgb(list[int])
    rgb = [int(total_r/len(pixels)), int(total_g/len(pixels)), int(total_b/len(pixels))]
    return rgb


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """
    color_average = get_average(pixels)
    # To make the distance be comparable, assign the color distance of the first pixel in pixels[list] to smallest_dist
    smallest_dist = get_pixel_dist(pixels[0], color_average[0], color_average[1], color_average[2])
    # Create an empty list to be filled up.
    best = []
    for pixel in pixels:
        color_distance = get_pixel_dist(pixel, color_average[0], color_average[1], color_average[2])
        # if the color distance in this loop is smaller than the smallest distance
        if smallest_dist >= color_distance:
            # Empty the list and assign the pixel to best[list]
            best = []
            best += pixel[0], pixel[1], pixel[2]
            # Assign the color distance in this loop to the smallest_distance
            smallest_dist = color_distance
    return best


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    ######## YOUR CODE STARTS HERE #########
    # Write code to populate image and create the 'ghost' effect
    # The first two for-loops (used with indexes i and j) are used for filling up blank image with the best pixels
    # The third loop (for-each loop) is used for create the RGB list of original images
    for i in range(width):
        for j in range(height):
            images_pixel = []
            for image in images:
                red = image.get_pixel(i, j).red
                green = image.get_pixel(i, j).green
                blue = image.get_pixel(i, j).blue
                images_pixel.append([red, green, blue])
            best_pixel = get_best_pixel(images_pixel)
            result.get_pixel(i, j).red = best_pixel[0]
            result.get_pixel(i, j).green = best_pixel[1]
            result.get_pixel(i, j).blue = best_pixel[2]

    ######## YOUR CODE ENDS HERE ###########
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
