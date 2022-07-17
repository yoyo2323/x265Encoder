import os
import sys
import json
import time
import ffmpeg
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

def get_codec(filepath, channel='v:0'):
    output = check_output(['ffprobe', '-v', 'error', '-select_streams', channel,
                            '-show_entries', 'stream=codec_name,codec_tag_string', '-of', 
                            'default=nokey=1:noprint_wrappers=1', filepath])
    return output.decode('utf-8').split()

def encode(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    output_filepath = basefilepath + '[HEVC]' + '.mp4'
    assert(output_filepath != filepath)
    if os.path.isfile(output_filepath):
        print('Skipping "{}": File Already Exists 🤷‍♂️'.format(output_filepath))
        return None
    print(filepath)
    # Get the video channel codec
    video_codec = get_codec(filepath, channel='v:0')
    if video_codec == []:
        print('Skipping No Video Codec Reported 🤷‍♂️')
        return None
    # Video transcode options
    if video_codec[0] == 'avif':
        if video_codec[1] == 'avif':
            print('Skipping :( Already In avif')
            return None
        else:
            # Copy stream to hvc1
            video_opts = '-c:v libsvtav1 -s 1024x576 -crf 45  -sn -threads 8'
    else:
        # Transcode to h265 / hvc1
        video_opts = '-c:v libsvtav1 -s 1024x576 -crf 45  -sn -threads 8'
    # Get the audio channel codec
    audio_codec = get_codec(filepath, channel='a:0')
    if audio_codec == []:
        audio_opts = ''
    elif audio_codec[0] == 'aac':
        audio_opts = '-c:a copy'
    else:
        audio_opts = '-c:a libfdk_aac -profile:a aac_he_v2 -vbr 1'
    call(['ffmpeg', '-i', filepath] + video_opts.split() + audio_opts.split() + [output_filepath])
    os.remove(filepath)
    return output_filepath

def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
            .input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
      return None

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720
