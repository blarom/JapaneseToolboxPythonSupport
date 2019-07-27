import datetime
import os
import random
import re
import subprocess


def getLength(filename):
    result = subprocess.Popen(["c:\\Projects\\ffmpeg\\bin\\ffprobe.exe", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration = [str(x) for x in result.stdout.readlines() if "Duration" in str(x)][0]
    match = re.search(r'Duration: ([\d:.]+)', duration)
    if match:
        return datetime.datetime.strptime(match.group(1), "%H:%M:%S.%f")
    else:
        return None


path = 'e:\\Media\\Movies\\'

files_list = []
# r=root, d=directories, f = files
for root, directories, files in os.walk(path):
    for file in files:
        if any(item in file for item in ['.avi', '.mkv', '.mp4', '.ogm']):
            files_list.append(os.path.join(root, file))

random.shuffle(files_list)

finish_time = datetime.datetime.now() + datetime.timedelta(hours=7)
cumulative_time = datetime.datetime.now()
final_movies_list = []
for filename in files_list:
    duration = getLength(filename)
    if duration is not None:
        if cumulative_time + datetime.timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second) > finish_time:
            break
        else:
            cumulative_time += datetime.timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
            final_movies_list.append(filename)

    cmd = 'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe --started-from-file --playlist-enqueue "'+filename+'" --play-and-exit'
    p = subprocess.Popen(cmd)  # start and forget
    assert not p.poll()  # assert that it is started successfully
    #subprocess.check_call(cmd)

print(str(final_movies_list))
