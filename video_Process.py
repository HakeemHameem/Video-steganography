import Stegno_image
import getpass
import cv2
import os
from subprocess import call, STDOUT
import shlex
from PIL import Image
import math

temp_folder = "frame_folder"


def split_string(s_str, count=10):
    per_c = math.ceil(len(s_str) / count)
    c_cout = 1
    out_str = ""
    split_list = []
    for s in s_str:
        out_str += s
        c_cout += 1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str = ""
            c_cout = 0
    if c_cout != 0:
        split_list.append(out_str)
    return split_list


def createTmp():
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)


def countFrames(path):
    cap = cv2.VideoCapture(path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Total frames:- ", length)
    return length


# Function to extract frames
def FrameCapture(path, op, password, message=""):
    # Path to video file
    createTmp()
    vidObj = cv2.VideoCapture(path)
    # Used as counter variable
    count = 0
    total_frame = countFrames(path)
    split_string_list = split_string(message)
    position = 0
    outputMessage = ""
    while count < total_frame:
        success, image = vidObj.read()
        if op == 1:
            cv2.imwrite(temp_folder + "\\" + "frame%d.png" % count, image)

        if op == 1:
            if position < len(split_string_list):
                print(
                    "Input in image working :- ",
                    split_string_list[position],
                )
                Stegno_image.main(
                    op,
                    password=password,
                    message=split_string_list[position],
                    img_path=temp_folder + "\\" + "frame%d.png" % count,
                )
                position += 1
                os.remove(temp_folder + "\\" + "frame%d.png" % count)

        if op == 2:
            str = Stegno_image.main(
                op,
                password=password,
                img_path=temp_folder + "\\" + "frame%d.png" % count,
            )
            if str == "Invalid data!":
                break
            outputMessage = outputMessage + str

        count += 1

    if op == 1:
        makeVideoFromFrame()
        # To delete frames

        # images = [img for img in os.listdir("frame_folder") if img.endswith(".png")]
        # for img in images:
        #     os.remove(os.path.join("frame_folder", img))

    if op == 2:
        print("Message is :- ", outputMessage)


def makeVideoFromFrame():
    images = [img for img in os.listdir("frame_folder") if img.endswith(".png")]
    for img in images:
        if img.count("-enc") == 1:
            newImgName = img.split("-")[0] + ".png"
            os.rename("frame_folder//" + img, "frame_folder//" + newImgName)

    cmd = shlex.split(
        "ffmpeg -framerate 29.92 -i frame_folder/frame%01d.png -vcodec libx264 -profile:v high444 -crf 0 -preset ultrafast output.mov"
    )
    call(
        cmd,
        stdout=open(os.devnull, "w"),
        stderr=STDOUT,
        shell=True,
    )


def main():
    print("In what you want to hide the data 1 for image and 2 for video Using e-LSB\n")
    print(">>")
    choice = int(input())

    if choice == 1:
        text = "Image"
    else:
        text = "Video"

    print("Choose one: ")
    op = int(input("1. Encode\n2. Decode\n>>"))

    if op == 1:
        print(f"{text} path (with extension): ")
        img = input(">>")

        print("Message to be hidden: ")
        message = input(">>")
        password = ""

        print("Password to encrypt (leave empty if you want no password): ")
        password = getpass.getpass(">>")

        if password != "":
            print("Re-enter Password: ")
            confirm_password = getpass.getpass(">>")
            if password != confirm_password:
                print("Passwords don't match try again ")
                return

        cmd = shlex.split(f"ffmpeg -i {img} -q:a 0 -map a sample.mp3")
        call(
            cmd,
            stdout=open(os.devnull, "w"),
            stderr=STDOUT,
            shell=True,
        )

        cmd = shlex.split(f"ffmpeg -i {img} -q:a 0 -map a sample.mp3 -y")
        call(
            cmd,
            stdout=open(os.devnull, "w"),
            stderr=STDOUT,
            shell=True,
        )

        FrameCapture(img, op, password, message)

        cmd = shlex.split(
            "ffmpeg -i output.mov -i output.mov -i sample.mp3 -codec copy final.mov -y"
        )
        call(
            cmd,
            stdout=open(os.devnull, "w"),
            stderr=STDOUT,
            shell=True,
        )
        os.remove("output.mov")
        os.remove("sample.mp3")

    elif op == 2:
        print(f"{text} path (with extension): ")
        img = input(">>")

        print("Enter password (leave empty if no password): ")
        password = getpass.getpass(">>")
        FrameCapture(img, op, password)


if __name__ == "__main__":

    print(
        "VIDEOHIDE allows you to hide texts inside an video. You can also protect these texts with a password using AES-256."
    )
    print()
    main()

# -----------------------
