import os
from os import PathLike
from time import time
import asyncio
from typing import Union
from dotenv import load_dotenv
# from Wav2Lip.inference_main import main_main
import openai
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from deepgram import Deepgram
import pygame
from pygame import mixer
import elevenlabs
from record import speech_to_text
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
elevenlabs.set_api_key(os.getenv("ELEVENLABS_API_KEY"))
REPLICATE_API_TOKEN=(os.getenv("REPLICATE_API_TOKEN"))

gpt_client = openai.Client(api_key=OPENAI_API_KEY)
deepgram = Deepgram(DEEPGRAM_API_KEY)
mixer.init()
context = "You are shravya and the user that are talking to is Gyan. You are my Girl friend. Your answers should be limited to 1-2 short sentences."
# context = "Your name is suneel and the user that are talking to is Gyan. Your answers should be limited to 1-2 short sentences."

conversation = {"Conversation": []}
RECORDING_PATH = "audio/recording.wav"

def request_gpt(prompt: str) -> str:
    response = gpt_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content

def getLLamaresponse(input_text):
    llm=CTransformers(model='./llama/llama-2-7b-chat.ggmlv3.q2_K.bin',
                      model_type='llama',
                      n_gqa=8,
                      config={'max_new_tokens':100,
                              'temperature':0.1})
    prompt=PromptTemplate(input_variables=["input_text"],
                          template=input_text)
    response_text=llm(prompt.format(input_text=input_text))
    return response_text

async def transcribe(file_name):
    with open(file_name, "rb") as audio:
        source = {"buffer": audio, "mimetype": "audio/wav"}
        response = await deepgram.transcription.prerecorded(source)
        return response["results"]["channels"][0]["alternatives"][0]["words"]

if __name__ == "__main__":
    while True:
        print("Listening...")
        speech_to_text()
        print("Done listening")
        current_time = time()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        words = loop.run_until_complete(transcribe(RECORDING_PATH))
        string_words = " ".join(
            word_dict.get("word") for word_dict in words if "word" in word_dict
        )
        # with open("conv.txt", "a") as f:
        #     f.write(f"{string_words}\n")
        transcription_time = time() - current_time
        print(f"Finished transcribing in {transcription_time:.2f} seconds.")

        # CHAT_GPT_3_MODEL
        # current_time = time()
        # context += f"\Gyan: {string_words}\Shravya: "
        # response = request_gpt(context)
        # context += response
        # gpt_time = time() - current_time
        # print(f"Finished generating response for Chatgpt model in {gpt_time:.2f} seconds.")
        
        # LLAMA_MODEL
        current_time = time()
        context += f"\Gyan: {string_words}\shravya: "
        response = getLLamaresponse(context)
        context += response
        llama_time = time() - current_time
        print(f"Finished generating response for LLAMA model in {llama_time:.2f} seconds.")
        
        current_time = time()
        audio = elevenlabs.generate(
            text=response, voice="Lily", model="eleven_monolingual_v1"
        )
        elevenlabs.save(audio, "audio/response.wav")
        audio_time = time() - current_time
        print(f"Finished generating audio in {audio_time:.2f} seconds.")
        current_time = time()
        os.system(f'conda activate wavlip && python inference.py --checkpoint_path .\models\wav2lip_gan.pth --face shravya.png --audio ./audio/response.wav --outfile ./web_api_testing/static/result_voice.mp4 && conda deactivate')
        weblip_time = time() - current_time
        print(f"Finished generating response for WebLip model in {weblip_time:.2f} seconds.")
        print("Speaking...")
        # sound = mixer.Sound("audio/response.wav")
        # with open("conv.txt", "a") as f:
        #     f.write(f"{response}\n")
        # sound.play()
        # pygame.time.wait(int((sound.get_length() * 1000)))
        # os.system("cp ./web_api_testing/result_voice.mp4 ./web_api_testing/static/result_voice.mp4 ")
        # os.remove("./web_api_testing/static/result_voice.mp4")
        print(f"\n --- GYAN: {string_words}\n --- shravya: {response}\n")
        
        input()
