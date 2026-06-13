"""Media Processing Module - Image and video processing with AI enhancements."""

import os
from pathlib import Path
from typing import Optional, Tuple, List
from loguru import logger
import yaml
import numpy as np

try:
    import cv2
except ImportError:
    logger.warning("OpenCV not installed. Install with: pip install opencv-python")

try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    logger.warning("Pillow not installed. Install with: pip install Pillow")


class ImageProcessor:
    """Process and enhance images using AI and computer vision."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Image Processor.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        logger.info("Image Processor initialized")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def load_image(self, image_path: str) -> Optional[Image.Image]:
        """Load image from file.
        
        Args:
            image_path: Path to image file
            
        Returns:
            PIL Image object or None
        """
        try:
            img = Image.open(image_path)
            logger.info(f"Loaded image: {image_path}")
            return img
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return None
    
    def save_image(self, image: Image.Image, output_path: str) -> bool:
        """Save image to file.
        
        Args:
            image: PIL Image object
            output_path: Output file path
            
        Returns:
            True if successful
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            image.save(output_path)
            logger.info(f"Saved image: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return False
    
    def resize_image(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """Resize image to specified dimensions.
        
        Args:
            image: PIL Image object
            size: (width, height) tuple
            
        Returns:
            Resized image
        """
        resized = image.resize(size, Image.Resampling.LANCZOS)
        logger.info(f"Resized image to {size}")
        return resized
    
    def enhance_image(self, image: Image.Image, brightness: float = 1.0, 
                     contrast: float = 1.0, saturation: float = 1.0) -> Image.Image:
        """Enhance image brightness, contrast, and saturation.
        
        Args:
            image: PIL Image object
            brightness: Brightness factor (1.0 = original)
            contrast: Contrast factor (1.0 = original)
            saturation: Saturation factor (1.0 = original)
            
        Returns:
            Enhanced image
        """
        enhanced = image.convert('RGB')
        
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = enhancer.enhance(brightness)
        
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(enhanced)
            enhanced = enhancer.enhance(contrast)
        
        if saturation != 1.0:
            enhancer = ImageEnhance.Color(enhanced)
            enhanced = enhancer.enhance(saturation)
        
        logger.info("Image enhanced")
        return enhanced
    
    def apply_filter(self, image: Image.Image, filter_type: str) -> Image.Image:
        """Apply filter to image.
        
        Args:
            image: PIL Image object
            filter_type: Type of filter (blur, sharpen, edge, smoothen, detail)
            
        Returns:
            Filtered image
        """
        filters = {
            'blur': ImageFilter.BLUR,
            'sharpen': ImageFilter.SHARPEN,
            'edge': ImageFilter.EDGE_ENHANCE,
            'smoothen': ImageFilter.SMOOTH,
            'detail': ImageFilter.DETAIL
        }
        
        if filter_type not in filters:
            logger.warning(f"Unknown filter type: {filter_type}")
            return image
        
        filtered = image.filter(filters[filter_type])
        logger.info(f"Applied {filter_type} filter")
        return filtered
    
    def remove_background(self, image_path: str, output_path: str) -> bool:
        """Remove background from image (requires rembg library).
        
        Args:
            image_path: Path to input image
            output_path: Path to output image
            
        Returns:
            True if successful
        """
        try:
            from rembg import remove
            input_img = Image.open(image_path)
            output_img = remove(input_img)
            output_img.save(output_path)
            logger.info(f"Background removed and saved to {output_path}")
            return True
        except ImportError:
            logger.error("rembg library not installed. Install with: pip install rembg")
            return False
        except Exception as e:
            logger.error(f"Error removing background: {e}")
            return False


class VideoProcessor:
    """Process and edit videos."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Video Processor.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        logger.info("Video Processor initialized")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
        """Get video information.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video info
        """
        try:
            cap = cv2.VideoCapture(video_path)
            info = {
                'fps': int(cap.get(cv2.CAP_PROP_FPS)),
                'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
            }
            cap.release()
            logger.info(f"Retrieved video info: {info}")
            return info
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def trim_video(self, input_path: str, output_path: str, 
                   start_time: float, end_time: float) -> bool:
        """Trim video to specified time range.
        
        Args:
            input_path: Path to input video
            output_path: Path to output video
            start_time: Start time in seconds
            end_time: End time in seconds
            
        Returns:
            True if successful
        """
        try:
            import subprocess
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-ss', str(start_time),
                '-to', str(end_time),
                '-c', 'copy',
                output_path
            ]
            subprocess.run(cmd, check=True)
            logger.info(f"Video trimmed and saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error trimming video: {e}")
            return False
    
    def extract_frames(self, video_path: str, output_dir: str, 
                      every_n_frames: int = 30) -> List[str]:
        """Extract frames from video.
        
        Args:
            video_path: Path to video file
            output_dir: Directory to save frames
            every_n_frames: Extract every nth frame
            
        Returns:
            List of output frame paths
        """
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            cap = cv2.VideoCapture(video_path)
            frames = []
            frame_count = 0
            extracted_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % every_n_frames == 0:
                    frame_path = f"{output_dir}/frame_{extracted_count:04d}.jpg"
                    cv2.imwrite(frame_path, frame)
                    frames.append(frame_path)
                    extracted_count += 1
                
                frame_count += 1
            
            cap.release()
            logger.info(f"Extracted {extracted_count} frames")
            return frames
        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            return []
    
    def generate_subtitle(self, video_path: str, output_path: str) -> bool:
        """Generate subtitles for video (requires speech recognition).
        
        Args:
            video_path: Path to video file
            output_path: Path to output SRT file
            
        Returns:
            True if successful
        """
        try:
            logger.info("Subtitle generation requires advanced speech-to-text")
            logger.info("Consider using services like Google Cloud Speech-to-Text or AWS Transcribe")
            return False
        except Exception as e:
            logger.error(f"Error generating subtitles: {e}")
            return False


if __name__ == "__main__":
    # Example: Image processing
    img_processor = ImageProcessor()
    img = img_processor.load_image("sample.jpg")
    if img:
        enhanced = img_processor.enhance_image(img, brightness=1.2, contrast=1.1)
        img_processor.save_image(enhanced, "output.jpg")
    
    # Example: Video processing
    video_processor = VideoProcessor()
    info = video_processor.get_video_info("sample.mp4")
    print(f"Video Info: {info}")
