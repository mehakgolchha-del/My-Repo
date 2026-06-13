"""File Manager - Manage your files and folders."""

from pathlib import Path
from loguru import logger
import os


class FileManager:
    """Manage files and directories."""
    
    def __init__(self):
        """Initialize the file manager."""
        logger.info("📁 File Manager initializing...")
        logger.info("✅ File Manager ready!")
    
    def list_files(self, directory: str = '.') -> list:
        """List all files in a directory.
        
        Args:
            directory: The folder to list files from
            
        Returns:
            List of files and folders
        """
        try:
            logger.info(f"📂 Listing files in: {directory}")
            files = []
            
            # Get list of items in directory
            for item in Path(directory).iterdir():
                # Create a simple list of file info
                info = {
                    'name': item.name,
                    'type': 'folder' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else 0
                }
                files.append(info)
            
            logger.info(f"✅ Found {len(files)} items")
            return files
        except Exception as e:
            logger.error(f"❌ Error listing files: {e}")
            return []
    
    def create_folder(self, folder_name: str, parent: str = '.') -> bool:
        """Create a new folder.
        
        Args:
            folder_name: Name of the folder to create
            parent: Parent directory
            
        Returns:
            True if successful
        """
        try:
            path = Path(parent) / folder_name
            path.mkdir(exist_ok=True)
            logger.info(f"✅ Created folder: {path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating folder: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful
        """
        try:
            Path(file_path).unlink()
            logger.info(f"✅ Deleted file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error deleting file: {e}")
            return False


if __name__ == "__main__":
    fm = FileManager()
    files = fm.list_files('.')
    for f in files:
        print(f)
