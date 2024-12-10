import os
import subprocess
import sys

exts = (".bmp", ".jpg", ".jpeg", ".png", ".webp")

def convert(image_path, output_dir):
    print(image_path)
    name, _ = os.path.splitext(os.path.basename(image_path))
    output_path = os.path.join(output_dir, f"{name}.png")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    subprocess.call(["ffmpeg", "-i", image_path, "-vf", "crop='if(gt(iw,ih),ih,iw):if(gt(iw,ih),ih,iw)',scale=128:128", "-y", output_path])

if len(sys.argv) < 2:
    target = os.getcwd()
else:
    target = sys.argv[1]
if os.path.isdir(target):
    output_dir = os.path.join(target, "thumb")
    for f in os.listdir(target):
        if f.lower().endswith(exts):
            image_path = os.path.join(target, f)
            convert(image_path, output_dir)
elif os.path.isfile(target) and target.lower().endswith(exts):
    convert(target, os.path.join(os.path.dirname(target), "thumb"))
