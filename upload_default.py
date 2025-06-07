import cloudinary
import cloudinary.uploader
import cloudinary.api

# Konfigurera Cloudinary med dina uppgifter
cloudinary.config(
    cloud_name = "do0tj36bv",
    api_key = "791417521195131",
    api_secret = "NyY4sGy2bq1eSWNnKvD_biAnpvc"
)

# Ange sökväg till din lokala bild
local_image_path = r'C:\Users\awamn\OneDrive\Desktop\default_sewing_card.webp'

# Ladda upp bilden till Cloudinary
result = cloudinary.uploader.upload(
    local_image_path,
    public_id = 'handcrafts_defaults/default_sewing_card',
    overwrite = True,
    resource_type = "image"
)

print("Upload successful! URL:")
print(result['secure_url'])
