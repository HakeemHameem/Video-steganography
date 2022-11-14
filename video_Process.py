import Stegno_image
import getpass
import cv2
import os
from subprocess import call, STDOUT
import shlex
from PIL import Image

temp_folder = "frame_folder"
frame_count = [1]


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
    while count < total_frame:
        success, image = vidObj.read()
        if op == 1:
            cv2.imwrite(temp_folder + "\\" + "frame%d.png" % count, image)

        if op == 1:
            if count in frame_count:
                Stegno_image.main(
                    op,
                    password=password,
                    message=message,
                    img_path=temp_folder + "\\" + "frame%d.png" % count,
                )
                os.remove(temp_folder + "\\" + "frame%d.png" % count)

        if op == 2 and count in frame_count:
            Stegno_image.main(
                op,
                password=password,
                img_path=temp_folder + "\\" + "frame%d.png" % count,
            )

        count += 1

    if op == 1:
        makeVideoFromFrame()
        # To delete frames

        # images = [img for img in os.listdir("frame_folder") if img.endswith(".png")]
        # for img in images:
        #     os.remove(os.path.join("frame_folder", img))


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

    # image_folder = temp_folder
    # video_name = "video.avi"

    # images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    # frame = cv2.imread(os.path.join(image_folder, images[0]))
    # height, width, layers = frame.shape

    # video = cv2.VideoWriter(video_name, 0, 1, (width, height))
    # video.set(cv2.CAP_PROP_FPS, 30)
    # for image in images:
    #     video.write(cv2.imread(os.path.join(image_folder, image)))

    # cv2.destroyAllWindows()
    # video.release()


def main():
    print("Choose one: ")
    op = int(input("1. Encode\n2. Decode\n>>"))

    if op == 1:
        print("Video path (with extension): ")
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
        print("Image path (with extension): ")
        img = input(">>")

        print("Enter password (leave empty if no password): ")
        password = getpass.getpass(">>")
        FrameCapture(img, op, password)


if __name__ == "__main__":

    print(
        "IMGHIDE allows you to hide texts inside an image. You can also protect these texts with a password using AES-256."
    )
    print()
    main()

# -----------------------
