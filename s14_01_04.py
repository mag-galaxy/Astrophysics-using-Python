import subprocess

ffmpeg = 'ffmpeg'    # ffmpeg command

# ffmpeg options
options_ffmpeg = f'-f image2 -start_number 0 -framerate 30 -i sirius/sirius_%08d.png'\
                + f' -an -vcodec libx264 -pix_fmt yuv420p -threads 4'

file_output = 'sirius.mp4'  # output file name (mp4)

# command
command = f'{ffmpeg} {options_ffmpeg} {file_output}'
subprocess.run(command, shell=True)
