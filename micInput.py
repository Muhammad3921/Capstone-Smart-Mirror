import wave
import pyaudio
import requests

#values taken from Nyle's headset microphone
samplingRate = 48000
numChannels = 2
samplingWidth = 2

authorization_string = 'Bearer 87YDB3F1BAKHUVQGAT5UU5WL2TN9FFAY' #put in .env file

def transcribeCommand():
    url = "https://transcribe.whisperapi.com"
    headers = {
    'Authorization': authorization_string
    }
    file = {'file': open('command.wav', 'rb')}
    data = {
    "fileType": "wav",
    "diarization": "false",
    "numSpeakers": "1",
    "url": "",
    "initialPrompt": "",
    "language": "en",
    "task": "transcribe",
    "callbackURL": ""
    }
    response = requests.post(url, headers=headers, files=file, data=data)
    
    return(response.json())

def getVoiceCommand():
    p =  pyaudio.PyAudio()
    wf = wave.open("command.wav", 'wb')
    wf.setframerate(samplingRate)
    wf.setnchannels(numChannels)
    wf.setsampwidth(samplingWidth)

    stream = p.open(rate = samplingRate, channels = numChannels, format = p.get_format_from_width(samplingWidth), input = True)

    print("Recording")
    wf.writeframes(stream.read(250000)) #hardcoded number of frames - about 5s of input
    print("Done")

    stream.close()
    wf.close()
    p.terminate()