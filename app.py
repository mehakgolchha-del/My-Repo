"""Flask web server - The main application that runs everything."""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from pathlib import Path
from loguru import logger
import yaml

# Import our AI modules
from modules.llm import AIBrain
from modules.code import CodeHelper
from modules.files import FileManager
from modules.analytics import FinanceTracker
from modules.media import MediaEditor

# Setup logging
logger.add("logs/app.log", rotation="500 MB")

# Create Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load configuration
with open('config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)

# Initialize all AI modules
logger.info("Initializing AI modules...")
try:
    ai_brain = AIBrain()
    code_helper = CodeHelper()
    file_manager = FileManager()
    finance_tracker = FinanceTracker()
    media_editor = MediaEditor()
    logger.info("✅ All modules initialized successfully!")
except Exception as e:
    logger.error(f"❌ Error initializing modules: {e}")
    ai_brain = None


# ============================================================
# ROUTES - What happens when you click buttons on the website
# ============================================================

@app.route('/')
def home():
    """Show the main chat page."""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user.
    
    Flow:
    1. User types message in browser
    2. Message sent to this function
    3. AI brain processes it
    4. Answer sent back to browser
    5. Answer shown to user
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        
        logger.info(f"User: {user_message}")
        
        # Get AI response
        if ai_brain:
            response = ai_brain.answer_question(user_message)
        else:
            response = "AI brain not initialized. Please check installation."
        
        logger.info(f"AI: {response}")
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/code-generator', methods=['GET'])
def code_generator():
    """Show code generator page."""
    return render_template('code.html')


@app.route('/generate-code', methods=['POST'])
def generate_code():
    """Generate code based on user description.
    
    Flow:
    1. User describes what code they want
    2. Sent to this function
    3. Code helper generates code
    4. Code shown to user with syntax highlighting
    """
    try:
        data = request.json
        description = data.get('description', '')
        language = data.get('language', 'python')
        
        logger.info(f"Generating {language} code for: {description}")
        
        if code_helper:
            code = code_helper.generate(description, language)
        else:
            code = "# Code generation not available"
        
        return jsonify({
            'success': True,
            'code': code,
            'language': language
        })
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/file-manager', methods=['GET'])
def file_manager():
    """Show file manager page."""
    return render_template('files.html')


@app.route('/list-files', methods=['POST'])
def list_files():
    """List files in a directory.
    
    Flow:
    1. User selects a folder
    2. Sent to this function
    3. Returns list of files
    4. Files displayed in browser
    """
    try:
        data = request.json
        directory = data.get('directory', '.')
        
        logger.info(f"Listing files in: {directory}")
        
        if file_manager:
            files = file_manager.list_files(directory)
        else:
            files = []
        
        return jsonify({
            'success': True,
            'files': files,
            'directory': directory
        })
    except Exception as e:
        logger.error(f"File listing error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/analytics', methods=['GET'])
def analytics():
    """Show analytics page."""
    return render_template('analytics.html')


@app.route('/get-balance', methods=['GET'])
def get_balance():
    """Get financial balance.
    
    Flow:
    1. User clicks "Get Balance" button
    2. Sent to this function
    3. Finance tracker calculates totals
    4. Results shown on page
    """
    try:
        if finance_tracker:
            balance = finance_tracker.get_balance()
        else:
            balance = {'income': 0, 'expenses': 0, 'balance': 0}
        
        return jsonify({
            'success': True,
            'data': balance
        })
    except Exception as e:
        logger.error(f"Balance error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/media', methods=['GET'])
def media():
    """Show media editor page."""
    return render_template('media.html')


@app.route('/edit-image', methods=['POST'])
def edit_image():
    """Edit an image.
    
    Flow:
    1. User uploads image
    2. Sent to this function
    3. Media editor processes it
    4. Edited image returned
    """
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        operation = request.form.get('operation', 'enhance')
        
        logger.info(f"Processing image with operation: {operation}")
        
        if media_editor and file:
            result = media_editor.process_image(file, operation)
            return jsonify({
                'success': True,
                'message': 'Image processed successfully',
                'result': result
            })
        else:
            return jsonify({'success': False, 'error': 'Media editor not available'}), 500
    except Exception as e:
        logger.error(f"Image processing error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Get system status.
    
    This shows if all AI modules are working properly.
    """
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'modules': {
            'ai_brain': ai_brain is not None,
            'code_helper': code_helper is not None,
            'file_manager': file_manager is not None,
            'finance_tracker': finance_tracker is not None,
            'media_editor': media_editor is not None
        }
    })


# ============================================================
# ERROR HANDLERS - What to show if something goes wrong
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """Show friendly error if page not found."""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Show friendly error if server has problem."""
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Server error. Check logs for details.'}), 500


# ============================================================
# START THE SERVER
# ============================================================

if __name__ == '__main__':
    # Create necessary directories
    Path('logs').mkdir(exist_ok=True)
    Path('uploads').mkdir(exist_ok=True)
    Path('templates').mkdir(exist_ok=True)
    Path('static').mkdir(exist_ok=True)
    
    logger.info("\n" + "="*50)
    logger.info("🚀 AI ASSISTANT SERVER STARTING")
    logger.info("="*50)
    logger.info(f"📱 Open your browser to: http://localhost:5000")
    logger.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*50 + "\n")
    
    # Start the web server
    # debug=True means the server reloads when you change code
    # threaded=True means it can handle multiple users
    app.run(
        host='localhost',
        port=5000,
        debug=True,
        threaded=True
    )
