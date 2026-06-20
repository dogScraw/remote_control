import evdev
import mds_commands as cmd
import mds_process_voice as voice

import pyaudio
p = pyaudio.PyAudio()

microphone_id = "Unknown"
for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    print(device['name'])

    if "USB Composite Device: Audio" in device['name'] and device['maxInputChannels'] > 0:
        microphone_id = i

p.terminate()

# Start the AI voice recognizer
from vosk import Model, KaldiRecognizer
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

remote_dev_path = "Unknown"
all_devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for dev in all_devices:
    remote_name = ["haobo", "keyboard"]

    if all(sub in dev.name.lower() for sub in remote_name):
        remote_dev_path = dev.path

try:
    device = evdev.InputDevice(remote_dev_path)
    print(f"Listening for input on {device.name}...")
except Exception as e:
    print(f"Failed to open device: {e}")
    exit(1)

command = []
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:

        key_event = evdev.categorize(event)

        # key_event.keystate 1 = Key Down, 0 = Key Up, 2 = Key Hold
        if key_event.keystate == 1 and key_event.keycode == "KEY_SELECT":
            cmd.run_commands(command)
            command.clear()

        if key_event.keystate == 1 and key_event.keycode == "KEY_VOICECOMMAND":
            print("Hearing you")
            voice.process_voice_command(recognizer, microphone_id)

        if key_event.keystate == 1 and key_event.keycode != "KEY_SELECT":
            command.append(key_event.keycode)


