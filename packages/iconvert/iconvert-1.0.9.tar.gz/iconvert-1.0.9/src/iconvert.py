# -*- coding: utf-8 -*-

import sys
import os
from PIL.Image import core as _imaging
from PIL import Image
# ANSI color escape sequences
RED = '\033[91m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
MAGENTA = '\033[35m'
RESET = '\033[0m'
BRIGHT_GREEN = '\033[92m'
DARK_GRAY = '\033[90m'
WASHED_BLUE = '\033[94m'
def is_image_file(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        img.close()
        return True
    except (IOError, SyntaxError):
        return False

def get_available_filename(export_path, custom_name):
    count = 0
    base_name, extension = os.path.splitext(custom_name)
    while True:
        count_str = f"_{count:03d}" if count > 0 else ""
        file_name = f"{base_name}{count_str}{extension}.ico"
        file_path = os.path.join(export_path, file_name)
        if not os.path.exists(file_path):
            return file_name
        count += 1

def is_compliant_image(img):
    # Define the compliant sizes for ICO files
    compliant_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]  # Add more if needed

    # Check if the image dimensions and mode match ICO standards
    if img.mode not in ["RGB", "RGBA"]:
        print(RED + "Image mode is not compatible (RGB or RGBA required)." + RESET)
        return False
    if img.size not in compliant_sizes:
        print(RED + f"Image size {img.size} is not compliant with ICO file standards." + RESET)
        print(RED + f"Required sizes: {compliant_sizes}" + RESET)
        return False

    return True

def adjust_image(img):
    try_sizes = [(256, 256), (48, 48), (32, 32), (16, 16)]  # Start from largest size
    
    for size in try_sizes:
        resized_img = img.resize(size, Image.LANCZOS)  # Resize directly without thumbnail
        if resized_img.mode != 'RGB':
            resized_img = resized_img.convert('RGB')
        
        if is_compliant_image(resized_img):
            return resized_img

    return None
def convert_to_image(input_path, export_path, custom_name):
    try:
        # Check if the output directory exists, create it if not
        os.makedirs(export_path, exist_ok=True)
        
        # Open the image using PIL
        img = Image.open(input_path)
        
        # Check if the image meets ICO standards
        if not is_image_file(input_path):
            print(RED + "Not a valid image file." + RESET)
            return

        adjusted_img = adjust_image(img)
        
        if adjusted_img:
            export_file = get_available_filename(export_path, custom_name)
            adjusted_img.save(os.path.join(export_path, export_file), format="PNG")  # Save as PNG instead of ICO

            if adjusted_img.size != img.size:
                print(f"{RED}WARNING: {YELLOW}Image was adjusted to size: {adjusted_img.size}" + RESET)

            print(f">_: {GREEN}SUCCESS{RESET}")
            print(f"{GREEN}Exported: {RESET}{custom_name}")
            print(f"{GREEN}To: {RESET}{export_path}\{export_file}{RESET}")
        else:
            print(RED + "Image could not be transformed to a compliant format." + RESET)
    except IOError:
        print(RED + "Cannot convert image." + RESET)
def print_usage():
    print(">_:  " + WASHED_BLUE + f"Iconvert{RESET} -{RESET} Convert images to .ico format for icon use in Windows" + RESET)
    print("Usage:" + RESET)
    print(f"     {WASHED_BLUE}iconvert {RESET}<{YELLOW}input path{RESET}> <{YELLOW}export path{RESET}> <{YELLOW}custom name{RESET}>")
    print("Example:" + RESET)
    print(f"     {WASHED_BLUE}iconvert {RESET}{BRIGHT_GREEN}$HOME{RESET}\{YELLOW}Pictures{RESET}\{YELLOW}Example.png {BRIGHT_GREEN}$HOME{RESET}\{YELLOW}Pictures MyIconName")
    print(f"        {DARK_GRAY}This will export the image {BRIGHT_GREEN}$HOME{RESET}\{YELLOW}Pictures{RESET}\{YELLOW}Example.png {DARK_GRAY}as {YELLOW}MyIconName{RESET}.ico {RESET}to the Pictures folder.")
def main():
    if len(sys.argv) != 4:
        print_usage()
    else:
        input_path = sys.argv[1]
        export_path = sys.argv[2]
        custom_name = sys.argv[3]
        convert_to_image(input_path, export_path, custom_name)

if __name__ == "__main__":
    main()