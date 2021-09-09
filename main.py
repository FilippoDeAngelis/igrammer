import glob
import sys, getopt
from PIL import Image, ImageDraw

# read all the picture files

# stretch them out to a 1:1 ratio

# add a semi transparent white background

# super impose the original picture

def get_all_pictures_in_current_folder():
    # returns list of filenames
    extensions = ["jpg", "jpeg", "png"]
    files = []
    # try and fill the files list until it fills
    for extension in extensions:
        files = glob.glob("*." + extension)
        if files:
            # TODO save the correct file extension, we'll need it later
            break
    else:
        raise Exception("No files found")

    return files

def stretch_pictures(picture_names):
    # takes list of filenames, returns Image objects
    resized_images = []
    for picture_name in picture_names:
        image = Image.open(picture_name)
        biggest_dimension = max(image.size)
        # make the image a square with side of biggest dimension
        resized_image = image.resize((biggest_dimension, biggest_dimension))
        resized_images.append(resized_image)
    return resized_images

def add_transparent_layer(images, opacity):
    # takes Image list, returns Image list
    color = (255, 255, 255, opacity if opacity is not None else 204)   #make opacity 204 by default

    output_images = []
    counter = 0

    for image in images:
        # create the white rectangle image
        white_rectangle = Image.new("RGBA", image.size, color)

        # add it to the original image
        output = Image.alpha_composite(image.convert("RGBA"), white_rectangle)
        output_images.append(output)
        counter += 1

    return output_images

def filenames_to_images(filenames):
    output = []
    for name in filenames:
        output.append(Image.open(name))

    return output

def super_impose_pictures(originals, whiteneds):
    # takes two list of images, returns one list
    output = []
    for i in range(len(originals)):
        original = originals[i]
        whitened = whiteneds[i]
        or_x, or_y = original.size
        wh_x, wh_y = whitened.size
        offset = ((wh_x - or_x) // 2, (wh_y - or_y) // 2)
        whitened.paste(original, offset)
        output.append(whitened)

    return output

def save_pictures(images):
    counter = 0
    for im in images:
        im.save(str(counter) + ".png")
        counter += 1

if __name__ == "__main__":
    opacity = None

    try:
        # sys.argv needs a [1:] because getopt doesn't work if you leave the script name as an argument
        options, args = getopt.getopt(sys.argv[1:], "o:", ["opacity="])
    except getopt.GetoptError:
        print("getopt error") #todo add tutorial
        pass

    for option, argument in options:
        if option in ["-o", "--opacity"]:  #opacity can be 0-255
            opacity = int(argument)


    pictures = get_all_pictures_in_current_folder()
    stretched_pictures = stretch_pictures(pictures)
    whitened_pictures = add_transparent_layer(stretched_pictures, opacity)
    final_pictures = super_impose_pictures(filenames_to_images(pictures), whitened_pictures)


    save_pictures(final_pictures)
