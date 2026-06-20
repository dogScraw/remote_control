import pyaudio
import json


def process_voice_command(recognizer, microphone_id):

    # Initialize PyAudio to capture microphone input
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        input_device_index=microphone_id,
        frames_per_buffer=8192
    )
    stream.start_stream()

    while True:
        # Read raw chunk data from the microphone
        data = stream.read(4096, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            # A full sentence/phrase was completed
            result = json.loads(recognizer.Result())
            print(f"You said: {result['text']}")
            break

    # Clean up resources
    stream.stop_stream()
    stream.close()
    p.terminate()