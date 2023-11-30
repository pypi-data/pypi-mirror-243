#!/bin/python

#pip install yt-dlp


import yt_dlp as yt
def main():
    url=input('Enter video url : ')

    ydl_opts={}

    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print('Video Downloaded Successfully ! ')

if __name__=='__main__':
    main()