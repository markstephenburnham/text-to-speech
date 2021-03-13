# text-to-speech
Sample script to to generate an mp3 speech file using Google Text-to-Speech

The processes were tested on MacOS, Big Sur, you'll likely need to modify for other systems.

### Functions

#### synthesize_ssml
#### process_txt_block

NOTE:  voices are hardcoded in this version

You will need to install ffmpeg and afplay to follow these instructions

### STEP BY STEP

#### 1) get a Google Cloud Account and install

pip3 install --upgrade google-cloud-speech

#### 2) export variables

```
export PYTHONPATH=/usr/local/lib/python3.9/site-packages
export GOOGLE_APPLICATION_CREDENTIALS=<path to your json credentials file>
```  
  
#### 3) run the processing script to process your transcription

This will create a new directory that you'll need to use in STEP 5.

```
~/dev/textToSpeech % ./text2speech.py -f snippet.txt -v1 en-US-Wavenet-H -v2 en-US-Wavenet-J
Processing file: snippet.txt
Voice 1: en-US-Wavenet-H
Voice 2: en-US-Wavenet-J
Output Path:/Users/markburnham/dev/textToSpeech/1615648935    <= you'll need this in the next 2 steps
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/1.mp3
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/2.mp3
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/3.mp3
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/4.mp3
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/5.mp3
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/6.mp3
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/7.mp3
Audio content written to file /Users/markburnham/dev/textToSpeech/1615648935/8.mp3
```

#### 4) cd into the newly created directory
```
% cd /Users/markburnham/dev/textToSpeech/1615648935
```
#### 5) create a file to be used by ffmpeg to concatenate the mp3 files

NOTE: The format of "filelist" is important

```
% ls -ltr *.mp3|awk '{print "file '\''<output path from step 3>/"$NF"'\''"}' > filelist

example =>
~/dev/textToSpeech/1615648935 % ls -ltr *.mp3|awk '{print "file '\''/Users/markburnham/dev/textToSpeech/1615648935/"$NF"'\''"}' > filelist
~/dev/textToSpeech/1615648935 % cat filelist
file '/Users/markburnham/dev/textToSpeech/1615648935/1.mp3'
file '/Users/markburnham/dev/textToSpeech/1615648935/2.mp3'
file '/Users/markburnham/dev/textToSpeech/1615648935/3.mp3'
file '/Users/markburnham/dev/textToSpeech/1615648935/4.mp3'
file '/Users/markburnham/dev/textToSpeech/1615648935/5.mp3'
file '/Users/markburnham/dev/textToSpeech/1615648935/6.mp3'
file '/Users/markburnham/dev/textToSpeech/1615648935/7.mp3'
file '/Users/markburnham/dev/textToSpeech/1615648935/8.mp3'
```
#### 6) use ffmpeg to process the filelist you created - this will concatenate the single files into a single mp3

```
~/dev/textToSpeech/1615648935 % ffmpeg -f concat -safe 0 -i filelist -c copy snippet.mp3
ffmpeg version 4.3.1 Copyright (c) 2000-2020 the FFmpeg developers
  built with Apple clang version 12.0.0 (clang-1200.0.32.28)
  configuration: --prefix=/usr/local/Cellar/ffmpeg/4.3.1_7 --enable-shared --enable-pthreads --enable-version3 --enable-avresample --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librtmp --enable-libspeex --enable-libsoxr --enable-videotoolbox --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack
  libavutil      56. 51.100 / 56. 51.100
  libavcodec     58. 91.100 / 58. 91.100
  libavformat    58. 45.100 / 58. 45.100
  libavdevice    58. 10.100 / 58. 10.100
  libavfilter     7. 85.100 /  7. 85.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  7.100 /  5.  7.100
  libswresample   3.  7.100 /  3.  7.100
  libpostproc    55.  7.100 / 55.  7.100
[mp3 @ 0x7fa635809000] Estimating duration from bitrate, this may be inaccurate
Input #0, concat, from 'filelist':
  Duration: N/A, start: 0.000000, bitrate: 32 kb/s
    Stream #0:0: Audio: mp3, 24000 Hz, mono, fltp, 32 kb/s
Output #0, mp3, to 'snippet.mp3':
  Metadata:
    TSSE            : Lavf58.45.100
    Stream #0:0: Audio: mp3, 24000 Hz, mono, fltp, 32 kb/s
Stream mapping:
  Stream #0:0 -> #0:0 (copy)
Press [q] to stop, [?] for help
[mp3 @ 0x7fa637017200] Estimating duration from bitrate, this may be inaccurate
[mp3 @ 0x7fa63600b000] Estimating duration from bitrate, this may be inaccurate
[mp3 @ 0x7fa637810200] Estimating duration from bitrate, this may be inaccurate
[mp3 @ 0x7fa63601c600] Estimating duration from bitrate, this may be inaccurate
[mp3 @ 0x7fa637017200] Estimating duration from bitrate, this may be inaccurate
[mp3 @ 0x7fa637010400] Estimating duration from bitrate, this may be inaccurate
[mp3 @ 0x7fa637810200] Estimating duration from bitrate, this may be inaccurate
size=     113kB time=00:00:28.89 bitrate=  32.1kbits/s speed=1.13e+03x    
video:0kB audio:113kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.204876%
```

#### 7) play your new mp3!
% afplay snippet.mp3
