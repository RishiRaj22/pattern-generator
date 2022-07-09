# Tiled image generator

This is a script to generate tiled images that have continuity between different tiles.

## Pre-requisites
* Python 3
* [Pillow library](https://pillow.readthedocs.io/en/stable/index.html)

## How to install?

* Make sure you have Python & the pillow library installed on your system. Check the link from pre-requisites for more details.
* Run `python generator.py` and voila, you'll find the `generated_image.png` in the img folder.

# How to use?

This script can be used to create seamless patterns which can continue across various tiles.
For this, we take 6 images as input and can be found in `img` folder with the following names:-
1. one_side.png: An image with some feature along the top boundary of the image.
1. two_sides.png: An image with some feature along the top and right boundaries of the image.
1. three_sides.png: An image with some feature along the top and right boundaries of the image.
1. two_opposite_sides.png: An image with some feature along the top and bottom boundaries of the image.
1. all_sides.png: An image with some feature along all the boundaries of the image.
1. empty.png: An image with no features along any of the image's boundaries.

You can check the sample images present in the img folder which can be used to generate images similar to `img/generated.png`. You can modify the images here following these parameters to generate custom patterns.
You can modify the number of tiles in image by changing the num_tiles variable's value in `generator.py`.

# Sample image
![alt text](https://github.com/rishiraj22/pattern-generator/blob/main/img/generated.png?raw=true)
