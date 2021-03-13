#!/usr/local/bin/python3

__author__ = "Mark Burnham"
__copyright__ = "Copyright 2021, Mark Stephen Burnham"
__license__ = "GPL"
__version__ = "1.0.0"

import sys, getopt, os, re, json, argparse

counter=0
d=os.popen('date +%s').read().rstrip()


def synthesize_ssml(ssml,thevoice,output_file):
    """Synthesizes speech from the input string of ssml.
    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    Example: <speak>Hello there.</speak>
    """
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml)

    # A list of available voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=thevoice,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1   # speed up slightly to sound more natural
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + output_file)

# this is assumes a simple format as used by Rev.com - see snippet.txt       
def process_txt_block(speaker,text):
   
    global counter, d, output_path
 
    # set the voice according to speaker
    if "1" in speaker:
        #voice = 'en-US-Wavenet-H'
        voice = voice1
    else:
        #voice = 'en-US-Wavenet-J' 
        voice = voice2

    counter += 1

    output_file = output_path + "/" + str(counter) + ".mp3"

    ssml = "<speak>" + text + "</speak>"
    synthesize_ssml(ssml,voice,output_file)

#
# PROCESSING ==>
#

# set up arguments
# NOTE -this example assumes 2 speakers in the transcript

parser = argparse.ArgumentParser(description="generates an mp3 file for each section of a transcript")

parser.add_argument("-f", "--filename", help="transcription file", required=True)
parser.add_argument("-v1", "--voice1", help="voice for speaker 1", required=True)
parser.add_argument("-v2", "--voice2", help="voice for speaker 2", required=True)

args = parser.parse_args()

print('Processing file: ' + args.filename)
print('Voice 1: ' + args.voice1)
print('Voice 2: ' + args.voice2)

filename = args.filename
voice1 = args.voice1
voice2 = args.voice2

if not "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    print("Please set the GOOGLE credentials envar...")
    sys.exit(2)

# create a destination dir for mp3 files
cwd = os.getcwd()

output_path=cwd + "/" + d
print("Output Path:" + output_path)
os.mkdir(output_path)


# read transcript file line by line
file1 = open(filename, 'r') 
Lines = file1.readlines()

regex_txt = 'Speaker [123]:'                # Rev.com format
regex = re.compile(regex_txt)

speaker = ''
# Strips the newline character 
for line in Lines: 
    if speaker:                             # send to fetch mp3
        process_txt_block(speaker, line.strip())
        speaker = ''
        continue
    if re.match(regex, line) is not None:   # MATCHED Speaker 1, 2
        speaker = line.strip()              # fetchthe speaker
    else:
        speaker = ''    


