import glob
import os
import shutil
from slugify import slugify

from rembg import remove
from PIL import Image
from tqdm import tqdm

INPUT_DIR = "./sample_in"
INPUT_IMG_EXT = "jpg"
OUTPUT_DIR = "./sample_out"
IMG_PREFIX = "palm__"

shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = sorted(glob.glob(f"{INPUT_DIR}/*.{INPUT_IMG_EXT}"))
print(f"going to process >{len(files)}< images from >{INPUT_DIR}< with extension: >{INPUT_IMG_EXT}<")

for x in tqdm(files):
    new_name = x.replace(INPUT_DIR, OUTPUT_DIR)
    _, tail = os.path.split(x.replace(f".{INPUT_IMG_EXT}" , ""))
    slug_name = f"{IMG_PREFIX}{slugify(tail)}"
    new_name = new_name.replace(tail, slug_name).replace(f".{INPUT_IMG_EXT}", ".png")
    input = Image.open(x)
    output = remove(input)
    output.save(new_name)
    im = Image.open(new_name)
    alpha = im.getchannel('A')
    bbox  = alpha.getbbox()
    res = im.crop(bbox)
    res.save(new_name)
    print(f"done converting {x} into {new_name}")



# # Load image
# im = Image.open('output/002_(02-03).png')

# # Extract alpha channel as new Image and get its bounding box
# alpha = im.getchannel('A')
# bbox  = alpha.getbbox()
# print(bbox)

# # Apply bounding box to original image
# res = im.crop(bbox)
# res.save('result.png')



# # from PIL import Image
# # import numpy as np
# # from os import listdir

# # def crop(png_image_name):
# #     pil_image = Image.open(png_image_name)
# #     np_array = np.array(pil_image)
# #     blank_px = [0, 0, 0, 0]
# #     mask = np_array != blank_px
# #     coords = np.argwhere(mask)
# #     x0, y0, z0 = coords.min(axis=0)
# #     x1, y1, z1 = coords.max(axis=0) + 1
# #     cropped_box = np_array[x0:x1, y0:y1, z0:z1]
# #     pil_image = Image.fromarray(cropped_box, 'RGBA')
# #     print(pil_image.width, pil_image.height)
# #     pil_image.save("test_cropped1.png")
# #     print("test_cropped1.png")

# # crop('palm/010_4-5.png')

# # import numpy as np
# # from PIL import Image

# # def bbox(im):
# #     a = np.array(im)[:,:,:3]  # keep RGB only
# #     m = np.any(a != [255, 255, 255], axis=2)
# #     coords = np.argwhere(m)
# #     print(coords)
# #     y0, x0, y1, x1 = *np.min(coords, axis=0), *np.max(coords, axis=0)
# #     print(x0, y0)
# #     return (x0, y0, x1+1, y1+1)

# # im = Image.open('palm/010_4-5.png')
# # print(bbox(im))  # (33, 12, 223, 80)
# # im2 = im.crop(bbox(im))
# # im2.save('test_cropped.png')


# # import glob
# # from tqdm import tqdm
# # from PIL import Image


# # for x in glob.glob('./palm/*.png'):
# #     im = Image.open(x)
# #     im.size  # (364, 471)
# #     im.getbbox()  # (64, 89, 278, 267)
# #     im2 = im.crop(im.getbbox())
# #     im2.size  # (214, 178)
# #     im2.save(x.replace('.png', 'aaa.png'))