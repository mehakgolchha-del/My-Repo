"""Media Processing Documentation."""

# Media Processing Module

Process and enhance images and videos using OpenCV, PIL, and AI techniques.

## Features

### Image Processing
- **Image Enhancement**: Adjust brightness, contrast, saturation
- **Filtering**: Apply blur, sharpen, edge detection, smoothing
- **Resizing**: Resize images to any dimensions
- **Background Removal**: Remove backgrounds from images
- **Format Support**: JPG, PNG, BMP, WEBP

### Video Processing
- **Video Info**: Get FPS, frame count, resolution, duration
- **Trimming**: Cut videos to specific time ranges
- **Frame Extraction**: Extract frames at intervals
- **Subtitle Generation**: Auto-generate subtitles (with external service)

## Quick Start

```python
from media_processing.processor import ImageProcessor, VideoProcessor

# Image processing
img_proc = ImageProcessor()
img = img_proc.load_image("photo.jpg")
enhanced = img_proc.enhance_image(img, brightness=1.2, contrast=1.1)
img_proc.save_image(enhanced, "enhanced.jpg")

# Video processing
video_proc = VideoProcessor()
info = video_proc.get_video_info("video.mp4")
print(info)

# Trim video
video_proc.trim_video("video.mp4", "trimmed.mp4", 10, 30)

# Extract frames
frames = video_proc.extract_frames("video.mp4", "./frames", every_n_frames=30)
```

## API Reference

### ImageProcessor

- `load_image(path)`: Load image from file
- `save_image(image, path)`: Save image to file
- `resize_image(image, size)`: Resize to (width, height)
- `enhance_image(image, brightness, contrast, saturation)`: Enhance image
- `apply_filter(image, filter_type)`: Apply filter (blur, sharpen, edge, smoothen, detail)
- `remove_background(input_path, output_path)`: Remove background

### VideoProcessor

- `get_video_info(path)`: Get video properties
- `trim_video(input, output, start, end)`: Trim video
- `extract_frames(path, output_dir, every_n_frames)`: Extract frames
- `generate_subtitle(input, output)`: Generate subtitles

## Installation

```bash
# Install FFmpeg (required for video operations)
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows (using Chocolatey)
choco install ffmpeg

# Optional: Background removal
pip install rembg
```

## Filter Types

- `blur`: Blur the image
- `sharpen`: Sharpen edges
- `edge`: Detect and enhance edges
- `smoothen`: Smooth the image
- `detail`: Enhance details

## Notes

- Video operations require FFmpeg to be installed
- Subtitle generation requires external speech-to-text service
- Maximum image size: 4096x4096 (configurable)
