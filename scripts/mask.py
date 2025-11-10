import os
import random
from PIL import Image

def createMasks(inputFolder="images", outputFolder="masks", blockSize=10):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    imageFiles = [f for f in os.listdir(inputFolder) if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))]

    for imageFile in imageFiles:
        imgPath = os.path.join(inputFolder, imageFile)
        img = Image.open(imgPath)
        img = img.convert("RGB") # incase its cmyk

        # resizes so that the image is a multiple of blocksize
        # despite each imagee being 400px tall after resizing,
        # still need this as it doesnt conform the images
        # to a uniform aspect ratio
        width, height = img.size
        xBlocks = width // blockSize
        yBlocks = height // blockSize
        newWidth = xBlocks * blockSize
        newHeight = yBlocks * blockSize
        img = img.resize((newWidth, newHeight))

        blocks = []

        # divides images into these blocks
        for y in range(0, newHeight, blockSize):
            for x in range(0, newWidth, blockSize):
                box = (x, y, x + blockSize, y + blockSize)
                block = img.crop(box)
                blocks.append(block)

        # by shuffling these blocks we get our scrambled image
        random.shuffle(blocks)

        # creates a blank image and puts the shuffled blocks in it (our mask)
        scrambledImg = Image.new("RGB", (newWidth, newHeight))
        index = 0
        for y in range(0, newHeight, blockSize):
            for x in range(0, newWidth, blockSize):
                scrambledImg.paste(blocks[index], (x, y))
                index += 1

        maskFilename = f"mask_{imageFile}"
        scrambledImg.save(os.path.join(outputFolder, maskFilename))

        print("file", imageFile, "saved as", maskFilename)

if __name__ == "__main__":
    createMasks()