import subprocess

# ffmpeg command
ffmpeg = 'ffmpeg'

# ffmpeg options
options_ffmpeg = f'-f image2 -start_number 0 -framerate 30' \
    + f' -i binary/binary_%08d.png' \
    + f' -an -vcodec libx264 -pix_fmt yuv420p -threads 4'

file_output = 'sirius_binary.mp4'  # output file name (mp4)

# command
command_ffmpeg = f'{ffmpeg} {options_ffmpeg} {file_output}'
subprocess.run(command_ffmpeg, shell=True)
