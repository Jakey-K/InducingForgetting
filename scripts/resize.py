from PIL import Image
import os
from pathlib import Path

folder_path = str(Path(__file__).resolve().parents[1] / "images")

# there is 100 images in the folder
for i in range(1, 111):
    file_name = f"{i}.jpg"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        # Open, compute size, create resized image
        with Image.open(file_path) as img:
            width, height = img.size 

            # I set all the images to the same height (400px)
            # so that when the participant goes through the
            # test feedback loop or tnt, it looks less weird.
            # But, I did not change the width, as these images
            # are not the same aspect ratio, and for some of
            # them, a universal width would augment them to
            # the point they don't look like a normal image.
            new_height = 400 
            new_width = int((new_height / height) * width) 

            resized_img = img.resize((new_width, new_height)) 

        # Save AFTER closing the original file handle (Windows-safe)
        resized_img.save(file_path)
        print(f"Resized {file_name} to {new_width}x{new_height}")
    else:
        print(f"{file_name} not found.")
