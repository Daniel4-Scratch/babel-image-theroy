from PIL import Image
import numpy as np
import os
import easydebugger as ed

im = Image.new("RGB", (100, 100), "white")
width, height = im.size

if not os.path.exists("./output"):
    os.makedirs("./output")

amount = int(input("Enter the amount of images to generate: "))

previous = 0

if os.path.exists("./output/!data.txt"):
    f = open("./output/!data.txt", "r")
    previous = int(f.read())
    f.close()

f = open("./output/!data.txt", "w")
ed.start_timer("creating_images")
for i in range(amount):
    for y in range(height):
        for x in range(width):
            im.putpixel((x, y), tuple(np.random.choice(range(256), size=3)))

    f.seek(0)
    f.write(str(i+previous))

    im.save("./output/image"+str(i+previous)+".jpg")
f.close()
ed.end_timer("creating_images")

def average_images_from_folder(folder_path, output_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif'))]
    image_paths = [os.path.join(folder_path, img) for img in image_files]
    
    if not image_paths:
        raise ValueError("No image files found in the specified folder.")
    
    images = [Image.open(path).convert('RGB') for path in image_paths]
    arrays = [np.array(img, dtype=np.float32) for img in images]
    
    width, height = images[0].size
    for img in images:
        if img.size != (width, height):
            raise ValueError("All images must have the same dimensions.")
    
    stacked_arrays = np.stack(arrays, axis=0)
    average_array = np.mean(stacked_arrays, axis=0).astype(np.uint8)
    average_image = Image.fromarray(average_array)
    average_image.save(output_path)

average_images_from_folder("./output", "./output/!average_image.jpg")

ed.success("Images created successfully @ ./output")