import os
import cv2
import numpy as np
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.io.VideoFileClip import concatenate_videoclips
import vidmodels

def generate_script(prompt):
    """Generate a script for the video based on a given prompt."""
    response = vidmodels.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def generate_images_from_script(script, num_images):
    """Generate images using an AI image generation model."""
    frames = []
    for i in range(num_images):
        description = f"Frame {i + 1}: {script}"
        response = vidmodels.Image.create(
            prompt=description,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        image_data = download_image(image_url)
        frames.append(image_data)
    return frames

def download_image(image_url):
    """Download an image from a URL."""
    import requests
    response = requests.get(image_url)
    if response.status_code == 200:
        image_array = np.asarray(bytearray(response.content), dtype="uint8")
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    else:
        raise Exception(f"Failed to download image from {image_url}")

def generate_narration(script, language="en"):
    """Generate audio narration from the script."""
    tts = gTTS(text=script, lang=language)
    audio_file = "narration.mp3"
    tts.save(audio_file)
    return audio_file

def create_video_from_frames(frames, frame_rate):
    """Create a video file from a list of image frames."""
    height, width, _ = frames[0].shape
    video_file = "output.mp4"
    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

    for frame in frames:
        out.write(frame)
    out.release()
    return video_file

def add_audio_to_video(video_file, audio_file):
    """Combine video and audio into a single video file."""
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    video_with_audio = video.set_audio(audio)
    output_file = "final_video.mp4"
    video_with_audio.write_videofile(output_file, codec="libx264", audio_codec="aac")
    return output_file

def cleanup_temp_files(*files):
    """Remove temporary files to clean up the workspace."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def example():
    """Example function to generate the video."""
    # Prompt for script generation
    prompt = "Write a story about a journey through a futuristic city." 
    print("Generating script...")
    script = generate_script(prompt)

    # Generate images for the video
    print("Generating images...")
    num_images = 10
    frames = generate_images_from_script(script, num_images)

    # Generate narration
    print("Generating narration...")
    narration_file = generate_narration(script)

    # Create video from frames
    print("Creating video from frames...")
    video_file = create_video_from_frames(frames, frame_rate=2)

    # Combine video and narration
    print("Adding audio to video...")
    final_video = add_audio_to_video(video_file, narration_file)

    # Cleanup temporary files
    cleanup_temp_files(video_file, narration_file)

    print(f"Video created successfully: {final_video}")
    return final_video

if __name__ == "__main__":
    main()
