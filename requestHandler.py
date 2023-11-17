from micInput import *

getVoiceCommand()
response = transcribeCommand()
print(response["text"])

