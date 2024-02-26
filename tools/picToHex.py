#pip install pillow
from PIL import Image
from os import path

filePath = input("Enter the path of the file: ")
if not path.exists(filePath):
    print("File not found...")
    print("Use imageInput.png")
    filePath = path.join(path.dirname(__file__), "imageInput.png")

img = Image.open(filePath).convert('1')
width, height = img.size

print(f"Size {width}x{height}")

print("Hex format...")
print("[", end="")
for y in range(height):
    numByte = 0
    for x in range(width):
        calPos = width - x - 1
        numByte <<= 1
        if img.getpixel((x, y)) != 0:
            numByte += 1
        
        if (calPos) % 32 == 0:
            print(f"0x{numByte:08X},", end=" ")
            numByte = 0
print("]")
