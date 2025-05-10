import re

# Open the raw stream file in binary mode
with open('stream.raw', 'rb') as f:
    data = f.read()

# Define JPEG start (FFD8) and end (FFD9) markers
jpeg_start = b'\xFF\xD8'
jpeg_end = b'\xFF\xD9'

# Find all start and end positions of JPEG images
start_positions = [m.start() for m in re.finditer(jpeg_start, data)]
end_positions = [m.start() + 2 for m in re.finditer(jpeg_end, data)]

# Extract each JPEG and save it as a separate file
for i, (start, end) in enumerate(zip(start_positions, end_positions)):
    with open(f'frame_{i}.jpg', 'wb') as f_out:
        f_out.write(data[start:end])
    print(f"Saved frame_{i}.jpg")
