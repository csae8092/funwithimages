import glob
import os
import shutil
from slugify import slugify

from rembg import remove
from PIL import Image
from tqdm import tqdm

INPUT_DIR = "/home/csae8092/Documents/palm/tagebuch_palm"
INPUT_IMG_EXT = "jpg"
OUTPUT_DIR = "/home/csae8092/Documents/palm/processed"

shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = sorted(glob.glob(f"{INPUT_DIR}/*.{INPUT_IMG_EXT}"))
print(
    f"going to process >{len(files)}< images from >{INPUT_DIR}< with extension: >{INPUT_IMG_EXT}<"
)

for x in tqdm(files):
    new_name = x.replace(INPUT_DIR, OUTPUT_DIR)
    _, tail = os.path.split(x.replace(f".{INPUT_IMG_EXT}", ""))
    slug_name = f"{slugify(tail)}"
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
