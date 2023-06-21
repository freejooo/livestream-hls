ffmpeg -thread_queue_size 1024 -f alsa -ac 2 -i default -f x11grab -r 30 -s 1920x1080 -i :0.0 -acodec aac -af "highpass=f=200" -vcodec libx264 -preset ultrafast -crf 0 -threads 0 output.mp4
