from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/start_stream/<stream_key>")
def start_stream(stream_key):
    # Insert your FFmpeg command here
    cmd = [
        'ffmpeg',
        '-f', 'x11grab',
        '-r', '30',
        '-s', '1920x1080',
        '-i', ':0.0',
        '-f', 'v4l2',
        '-video_size', '640x480',
        '-i', '/dev/video0',
        '-f', 'alsa',
        '-ac', '1',
        '-i', 'hw:1',
        '-filter_complex', "[1:v]scale=320:-1[webcam];[0:v][webcam]overlay=W-w-10:H-h-10:format=rgb;[2:a]highpass=f=200,lowpass=f=3000",
        '-flags', '+global_header',
        '-ar', '44100',
        '-ab', '128k',
        '-s', '1920x1080',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-vcodec', 'libx264',
        '-preset', 'ultrafast',
        '-pix_fmt', 'yuv420p',
        '-g', '25',
        '-vb', '750k',
        '-profile:v', 'baseline',
        '-r', '24',
        '-f', 'flv', f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
    ]

    # Run the FFmpeg command in a subprocess
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Return the RTMP link
    return jsonify({"rtmp_link": f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"})

if __name__ == "__main__":
    app.run(debug=True)
