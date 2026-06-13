"""AI Brain - The main AI that answers questions."""

from loguru import logger


class AIBrain:
    """Simple AI that answers questions.
    
    This is like the intelligence of your assistant.
    It processes questions and gives answers.
    """
    
    def __init__(self):
        """Start up the AI brain."""
        logger.info("🧠 AI Brain initializing...")
        self.model = None
        self._load_llm()
        logger.info("✅ AI Brain ready!")
    
    def _load_llm(self):
        """Try to load the offline LLM model.
        
        This is optional - if it fails, AI will still work
        but might be less powerful.
        """
        try:
            # Try to import the LLM library
            from llama_cpp import Llama
            import os
            
            model_path = './models/llama-2-7b-chat.gguf'
            
            # Check if model file exists
            if os.path.exists(model_path):
                logger.info(f"📥 Loading AI model from: {model_path}")
                self.model = Llama(model_path=model_path, n_ctx=512, n_threads=4)
                logger.info("✅ Model loaded successfully!")
            else:
                logger.warning(f"⚠️  Model file not found at {model_path}")
                logger.warning("   The AI will use basic responses")
                logger.info("   To use full AI: Download from https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF")
        except ImportError:
            logger.warning("⚠️  llama-cpp-python not installed")
            logger.warning("   AI will use basic responses")
        except Exception as e:
            logger.warning(f"⚠️  Error loading model: {e}")
    
    def answer_question(self, question: str) -> str:
        """Answer a question from the user.
        
        Args:
            question: What the user is asking
            
        Returns:
            The AI's answer
        """
        logger.info(f"❓ User asked: {question}")
        
        # If we have the AI model loaded
        if self.model:
            try:
                prompt = f"Answer this question: {question}\n\nAnswer:"
                response = self.model(
                    prompt,
                    max_tokens=200,
                    temperature=0.7
                )
                answer = response['choices'][0]['text'].strip()
                logger.info(f"✅ AI answered: {answer}")
                return answer
            except Exception as e:
                logger.error(f"❌ Error with AI: {e}")
                return self._get_fallback_response(question)
        else:
            # If no AI model, use basic responses
            return self._get_fallback_response(question)
    
    def _get_fallback_response(self, question: str) -> str:
        """Give a basic response if AI model isn't available.
        
        This is a simple dictionary of common questions and answers.
        It helps the AI work even without the fancy model.
        """
        # Convert question to lowercase to match patterns
        q = question.lower()
        
        # Dictionary of questions and answers
        responses = {
            'hello': 'Hello! I\'m your AI assistant. How can I help you today?',
            'hi': 'Hi there! What can I help you with?',
            'how are you': 'I\'m working great! Ready to help you.',
            'what can you do': 'I can help with: coding, file management, image editing, finance tracking, and more!',
            'help': 'I can help with: 1) Answer questions, 2) Generate code, 3) Manage files, 4) Track finances, 5) Edit images',
            'thanks': 'You\'re welcome! Anything else I can help with?',
            'bye': 'Goodbye! Come back soon!',
        }
        
        # Look for matching keywords
        for key, answer in responses.items():
            if key in q:
                logger.info(f"✅ Matched keyword: {key}")
                return answer
        
        # If no match, give a generic response
        logger.info("⚠️  No matching response found")
        return f'I received your message: "{question}". To get better answers, please download the AI model. See BEGINNER_GUIDE.md for details.'


if __name__ == "__main__":
    # Test the AI brain
    brain = AIBrain()
    answer = brain.answer_question("Hello")
    print(f"Answer: {answer}")
