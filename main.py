"""Main application entry point."""

from loguru import logger
from voice_assistant.voice_assistant import VoiceAssistant, LLMIntegration
from pc_automation.automation import PCAutomation
from coding_assistant.assistant import CodingAssistant
from media_processing.processor import ImageProcessor, VideoProcessor
from analytics_dashboard.analytics import Analytics
import yaml


class AIAssistant:
    """Main AI Assistant orchestrator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize AI Assistant with all modules.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        
        # Initialize modules
        logger.info("Initializing AI Assistant...")
        self.voice = VoiceAssistant(config_path)
        self.llm = LLMIntegration(config_path)
        self.automation = PCAutomation(config_path)
        self.coder = CodingAssistant(config_path)
        self.image_processor = ImageProcessor(config_path)
        self.video_processor = VideoProcessor(config_path)
        self.analytics = Analytics(config_path)
        
        logger.info("AI Assistant initialized successfully!")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def greet(self) -> None:
        """Greet the user."""
        greeting = "Hello! I'm your AI assistant. I'm ready to help with voice commands, coding, image processing, and more!"
        self.voice.speak(greeting)
        logger.info(greeting)
    
    def start_interactive(self) -> None:
        """Start interactive mode with voice commands."""
        logger.info("Starting interactive mode...")
        self.greet()
        
        def handle_command(command: str) -> None:
            """Handle voice commands."""
            logger.info(f"Handling command: {command}")
            
            # Route command to appropriate module
            if "code" in command or "program" in command:
                response = self.coder.generate_code(command)
                self.voice.speak(response[:100])  # Speak first 100 chars
            elif "file" in command:
                response = "File operation requested. Details coming soon."
                self.voice.speak(response)
            elif "screenshot" in command:
                path = self.automation.take_screenshot()
                self.voice.speak(f"Screenshot saved to {path}")
            else:
                # Use LLM for general questions
                response = self.llm.answer_question(command)
                self.voice.speak(response[:200])  # Speak first 200 chars
        
        # Start listening for wake word
        self.voice.start_listening_thread(handle_command)
        
        # Keep running
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("Interactive mode stopped")
            self.voice.speak("Goodbye!")


if __name__ == "__main__":
    assistant = AIAssistant()
    
    # Option 1: Start interactive voice mode
    # assistant.start_interactive()
    
    # Option 2: Use individual modules
    print("\n=== AI Assistant Initialized ===")
    print("Available modules:")
    print("- Voice Assistant: voice, llm")
    print("- PC Automation: automation")
    print("- Coding Assistant: coder")
    print("- Image Processing: image_processor")
    print("- Video Processing: video_processor")
    print("- Analytics: analytics")
    print("\nExample usage:")
    print("  assistant.voice.speak('Hello')")
    print("  assistant.coder.generate_code('Create a hello world function')")
    print("  assistant.automation.take_screenshot()")
    print("  assistant.analytics.get_balance()")
