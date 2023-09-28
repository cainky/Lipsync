import gdown

checkpoints_directory = "/backend/wav2lip-hq/checkpoints/"

urls = {
    "wav2lip_gan.pth": "10Iu05Modfti3pDbxCFPnofmfVlbkvrCm",
    "face_segmentation.pth": "154JgKpzCPW82qINcVieuPH3fZ2e0P812",
    "esrgan_max.pth": "1e5LT83YckB5wFKXWV4cWOPkVRnCDmvwQ",
}

for name, id in urls.items():
    url = f"https://drive.google.com/uc?id={id}"
    output = checkpoints_directory + name
    gdown.download(url, output, quiet=False)
    print(f"Loaded {name}")
