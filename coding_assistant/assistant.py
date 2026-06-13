"""Coding Assistant Module - Code generation, debugging, and analysis."""

import re
from typing import List, Dict, Optional
from loguru import logger
import yaml


class CodingAssistant:
    """AI-powered coding assistance for generation, debugging, and review."""
    
    SUPPORTED_LANGUAGES = [
        "python", "javascript", "java", "cpp", "csharp", "go", 
        "rust", "php", "ruby", "typescript", "sql", "html", "css"
    ]
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Coding Assistant.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.llm = None
        self._init_llm()
        logger.info("Coding Assistant initialized")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _init_llm(self) -> None:
        """Initialize LLM for code generation."""
        try:
            from voice_assistant.voice_assistant import LLMIntegration
            self.llm = LLMIntegration()
        except Exception as e:
            logger.warning(f"Could not initialize LLM: {e}")
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code from description.
        
        Args:
            description: Description of what code should do
            language: Programming language
            
        Returns:
            Generated code
        """
        if not self.llm:
            return "LLM not initialized"
        
        if language.lower() not in self.SUPPORTED_LANGUAGES:
            return f"Unsupported language: {language}"
        
        prompt = f"Write {language} code to: {description}\nCode:"
        code = self.llm.generate_response(prompt, max_tokens=1024)
        logger.info(f"Generated {language} code")
        return code
    
    def debug_code(self, code: str, error: str, language: str = "python") -> str:
        """Debug code based on error.
        
        Args:
            code: Code that has error
            error: Error message
            language: Programming language
            
        Returns:
            Fixed code with explanation
        """
        if not self.llm:
            return "LLM not initialized"
        
        prompt = f"""Debug this {language} code:
```
{code}
```
Error: {error}

Fixed code and explanation:"""
        
        fix = self.llm.generate_response(prompt, max_tokens=1024)
        logger.info("Code debugging completed")
        return fix
    
    def review_code(self, code: str, language: str = "python") -> Dict[str, any]:
        """Review code for issues and improvements.
        
        Args:
            code: Code to review
            language: Programming language
            
        Returns:
            Review results with issues and suggestions
        """
        if not self.llm:
            return {"status": "error", "message": "LLM not initialized"}
        
        prompt = f"""Review this {language} code and provide:
1. Issues found (bugs, security, performance)
2. Code style improvements
3. Optimization suggestions

```
{code}
```

Review:"""
        
        review = self.llm.generate_response(prompt, max_tokens=1024)
        logger.info("Code review completed")
        
        return {
            "language": language,
            "review": review,
            "code_length": len(code),
            "issues_found": self._count_issues(review)
        }
    
    def explain_code(self, code: str, language: str = "python") -> str:
        """Explain what code does.
        
        Args:
            code: Code to explain
            language: Programming language
            
        Returns:
            Explanation of code
        """
        if not self.llm:
            return "LLM not initialized"
        
        prompt = f"Explain this {language} code:\n```\n{code}\n```\nExplanation:"
        explanation = self.llm.generate_response(prompt, max_tokens=512)
        logger.info("Code explanation completed")
        return explanation
    
    def optimize_code(self, code: str, language: str = "python") -> str:
        """Optimize code for performance.
        
        Args:
            code: Code to optimize
            language: Programming language
            
        Returns:
            Optimized code
        """
        if not self.llm:
            return "LLM not initialized"
        
        prompt = f"""Optimize this {language} code for performance and readability:
```
{code}
```

Optimized code:"""
        
        optimized = self.llm.generate_response(prompt, max_tokens=1024)
        logger.info("Code optimization completed")
        return optimized
    
    def suggest_improvements(self, code: str, language: str = "python") -> List[str]:
        """Suggest improvements to code.
        
        Args:
            code: Code to analyze
            language: Programming language
            
        Returns:
            List of improvement suggestions
        """
        review = self.review_code(code, language)
        suggestions = review.get('review', '').split('\n')
        return [s.strip() for s in suggestions if s.strip()]
    
    def _count_issues(self, review_text: str) -> int:
        """Count issues found in review."""
        issue_keywords = ['bug', 'error', 'issue', 'problem', 'vulnerability']
        count = 0
        for keyword in issue_keywords:
            count += len(re.findall(rf'\b{keyword}\b', review_text.lower()))
        return count


if __name__ == "__main__":
    assistant = CodingAssistant()
    
    # Example: Generate code
    code = assistant.generate_code("Create a function to calculate factorial")
    print("Generated Code:")
    print(code)
    
    # Example: Review code
    review = assistant.review_code(code)
    print(f"\nReview: {review}")
