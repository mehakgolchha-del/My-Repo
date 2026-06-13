"""Coding Assistant Documentation."""

# Coding Assistant Module

AI-powered coding assistance for code generation, debugging, and analysis.

## Features

- **Code Generation**: Generate code from descriptions
- **Debugging**: Fix code errors with AI assistance
- **Code Review**: Analyze code for issues and improvements
- **Code Explanation**: Understand what code does
- **Optimization**: Improve code performance
- **Multi-Language**: Supports 13+ programming languages

## Supported Languages

Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, TypeScript, SQL, HTML, CSS

## Quick Start

```python
from coding_assistant.assistant import CodingAssistant

assistant = CodingAssistant()

# Generate code
code = assistant.generate_code("Create a function to sort a list")
print(code)

# Debug code
fixed = assistant.debug_code(buggy_code, error_message)
print(fixed)

# Review code
review = assistant.review_code(my_code)
print(review)

# Explain code
explanation = assistant.explain_code(code)
print(explanation)

# Optimize code
optimized = assistant.optimize_code(code)
print(optimized)
```

## API Reference

### CodingAssistant

- `generate_code(description, language)`: Generate code from description
- `debug_code(code, error, language)`: Fix code errors
- `review_code(code, language)`: Review code for issues
- `explain_code(code, language)`: Explain code functionality
- `optimize_code(code, language)`: Optimize for performance
- `suggest_improvements(code, language)`: Get improvement suggestions

## Usage Examples

### Generate a Python Function

```python
code = assistant.generate_code(
    "Create a function that validates email addresses",
    language="python"
)
```

### Debug and Fix Code

```python
buggy_code = "def add(a, b)\n    return a + b"
error = "SyntaxError: expected ':'"

fixed = assistant.debug_code(buggy_code, error, language="python")
```

### Review Code Quality

```python
my_code = """def calculate(x):
    result = x * 2
    return result"""

review = assistant.review_code(my_code)
print(review['review'])
print(f"Issues found: {review['issues_found']}")
```

## Requirements

- LLM model must be initialized and available
- Supports both online and offline LLMs
- Works with local LLaMA 2 or Mistral models
