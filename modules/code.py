"""Code Helper - Helps you generate and debug code."""

from loguru import logger


class CodeHelper:
    """Help with coding tasks."""
    
    def __init__(self):
        """Initialize the code helper."""
        logger.info("📝 Code Helper initializing...")
        logger.info("✅ Code Helper ready!")
    
    def generate(self, description: str, language: str = 'python') -> str:
        """Generate code from a description.
        
        Args:
            description: What you want the code to do
            language: Programming language (python, javascript, etc)
            
        Returns:
            Generated code
        """
        logger.info(f"Generating {language} code for: {description}")
        
        # Simple templates for common requests
        templates = {
            'hello world': {
                'python': 'print("Hello, World!")',
                'javascript': 'console.log("Hello, World!");',
                'java': 'public class HelloWorld {\n  public static void main(String[] args) {\n    System.out.println("Hello, World!");\n  }\n}'
            },
            'add numbers': {
                'python': 'def add(a, b):\n    return a + b\n\nresult = add(5, 3)\nprint(result)',
                'javascript': 'function add(a, b) {\n  return a + b;\n}\n\nconst result = add(5, 3);\nconsole.log(result);'
            },
            'list': {
                'python': 'my_list = [1, 2, 3, 4, 5]\nprint(my_list)',
                'javascript': 'const myList = [1, 2, 3, 4, 5];\nconsole.log(myList);'
            }
        }
        
        # Check if we have a template for this
        for keyword, langs in templates.items():
            if keyword in description.lower():
                if language in langs:
                    code = langs[language]
                    logger.info(f"✅ Generated code using template: {keyword}")
                    return code
        
        # If no template, return a generic template
        generic_templates = {
            'python': '# Your code here\nprint("This is Python code")',
            'javascript': '// Your code here\nconsole.log("This is JavaScript");',
            'java': 'public class Main {\n  public static void main(String[] args) {\n    System.out.println("This is Java");\n  }\n}',
            'html': '<html>\n  <head><title>Hello</title></head>\n  <body>\n    <h1>Hello World</h1>\n  </body>\n</html>'
        }
        
        code = generic_templates.get(language, f'# {language} code goes here')
        logger.info(f"✅ Generated generic {language} template")
        return code


if __name__ == "__main__":
    helper = CodeHelper()
    code = helper.generate("hello world", "python")
    print(code)
