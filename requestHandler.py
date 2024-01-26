from micInput import *


while True:
        print("in while loop")
        if(listen()):
            getVoiceCommand()
            response = transcribeCommand()
            print(response["text"])

            if("bye" in response["text"].lower()):
                print("goodbye sire")
                break

