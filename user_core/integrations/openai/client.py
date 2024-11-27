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
            file=audio_file,
        )
        return transcription.text
    
    def chat(self, request_text: str, main_context: str, messages: list[dict]) -> str:
        if not messages:
            messages = [{"role": "system", "content": main_context}]

        messages.append(
             {
                    "role": "user",
                    "content": request_text
                }
        )
        completion = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        ) 
        messages.append(
             {
                    "role": "assistant",
                    "content": completion.choices[0].message.content
                }
        )
        return completion.choices[0].message.content, messages
    
    def speech_to_speech_chat(self, audio, main_context, messages): 
        last_text = self.speech_to_text(audio)
        print('last_text: ', last_text)
        answer, messages = self.chat(last_text, main_context, messages)
        return self.text_to_speech(answer), messages


if __name__ == "__main__":
    from pathlib import Path
    client = ClientOpenAI()
    main_context = "Ти психотерапевт у когнетивно-поведімковому підході з досвідом більше 10 років"
    audio_path = 'test.ogg'
    speech_file_path = Path(__file__).parent / audio_path
    answer = client.speech_to_speech_chat(speech_file_path, main_context, [])
    
    t = 1