"""PC Automation Module - Control applications, files, and system tasks."""

import os
import subprocess
import platform
import shutil
from pathlib import Path
from typing import List, Optional
from loguru import logger
import yaml


class PCAutomation:
    """Automate PC tasks like app control, file management, and screenshots."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize PC Automation.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.system = platform.system()
        logger.info(f"PC Automation initialized on {self.system}")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def open_application(self, app_name: str) -> bool:
        """Open an application.
        
        Args:
            app_name: Name of application to open
            
        Returns:
            True if successful
        """
        try:
            if self.system == "Windows":
                os.startfile(app_name)
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
            elif self.system == "Linux":
                subprocess.Popen([app_name])
            logger.info(f"Opened application: {app_name}")
            return True
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            return False
    
    def close_application(self, app_name: str) -> bool:
        """Close an application.
        
        Args:
            app_name: Name of application to close
            
        Returns:
            True if successful
        """
        try:
            if self.system == "Windows":
                os.system(f"taskkill /IM {app_name}.exe")
            elif self.system == "Darwin":
                os.system(f"pkill -f {app_name}")
            elif self.system == "Linux":
                os.system(f"pkill -f {app_name}")
            logger.info(f"Closed application: {app_name}")
            return True
        except Exception as e:
            logger.error(f"Error closing application: {e}")
            return False
    
    def take_screenshot(self, output_path: str = "./screenshots") -> Optional[str]:
        """Take a screenshot.
        
        Args:
            output_path: Directory to save screenshot
            
        Returns:
            Path to screenshot or None
        """
        try:
            from PIL import ImageGrab
            Path(output_path).mkdir(exist_ok=True)
            
            filename = f"{output_path}/screenshot_{int(__import__('time').time())}.png"
            screenshot = ImageGrab.grab()
            screenshot.save(filename, quality=self.config['automation']['screenshot_quality'])
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
    
    def get_file_list(self, directory: str, extension: Optional[str] = None) -> List[str]:
        """Get list of files in directory.
        
        Args:
            directory: Directory path
            extension: Filter by file extension (e.g., '.txt')
            
        Returns:
            List of file paths
        """
        try:
            files = []
            for file in Path(directory).iterdir():
                if file.is_file():
                    if extension is None or file.suffix == extension:
                        files.append(str(file))
            logger.info(f"Found {len(files)} files in {directory}")
            return files
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    def copy_file(self, source: str, destination: str) -> bool:
        """Copy a file.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful
        """
        try:
            shutil.copy2(source, destination)
            logger.info(f"Copied {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file.
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if successful
        """
        try:
            Path(file_path).unlink()
            logger.info(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    def get_system_info(self) -> dict:
        """Get system information.
        
        Returns:
            Dictionary with system info
        """
        import psutil
        return {
            "os": self.system,
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    
    def control_volume(self, level: int) -> bool:
        """Control system volume.
        
        Args:
            level: Volume level 0-100
            
        Returns:
            True if successful
        """
        try:
            if self.system == "Windows":
                from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    ISimpleAudioVolume._iid_, 0, None
                )
                volume = interface.QueryInterface(ISimpleAudioVolume)
                volume.SetMasterVolume(level / 100, None)
            logger.info(f"Volume set to {level}%")
            return True
        except Exception as e:
            logger.error(f"Error controlling volume: {e}")
            return False


if __name__ == "__main__":
    automation = PCAutomation()
    
    # Example: Take screenshot
    automation.take_screenshot()
    
    # Example: Get system info
    info = automation.get_system_info()
    print(f"System Info: {info}")
    
    # Example: List files
    files = automation.get_file_list(".")
    print(f"Files: {files[:5]}")
