"ffmpeg\bin\ffmpeg.exe" ^
-framerate 30 ^
-i frames\%%d.png ^
-c:v libx264 ^
-profile:v high ^
-r 30 ^
-pix_fmt yuv420p ^
animated_word_cloud.mp4
