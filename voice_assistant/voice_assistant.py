"""Voice Assistant Module - Wake word detection, speech recognition, and TTS."""

import os
import threading
from typing import Callable, Optional
from loguru import logger
import speech_recognition as sr
import pyttsx3
import yaml
from pathlib import Path

class VoiceAssistant:
    """Main voice assistant class with wake word detection and response."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize voice assistant with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self._setup_tts()
        self.is_listening = False
        self.wake_word = self.config['voice']['wake_word'].lower()
        logger.info(f"Voice Assistant initialized with wake word: {self.wake_word}")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _setup_tts(self) -> None:
        """Configure text-to-speech engine."""
        self.engine.setProperty('rate', self.config['voice']['speech_rate'])
        self.engine.setProperty('volume', self.config['voice']['volume'])
        
        # Set voice gender
        voices = self.engine.getProperty('voices')
        if self.config['voice']['voice_gender'].lower() == 'male':
            self.engine.setProperty('voice', voices[0].id)
        else:
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
    
    def speak(self, text: str) -> None:
        """Speak text using TTS.
        
        Args:
            text: Text to speak
        """
        logger.info(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for audio input and convert to text.
        
        Args:
            timeout: Listening timeout in seconds
            
        Returns:
            Recognized text or None
        """
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def detect_wake_word(self) -> bool:
        """Detect wake word in audio.
        
        Returns:
            True if wake word detected
        """
        text = self.listen(timeout=2)
        return text and self.wake_word in text if text else False
    
    def start_listening_loop(self, callback: Callable[[str], None]) -> None:
        """Start continuous listening loop for wake word.
        
        Args:
            callback: Function to call when wake word detected
        """
        self.is_listening = True
        logger.info("Starting listening loop...")
        
        while self.is_listening:
            if self.detect_wake_word():
                logger.info(f"Wake word '{self.wake_word}' detected!")
                self.speak("Yes, I'm listening")
                command = self.listen(timeout=10)
                if command:
                    callback(command)
    
    def start_listening_thread(self, callback: Callable[[str], None]) -> threading.Thread:
        """Start listening in background thread.
        
        Args:
            callback: Function to call when command received
            
        Returns:
            Thread object
        """
        thread = threading.Thread(target=self.start_listening_loop, args=(callback,))
        thread.daemon = True
        thread.start()
        return thread
    
    def stop_listening(self) -> None:
        """Stop the listening loop."""
        self.is_listening = False
        logger.info("Stopped listening")


class LLMIntegration:
    """Integration with offline LLMs (LLaMA 2, Mistral)."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize LLM integration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.model = None
        self._load_model()
        logger.info("LLM Integration initialized")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_model(self) -> None:
        """Load LLM model (requires model file to be present)."""
        try:
            from llama_cpp import Llama
            model_path = self.config['llm']['model_path']
            if os.path.exists(model_path):
                self.model = Llama(
                    model_path=model_path,
                    n_ctx=self.config['llm']['context_length'],
                    n_threads=4
                )
                logger.info(f"Loaded model: {model_path}")
            else:
                logger.warning(f"Model not found at {model_path}")
        except ImportError:
            logger.warning("llama-cpp-python not installed. Install with: pip install llama-cpp-python")
    
    def generate_response(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate response from LLM.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        if not self.model:
            return "LLM model not loaded. Please ensure the model file is present."
        
        max_tokens = max_tokens or self.config['llm']['max_tokens']
        
        try:
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=self.config['llm']['temperature']
            )
            return response['choices'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Error generating response"
    
    def answer_question(self, question: str) -> str:
        """Answer a question using the LLM.
        
        Args:
            question: Question to answer
            
        Returns:
            Answer
        """
        prompt = f"Question: {question}\nAnswer:"
        return self.generate_response(prompt)


if __name__ == "__main__":
    # Example usage
    assistant = VoiceAssistant()
    assistant.speak("Voice assistant initialized successfully")
    
    llm = LLMIntegration()
    response = llm.answer_question("What is Python?")
    print(f"LLM Response: {response}")
