import os
from PIL import Image

def optimize_images():
    images_dir = os.path.join("static", "images")
    if not os.path.exists(images_dir):
        print(f"Directory {images_dir} does not exist!")
        return

    # List of images to skip deleting (or skip converting)
    # We will convert everything but we can keep logo.png as png just in case, but convert to webp too.
    keep_originals = ["logo.png", "logo (2).png", "hasnain.jfif"]

    supported_extensions = (".png", ".jpg", ".jpeg", ".jfif")
    
    total_saved = 0
    
    for filename in os.listdir(images_dir):
        if filename.lower().endswith(supported_extensions) and not filename.lower().endswith(".webp"):
            original_path = os.path.join(images_dir, filename)
            
            # Skip if it is a directory
            if os.path.isdir(original_path):
                continue
                
            name_without_ext = os.path.splitext(filename)[0]
            webp_filename = f"{name_without_ext}.webp"
            webp_path = os.path.join(images_dir, webp_filename)
            
            original_size = os.path.getsize(original_path)
            
            try:
                with Image.open(original_path) as img:
                    # Convert to RGB if it has RGBA and we want a standard webp
                    # WebP supports alpha, so we keep RGBA if the format supports it, otherwise convert to RGB.
                    if img.mode in ('RGBA', 'LA') and filename.lower().endswith(('.jpg', '.jpeg')):
                        # JPEGs don't support alpha, but if we save as webp, it supports alpha.
                        pass
                    
                    # Save as webp with optimization
                    img.save(webp_path, "WEBP", quality=80, optimize=True)
                    
                webp_size = os.path.getsize(webp_path)
                saved_bytes = original_size - webp_size
                total_saved += saved_bytes
                
                reduction = (saved_bytes / original_size) * 100
                print(f"Converted: {filename} ({original_size/1024:.1f} KB) -> {webp_filename} ({webp_size/1024:.1f} KB) | Reduction: {reduction:.1f}%")
                
                # Delete original if it's not in the keep list and we saved space
                if filename not in keep_originals and webp_size < original_size:
                    os.remove(original_path)
                    print(f"  Removed original: {filename}")
                    
            except Exception as e:
                print(f"Error converting {filename}: {e}")
                
    print(f"\nOptimization completed! Total space saved: {total_saved / (1024*1024):.2f} MB")

if __name__ == "__main__":
    optimize_images()
