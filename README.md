# ksy0095.github.io



This program is YouTube Video or Music Download program using the pytube

!--This pytube version--!

pytube 12.0.0 (not pytube3 9.6.4 = occured regx problem error and collision libraries)

!--GUI Environment--!

using the PYQT5, PYQT5 designer

!--EXE Packaging--!

using Pyinstaller

!--MP4 to MP3 Change function--!

using "ffmpeg.exe" (for window version)

<Issues / problem>

You can not download 1080p resolution video file, because does not supported pytube.

!--build process--!

open cmd prompt, put in the below Syntax code project or solutions directory\Pyinstaller [--option] [--option] [--option] [target_file.py]

!--I used option--!

--icon='path' : set a exe program icon // --noconsole : set a no popup console window // --add-data="path" : additional data // --onefile : only one .exe output file // target_file.py : extract to exe for target .py file
