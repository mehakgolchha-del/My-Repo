"""Voice Assistant Documentation."""

# Voice Assistant Module

This module provides voice control for the AI assistant with offline LLM integration.

## Features

- **Wake Word Detection**: Listen for "Hey Vish" to activate
- **Speech Recognition**: Convert speech to text using Google Speech Recognition
- **Text-to-Speech**: Respond with natural male voice using pyttsx3
- **Offline LLM**: Integrate with LLaMA 2 or Mistral for offline responses
- **Command Processing**: Execute voice commands

## Quick Start

```python
from voice_assistant import VoiceAssistant, LLMIntegration

# Initialize voice assistant
assistant = VoiceAssistant()

# Speak a message
assistant.speak("Hello, I'm ready to help")

# Start listening for wake word
def handle_command(command):
    print(f"Command received: {command}")
    llm = LLMIntegration()
    response = llm.answer_question(command)
    assistant.speak(response)

# Start listening in background
assistant.start_listening_thread(handle_command)
```

## Setup Instructions

### 1. Install Audio Libraries

```bash
# Linux
sudo apt-get install python3-pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Windows
pip install pyaudio
```

### 2. Download LLM Model

Download GGUF format models:
- [LLaMA 2 7B Chat](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
- [Mistral 7B](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

Place in `./models/` directory.

### 3. Configure

Edit `config.yaml` to set:
- Wake word
- Voice gender and speed
- Model path
- LLM parameters

## API Reference

### VoiceAssistant

- `speak(text)`: Speak text
- `listen(timeout)`: Listen for speech
- `detect_wake_word()`: Detect wake word
- `start_listening_loop(callback)`: Start listening loop
- `start_listening_thread(callback)`: Start listening in thread
- `stop_listening()`: Stop listening

### LLMIntegration

- `generate_response(prompt, max_tokens)`: Generate LLM response
- `answer_question(question)`: Answer a question

## Notes

- Requires microphone hardware
- Internet required for Google Speech Recognition (can use offline alternatives)
- LLM model file (~4-7GB) must be downloaded separately
- Works best with quiet environment
