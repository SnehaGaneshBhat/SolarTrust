
import requests

url = (
    "https://maps.googleapis.com/maps/api/staticmap"
    "?center=22.5726,88.3639&zoom=20&size=640x640&maptype=satellite"
    "&key=AIzaSyBEFWNa28eYqCylLzCDLW9cn4xsjiqRNng"  # Replace with your actual key
)

response = requests.get(url)
print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))

# Optional: Save the image if successful
if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
    with open("test_image.jpg", "wb") as f:
        f.write(response.content)
    print("✅ Image saved as test_image.jpg")
else:
    print("❌ Failed to fetch image")
    print("Response:", response.text)