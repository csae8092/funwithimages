import glob
import os
import shutil
from slugify import slugify

from rembg import remove
from PIL import Image
from tqdm import tqdm

INPUT_DIR = "/mnt/acdh_resources/container/R_wkfm_palm_21464/tagebuch_palm_orig_as_transmitted"
INPUT_IMG_EXT = "jpg"
OUTPUT_DIR = "/mnt/acdh_resources/container/R_wkfm_palm_21464/tagebuch_processed"
IMG_PREFIX = "palm__"

shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = sorted(glob.glob(f"{INPUT_DIR}/*.{INPUT_IMG_EXT}"))
print(
    f"going to process >{len(files)}< images from >{INPUT_DIR}< with extension: >{INPUT_IMG_EXT}<"
)

for x in tqdm(files):
    new_name = x.replace(INPUT_DIR, OUTPUT_DIR)
    _, tail = os.path.split(x.replace(f".{INPUT_IMG_EXT}", ""))
    slug_name = f"{IMG_PREFIX}{slugify(tail)}"
    new_name = new_name.replace(tail, slug_name).replace(f".{INPUT_IMG_EXT}", ".png")
    input = Image.open(x)
    output = remove(input)
    output.save(new_name)
    im = Image.open(new_name)
    alpha = im.getchannel("A")
    alpha = alpha.point(lambda i: 0 if i < 150 else i)
    bbox = alpha.getbbox()
    res = im.crop(bbox)
    res.save(new_name)
    print(f"done converting {x} into {new_name}")
