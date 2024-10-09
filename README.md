<h1>
  Log Downloaded Youtube Videos
   <img src="https://github.com/cluster-coder/cluster-coder/blob/86c9f575c16835d153d9008a2dd7582e53b89725/Assets/Utility_Badge.png" height=30 align="right">
</h1>

Given a folder path, this code will get all the videos and music files(.mp4, .mp3) in a folder and it's subdirectories and output usefull information about them in a .json file.

> [!NOTE]
> FFMPEG is used to get the video/music duration and pytube helps with finding it's youtube information, make sure both of them are properly installed.  
> [FFMPEG download tab](https://www.ffmpeg.org/download.html)  
> [Pytubefix github repository](https://github.com/JuanBindez/pytubefix?tab=readme-ov-file#install)

## Usage example
Suppose we have a folder with 2 videos in the path `C:\Hypothetical folder` we would just open the `LogYoutubeVideos.py` and input this path.  
Then, a `Hypothetical folder.json` file will be created in the same folder with the following information:
```json
[
  "C:\\Hypothetical folder",
  {
    "Lazy Afternoons - Kingdom Hearts II Music Extended.mp4": {
      "Youtube": {
        "Title": "Lazy Afternoons - Kingdom Hearts II Music Extended",
        "URL": "https://youtube.com/watch?v=MNBPHmEkPhU",
        "i": 1
      },
      "Length": "30:00",
      "Modification date": "14/07/2024 02:17:16",
      "Creation date": "14/07/2024 02:16:56",
      "Bytes": 39958369,
      "Megabytes": 38.1
    },
    "surskit - a.mp4": {
      "Youtube": {
        "Title": "surskit - a",
        "URL": "https://youtube.com/watch?v=PYNYpkZLhXY",
        "i": 1
      },
      "Length": "0:11",
      "Modification date": "14/07/2024 02:50:36",
      "Creation date": "14/07/2024 02:50:35",
      "Bytes": 502975,
      "Megabytes": 0.5
    }
  }
]
```

## Youtube information
The file's name will be get and be put on a youtube search by pytube, then it will iterate through the found videos and if they have the same length as the file, 
their names (without invalid characters for a filename) will be compared, if it is a exact match, it will stop searching, otherwise it will look for more videos, up to ~100  

If no exact match is found, the first video with the exact time duration that was shown will be chosen, if there is none, a "No match found." will be outputted in it's place.  

When a video is chosen, it's `title`, `URL`, and "`i`" will be present in the `Youtube` object, `i` being the chosen video's position in the results.
The result may be inaccurate if the video name is too generic, short or it's view count is too low.

> [!NOTE]
> As youtube is ocasionally changing, sometimes conflicts with it and pytube's code may arise,  
> [pytube's original repository](https://github.com/pytube/pytube) is no longer being maintained or updated, but using the latest version of [pytubefix](https://github.com/JuanBindez/pytubefix) should work.