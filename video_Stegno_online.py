from stegano import lsb
from os.path import isfile, join

import time  # install time ,opencv,numpy modules
import cv2
import numpy as np
import math
import os
import shutil
from subprocess import call, STDOUT
import shlex


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


def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    print("[INFO] tmp directory is created")
    cmd = shlex.split("ffmpeg -i t.mp4 -vf fps=29.92 tmp/%d.png")
    call(
        cmd,
        stdout=open(os.devnull, "w"),
        stderr=STDOUT,
        shell=True,
    )


def encode_string(input_string, root="./tmp/"):
    split_string_list = split_string(input_string)
    for i in range(0, len(split_string_list)):
        f_name = "{}{}.png".format(root, i + 1)
        secret_enc = lsb.hide(f_name, split_string_list[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name, split_string_list[i]))


def decode_string(video):
    frame_extraction(video)
    secret = []
    root = "tmp/"
    for i in range(0, len(os.listdir(root))):
        f_name = "{}{}.png".format(root, i + 1)
        secret_dec = lsb.reveal(f_name)
        print(i, secret_dec)
        if secret_dec == None:
            break
        secret.append(secret_dec)

    print("".join([i for i in secret]))
    clean_tmp()


def clean_tmp(path="./tmp"):
    # if os.path.exists(path):
    #     shutil.rmtree(path)
    #     print("[INFO] tmp files are cleaned up")
    print("clean up")


def main():
    input_string = input("Enter the input string : ")
    f_name = input("enter the name of video: ")
    frame_extraction(f_name)
    call(
        ["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],
        stdout=open(os.devnull, "w"),
        stderr=STDOUT,
        shell=True,
    )

    encode_string(input_string)
    cmd = shlex.split(
        "ffmpeg -framerate 29.92 -i tmp/%d.png -vcodec libx264 -profile:v high444 -crf 0 -preset ultrafast tmp/video.avi"
    )
    call(
        cmd,
        stdout=open(os.devnull, "w"),
        stderr=STDOUT,
        shell=True,
    )

    call(
        [
            "ffmpeg",
            "-i",
            "tmp/video.avi",
            "-i",
            "tmp/audio.mp3",
            "-codec",
            "copy",
            "video.avi",
            "-y",
        ],
        stdout=open(os.devnull, "w"),
        stderr=STDOUT,
        shell=True,
    )
    clean_tmp()


if __name__ == "__main__":
    while True:
        print("1.Hide a message in video 2.Reveal the secret from video")
        print("any other value to exit")
        choice = input()
        if choice == "1":
            main()
        elif choice == "2":
            decode_string(input("enter the name of video with extension "))
        else:
            break
