import math
import datetime
import os
from PIL import Image, ImageColor

folder_path = r"C:\Users\1isai\Desktop\chromarithmography" #REPLACE WITH THE LOCATION OF THE PROGRAM!

color_path = "12tone.hex" #The first color is the "separator", it will be the predominant color of the image
custom_message = 1 #Selects the data below automatically when converting numbers to colors, disable to type manually
data = "69 118 101 114 121 111 110 101 32 104 97 115 32 116 104 101 32 114 105 103 104 116 32 116 111 32 102 114 101 101 100 111 109 32 111 102 32 111 112 105 110 105 111 110 32 97 110 100 32 101 120 112 114 101 115 115 105 111 110 59 32 116 104 105 115 32 114 105 103 104 116 32 105 110 99 108 117 100 101 115 32 102 114 101 101 100 111 109 32 116 111 32 104 111 108 100 32 111 112 105 110 105 111 110 115 32 119 105 116 104 111 117 116 32 105 110 116 101 114 102 101 114 101 110 99 101 32 97 110 100 32 116 111 32 115 101 101 107 44 32 114 101 99 101 105 118 101 32 97 110 100 32 105 109 112 97 114 116 32 105 110 102 111 114 109 97 116 105 111 110 32 97 110 100 32 105 100 101 97 115 32 116 104 114 111 117 103 104 32 97 110 121 32 109 101 100 105 97 32 97 110 100 32 114 101 103 97 114 100 108 101 115 115 32 111 102 32 102 114 111 110 116 105 101 114 115 "

cube = 1 #Outputs the image in cube form, disable for a long strip of colorful pixels
debug = 0 #Prints useful values for developers, but slows down the entire program
redundancy = 1 #Adds extra "separator" pixels, disable when converting images or for smaller size

#Do not touch these
color_list = []
number_list = []
integer_list = []

if custom_message == 1:
    message = [int(x) for x in data.split()]
else: 
    message = []

color_file = os.path.join(folder_path, color_path)
with open(color_file, "r") as file:
    color_palette = [line.rstrip() for line in file]
color_palette = ["#" + line for line in color_palette]

user_num = 0
color_size = len(color_palette) - 1

def rgb_to_hex(rgb_tuple):
    return "#{:02x}{:02x}{:02x}".format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]).upper()

color_palette = [c.upper() for c in color_palette]


def numbers_to_colors():
    while True:
        user_input = input("Input numbers")

        if not user_input:
            break

        try:
            user_num = int(user_input)
            number_list.append(user_num)
        
        except ValueError:
            print("Invalid input")

    if custom_message == 1:
        for i, item in enumerate(message):
            Index_Num = math.floor(item/color_size)+1
            Number = item - ((Index_Num - 1) * color_size)
            if (Number >= Index_Num):
                Number += 1 

            color_list.append(0)
            color_list.append(Index_Num)
            if redundancy == 0:
                if Number != 0:
                    color_list.append(Number)
            else:
                color_list.append(Number)

            if (Number >= Index_Num):
                Number -= 1
    else:
        for i, item in enumerate(number_list):
            Index_Num = math.floor(item/color_size)+1
            Number = item - (Index_Num - 1) * color_size
            if (Number >= Index_Num):
                Number += 1 

            color_list.append(0)
            color_list.append(Index_Num)
            if redundancy == 0:
                if Number != 0:
                    color_list.append(Number)
            else:
                color_list.append(Number)

            if (Number >= Index_Num):
                Number -= 1

    if debug == 1:
        print(color_list)
        print(number_list)
        print(user_num)

    if cube == 0:
        img = Image.new ("RGB", (1, len(color_list)), color = "black")
        for i, item in enumerate(color_list):
            if item > color_size: item = 0
            img.putpixel((0, i), ImageColor.getrgb(color_palette[item])) 

    else:
        dim = math.ceil(math.sqrt(len(color_list)))
        img = Image.new ("RGB", (dim, dim), color = ImageColor.getrgb(color_palette[color_list[-1]]))

        for i, item in enumerate(color_list):
            col = i // dim
            row = i % dim

            if item > color_size: item = 0
            img.putpixel((col, row), ImageColor.getrgb(color_palette[item])) 

    img.show()

def colors_to_numbers():
    last_hex = None

    img = input("Input image.")
    img_data = Image.open(img).convert("RGB")

    width, height = img_data.size

    if cube == 0:
        for i in range(height):
            pixel_color = img_data.getpixel((0, i))
            pixel_hex = rgb_to_hex(pixel_color)

            if pixel_hex not in color_palette:
                print("⚠ Unknown color:", pixel_hex)
                continue

            if debug == 1:
                print(pixel_color)
                print(pixel_hex)

            if (pixel_hex != last_hex):
                color_list.append(color_palette.index(pixel_hex))
            last_hex = pixel_hex

    else:
        for x in range(width):
            for y in range(height):
                pixel_color = img_data.getpixel((x, y))
                pixel_hex = rgb_to_hex(pixel_color)

                if pixel_hex not in color_palette:
                    print("⚠ Unknown color:", pixel_hex)
                    continue

                if debug == 1:
                    print(pixel_color)
                    print(pixel_hex)

                if (pixel_hex != last_hex):
                    color_list.append(color_palette.index(pixel_hex))
                last_hex = pixel_hex

    if debug == 1:
        print(color_list)
    
    for i in range(len(color_list)-1):
        integer_list = []

        if color_list[i] == 0 and i + 2 < len(color_list):
        
            Index_Num = color_list[i+1]
            place = i + 2

            if color_list[place] != 0:

                val = color_list[place]
                if val >= Index_Num:
                    val -= 1
                integer_list.append(val)
            
            user_num = (Index_Num - 1) * color_size + sum(integer_list)
            number_list.append(user_num)

    if debug == 1:
        print(number_list)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"decoded_{timestamp}.txt"
    full_path = os.path.join(folder_path, filename)

    output_data = " ".join(map(str, number_list))
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(output_data)

    print(f"File saved successfully at: {full_path}")

#Execution
if __name__ == "__main__":
    select = input("0 for number to colors. 1 for colors to number.")

    if select.strip() == "0":
        numbers_to_colors()
    else:
        colors_to_numbers()