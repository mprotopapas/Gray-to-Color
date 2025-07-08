# Libs
import cv2
import numpy as np
import os
import subprocess

def convert_yuv_to_grayscale(yuv_file, width, height, fps, duration, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Calculate total frames based on duration and fps
    total_frames = int(fps * duration)

    # Open the YUV file
    with open(yuv_file, 'rb') as file:
        for frame_number in range(total_frames):

            # Calculate the size of one frame in bytes (YUV420)
            frame_size = int(width * height * 1.5)  # YUV420 has 1.5 bytes per pixel

            # Seek to the start of the current frame
            file.seek(frame_number * frame_size)

            # Read Y component for the current frame
            Y = np.frombuffer(file.read(int(width * height)), dtype=np.uint8).reshape((height, width))

            # Create a grayscale image using only the Y component
            grayscale_frame = Y

            # Save the grayscale image
            output_filename = f"{output_folder}/frame_{frame_number + 1}.png"
            cv2.imwrite(output_filename, grayscale_frame)

            print(f"Frame {frame_number + 1} processed and saved as {output_filename}") # number +1 to display the correct value

def create_yuv_video(input_folder, output_video_path, resolution=(1920, 1080), frame_rate=120):

    # List all images in the input folder and sort them numerically
    input_images = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')],
                          key=lambda x: int(x.split('_')[1].split('.')[0]))

    # Initialize output YUV file
    output_file = open(output_video_path, 'wb')

    total_frames = len(input_images) # Get the number of the total frames 

    # Calculates the size of one frame in bytes (YUV420)
    frame_size = int(resolution[0] * resolution[1] * 1.5)  # YUV420 has 1.5 bytes per pixel

    # Write each frame to the YUV file
    for i in range(total_frames):
        image_name = input_images[i]  # Use the original image name
        image_path = os.path.join(input_folder, image_name)
        frame = cv2.imread(image_path)

        # Resize frame to match resolution if needed
        frame = cv2.resize(frame, resolution)

        # Convert the frame to YUV format
        frame_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)

        # Write Y, U, and V components to the YUV file
        output_file.write(frame_yuv.tobytes())

    # Close the output YUV file
    output_file.close()

def colorize_image(input_path, output_path):

    # Run the colorization command using the external tool
    colorization_command = [
        'python3', 'demo_release.py', '-i', input_path, '-o', output_path
    ]
    subprocess.run(colorization_command)

def colorize_images(input_folder, output_folder):
    # Ensure the output folder existsi
    os.makedirs(output_folder, exist_ok=True)

    # List all images in the input folder
    input_images = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')])

    for image in input_images:
        input_path = os.path.join(input_folder, image)
        output_path = os.path.join(output_folder, image)

        # Run colorization for each image from demo
        colorize_image(input_path, output_path)


if __name__ == "__main__":
    yuv_file = input("Write your video with .yuv in the end: ") # Lets the user input the YUV video they wish to color
    width, height = 1920, 1080 # Sets the value to 2k
    fps = 120
    duration = 5
    output_folder = "output_frames" # The output folder for each gray frame

    convert_yuv_to_grayscale(yuv_file, width, height, fps, duration, output_folder)

    input_folder = "output_frames"
    output_folder = "colorized_frames" # Change the output folder for the colorized one
    output_video_path = "colored.yuv"

    # Step 1: Colorize the images using the demo_release script
    colorize_images(input_folder, output_folder)

    # Step 2: Create a video from the colorized images without resizing and ensuring numerical order to correctly recreate the video
    create_yuv_video(output_folder, output_video_path, resolution=(1920, 1080), frame_rate=120)

    print("Your Video has been created successfully!")
