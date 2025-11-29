"""
Visual Forensics Utilities
Performs Error Level Analysis (ELA) and metadata extraction for image manipulation detection
"""

import os
from typing import Dict, Any
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
from loguru import logger


def perform_ela(image_path: str, quality: int = 90) -> str:
    """
    Perform Error Level Analysis on an image
    
    Args:
        image_path: Path to image file
        quality: JPEG quality for re-compression (default 90)
        
    Returns:
        Suspicion level: "low", "medium", or "high"
    """
    try:
        # Open original image
        original = Image.open(image_path)
        
        # Convert to RGB if needed
        if original.mode != 'RGB':
            original = original.convert('RGB')
        
        # Save with specified quality
        temp_path = "temp_ela.jpg"
        original.save(temp_path, 'JPEG', quality=quality)
        
        # Open re-compressed image
        compressed = Image.open(temp_path)
        
        # Calculate difference
        ela_image = ImageChops.difference(original, compressed)
        
        # Enhance for visibility
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        
        if max_diff == 0:
            suspicion = "low"
        else:
            scale = 255.0 / max_diff
            ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        # Convert to numpy for analysis
        ela_array = np.array(ela_image)
        
        # Calculate statistics
        mean_diff = np.mean(ela_array)
        std_diff = np.std(ela_array)
        max_pixel = np.max(ela_array)
        
        # Determine suspicion level based on thresholds
        if max_pixel > 180 or std_diff > 50:
            suspicion = "high"
        elif max_pixel > 120 or std_diff > 30:
            suspicion = "medium"
        else:
            suspicion = "low"
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        logger.info(f"ELA analysis: mean={mean_diff:.2f}, std={std_diff:.2f}, max={max_pixel}, suspicion={suspicion}")
        
        return suspicion
        
    except Exception as e:
        logger.error(f"ELA analysis failed: {e}")
        return "unknown"


def extract_metadata(image_path: str) -> Dict[str, Any]:
    """
    Extract EXIF metadata from image
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary of metadata
    """
    try:
        image = Image.open(image_path)
        
        metadata = {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "width": image.width,
            "height": image.height
        }
        
        # Try to get EXIF data
        exif_data = image.getexif()
        if exif_data:
            metadata["has_exif"] = True
            metadata["exif_tags_count"] = len(exif_data)
        else:
            metadata["has_exif"] = False
        
        return metadata
        
    except Exception as e:
        logger.error(f"Metadata extraction failed: {e}")
        return {"error": str(e)}


def analyze_image_forensics(image_path: str) -> Dict[str, Any]:
    """
    Perform comprehensive visual forensics analysis
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary with forensics results
    """
    suspicion_level = perform_ela(image_path)
    metadata = extract_metadata(image_path)
    
    return {
        "suspicion_level": suspicion_level,
        "metadata": metadata,
        "analysis_complete": True
    }


if __name__ == "__main__":
    # Test with a sample image
    test_image = "test_image.jpg"
    if os.path.exists(test_image):
        result = analyze_image_forensics(test_image)
        print(f"Forensics result: {result}")
    else:
        print("No test image found")
