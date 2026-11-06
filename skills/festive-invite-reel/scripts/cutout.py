#!/usr/bin/env python3
"""Cut a white-background sticker sheet into one transparent PNG per object.

    python -I cutout.py <sheet.png> <out_dir> [min_area=3000] [dilate=14]

rembg (isnet-general-use) mask + a white-key near each object (keeps thin sparks), then splits the sheet into
connected components (dilate groups sparks with their object). Outputs <sheet>_NN.png and prints (index, x, y, w, h)
so you can rename by position.
"""
import sys, os, numpy as np
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage
sess = new_session("isnet-general-use")
src, outdir, minarea, dil = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
os.makedirs(outdir, exist_ok=True)
im = Image.open(src).convert("RGB")
cut = remove(im, session=sess, post_process_mask=True)
a = np.array(cut)
# also keep saturated/dark pixels rembg dropped (sparks): distance from white
rgb = np.array(im).astype(int)
dist = np.abs(255-rgb).max(2)
key = np.clip((dist-18)*6,0,255)
alpha = np.maximum(a[...,3], np.where(ndimage.binary_dilation(a[...,3]>40, iterations=60), key, 0)).astype(np.uint8)
a[...,3] = alpha
m = ndimage.binary_dilation(alpha>30, iterations=dil)
lab, n = ndimage.label(m)
objs = ndimage.find_objects(lab)
k=0
base=os.path.splitext(os.path.basename(src))[0]
info=[]
for i,sl in enumerate(objs):
    area=(lab[sl]==i+1).sum()
    if area<minarea: continue
    y0,y1,x0,x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
    crop = a[y0:y1, x0:x1].copy()
    crop[...,3] = crop[...,3] * (lab[y0:y1,x0:x1]==i+1)
    Image.fromarray(crop).save(f"{outdir}/{base}_{k:02d}.png"); info.append((k,x0,y0,x1-x0,y1-y0)); k+=1
print(base, info)
