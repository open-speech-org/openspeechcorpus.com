"""
Convierte archivos a formato wav
"""
__author__ = 'ma0'
import os

mp4_path = "output_folder"
convert_path = "output_folder_wav"
so_path_separator = "/"


def recursive_convert(path, root_dir):
    if os.path.isdir(root_dir+so_path_separator+path):
        if not os.path.exists(convert_path+so_path_separator+path):
            os.makedirs(convert_path+so_path_separator+root_dir+so_path_separator+path)
        dirs = os.listdir(root_dir+so_path_separator+path)
        for directory in dirs:
            recursive_convert(directory, root_dir+so_path_separator+path)
    else:
        # if (root_dir+so_path_separator+path).endswith(".wav"):
        #     os.popen("rm %s" % root_dir+so_path_separator+path)
        print(root_dir+so_path_separator+path)
        if "3gp" in path:
            os.popen(
                "ffmpeg -i %s -qscale 0 -ab 64k -ar 16000 %s" %
                (
                    root_dir+so_path_separator+path,
                    convert_path+so_path_separator+root_dir+so_path_separator+path.replace(".3gp", "_3gp.wav")
                )
            )
        elif "mp4" in path:
            os.popen(
                "ffmpeg -i %s -qscale 0 -ab 64k -ar 16000 %s" %
                (
                    root_dir+so_path_separator+path,
                    convert_path+so_path_separator+root_dir+so_path_separator+path.replace(".mp4", ".wav")
                )
            )

recursive_convert("", mp4_path)



