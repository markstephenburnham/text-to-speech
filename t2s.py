#!/usr/local/bin/python3

import sys, getopt, os, re, json

counter=0
d=os.popen('date +%s').read().rstrip()


# def synthesize_ssml(ssml):
def synthesize_ssml(ssml,thevoice,output_file):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    Example: <speak>Hello there.</speak>
    """
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # A list of available voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=thevoice,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.1
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + output_file)

# this is assumes a simple format as used by Rev.com - see sample        
def process_txt_block(speaker,text):
   
    global counter, d, output_path
 
    body = """
    {
    "input":{
     "ssml":"<speak>Here is some nice text.</speak>"
    },
    "voice":{
      "languageCode":"en-us",
      "name":"en-US-Standard-B",
      "ssmlGender":"MALE"
    },
    "audioConfig":{
      "audioEncoding":"MP3"
    }
    }
    """
    # set the voice according to speaker
    if "1" in speaker:
        voice = 'en-US-Wavenet-H'
    else:
        voice = 'en-US-Wavenet-J'        
    counter += 1

    output_file = output_path + "/" + str(counter) + ".mp3"

    ssml = "<speak>" + text + "</speak>"
    synthesize_ssml(ssml,voice,output_file)

#    j = json.loads(body)
#    j["input"]["ssml"] = "<speak>" + text + "</speak>"
#    j["voice"]["name"] = voice
    
#    print(j["voice"]["name"])
#    print(j["input"]["ssml"])
   

voice1 = 'en-US-Wavenet-A'
voice2 = 'en-US-Wavenet-F'

inputfile = ''
speaker_1_voice = ''  #s1

# gender is not supported in the API!
speaker_1_gender = '' #g1

speaker_2_voice = ''  #s2
speaker_2_gender = '' #g2

try:
    opts, args = getopt.getopt(sys.argv[1:],"hf:s:t:u:v:",["filename=","s1_voice=","s1_gender=","s2_voice=","s2_gender="])
except getopt.GetoptError:
    print('t2s.py -f <input_file> -s1 <speaker1_voice> -g1 <speaker1_gender> -s2 <speaker2_voice> -g2 <speaker2_gender>')
    sys.exit(2)

# set up parameters
for opt, arg in opts:
 #   print("opt=" + opt)
 #   print("arg=" + arg)
    if opt == '-h':
        print('t2s.py -f <input_file> -s1 <speaker1_voice> -g1 <speaker1_gender> -s2 <speaker2_voice> -g2 <speaker2_gender>')
        sys.exit(2)
    elif opt in ('-f','--filename'):
        inputfile = arg
    elif opt in ('-s','--s1_voice'):
        speaker_1_voice = arg
    elif opt in ('-t','--s1_gender'):
        gender_1_voice = arg
    elif opt in ('-u','--s2_voice'):
        speaker_2_voice = arg
    elif opt in ('-v','--s2_gender'):
        gender_2_voice = arg
    else:
        print("NO MATCH: opt=" + opt)
        print("NO MATCH: arg=" + arg)

if not "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    print("Please set the GOOGLE credentials envar...")
    sys.exit(2)

# create a destination dir for files
cwd = os.getcwd()

output_path=cwd + "/" + d
print("output path:" + output_path)
os.mkdir(output_path)
#print(sys.argv);

#print("Processing file: " + inputfile)
#print("speaker_1_voice: " + speaker_1_voice)

# pass in Speaker 1 voice parms [voice, gender]
# pass in Speaker 2 voice parms
# pass in directory name for files

# read file line by line
# Using readlines() 
file1 = open(inputfile, 'r') 
Lines = file1.readlines()

regex_txt = 'Speaker [123]:' 
regex = re.compile(regex_txt)

speaker = ''
# Strips the newline character 
for line in Lines: 
#    print("Line{}: {}".format(count, line.strip()))
    if speaker:                             # send to fetch mp3
        #print(line.strip())
        process_txt_block(speaker, line.strip())
        speaker = ''
        continue
    if re.match(regex, line) is not None:   # MATCHED Speaker 1, 2
       # print(line)
        speaker = line.strip()              # grab the speaker
    else:
        speaker = ''    

# if contains "Speaker", save to var, set process = 1
# if contains txt, NOT speaker, concat to var
# if empty, check parms and process

# grab speaker occurences
# process by Speaker 1,2

