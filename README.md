# slice of life

Bulk rip audio from video files and split into small chunks.

This is an immersion tool for language learning. Prepares audio files from
TV/Movies for passive listening. By creating small chunks it's easier to skip
through tracks (or shuffle).

#### Features

- Adjustable segment length
- MP3 tagging album art embedding
- Progress bar from [tqdm](https://github.com/tqdm/tqdm)
- Chance to confirm options and files before processing

#### In Progress

- Album art embedding
- Prompting to select audio tracks before processing


#### Usage

```
usage: slice_of_life.py [-h] \
	--video-dir VIDEO_DIR \
	--artist-name ARTIST_NAME \
	--album-name ALBUM_NAME \
	[--output-dir OUTPUT_DIR] \
	[--segment-time SEGMENT_TIME] \
	[--album-art ALBUM_ART]

Bulk rip audio from video files and split into small chunks.

optional arguments:
  -h, --help            show this help message and exit
  --video-dir VIDEO_DIR, -v VIDEO_DIR
                        The directory of videos to process.
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        The directory to place output audio files (default=/tmp).
  --segment-time SEGMENT_TIME, -s SEGMENT_TIME
                        The length of the audio snippets in seconds (default=180).
  --artist-name ARTIST_NAME
                        The artist name for the mp3 tags.
  --album-name ALBUM_NAME
                        The album name for the mp3 tags.
  --album-art ALBUM_ART
                        The cover art to be embedded into the mp3 files.
```
