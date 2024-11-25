from django.conf import settings
from openai import OpenAI


class ClientOpenAI:
    
    def __init__(self) -> None:
        self.__client = None
    
    @property
    def _client(self) -> OpenAI:
        if self.__client:
            return self.__client
        return OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def text_to_speech(self, text: str) -> bytes:
        response = self._client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        return response.content
    
    def speech_to_text(self, audio_file):
        transcription = self._client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcription.text
    
    def chat(self, request_text: str, main_context: str) -> str:
        completion = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": main_context},
                {
                    "role": "user",
                    "content": request_text
                }
            ],
        ) 
        return completion.choices[0].message.content
    
    def speech_to_speech_chat(self, audio, main_context): 
        request = self.speech_to_text(audio)
        answer = self.chat(request, main_context)
        return self.text_to_speech(answer)


if __name__ == "__main__":
    from pathlib import Path
    client = ClientOpenAI()
    main_context = "Ти психотерапевт у когнетивно-поведімковому підході з досвідом більше 10 років"
    audio_path = 'test.ogg'
    speech_file_path = Path(__file__).parent / audio_path
    answer = client.speech_to_speech_chat(speech_file_path, main_context)
    
    t = 1