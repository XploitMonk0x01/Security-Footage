# Security Footage CTF Challenge

## Description

Last night, someone broke into our office and destroyed the hard drives containing our security footage. Fortunately, we captured the network traffic during the incident in a PCAP file. Your task is to recover the security footage and find the flag hidden within it. The footage might reveal clues about the intruder, but be warned—the office server (`http://10.10.203.65`) hosting `album.php` and `image.php` might hold additional secrets. Can you piece together the evidence and capture the flag?

**Hint 1**: The PCAP contains a stream of images—look for a protocol that streams security footage. (50 points)  

## Requirements

- **Tools**:
  - Wireshark or `tshark` (for PCAP analysis)
  - `tcpflow` (optional, for extracting streams)
  - Python 3 (for extracting JPEG frames)
  - `ffmpeg` (for reconstructing footage)
  - `vlc` or another media player (to play the footage)
- **Environment**:
  - AttackBox or a Linux environment with the above tools installed
  - Access to the server at `http://10.10.203.65`

## Files

- [security-footage-1648933966395.pcap](./security-footage-1648933966395.pcap): The PCAP file containing network traffic from the security camera.
- [extract_jpegs.py](./extract_jpegs.py): Python script to extract JPEG frames from the MJPEG stream.

## Solution

### Step 1: Analyze the PCAP File
Open the PCAP file in Wireshark to inspect the network traffic:

```bash
wireshark security-footage-1648933966395.pcap
```

- Use the filter `http` to find HTTP traffic.
- Look for a TCP stream with `Content-Type: multipart/x-mixed-replace; boundary=BoundaryString`, indicating an MJPEG stream (common for security cameras).
- Follow the TCP stream (right-click > Follow > TCP Stream), switch to “Raw” mode, and save it as `stream.raw`.

### Step 2: Extract JPEG Frames
The MJPEG stream contains JPEG images separated by boundaries. Use the provided Python script to extract the frames:

```bash
python3 extract_jpegs.py
```

This script reads `stream.raw`, identifies JPEG markers (`FFD8` to `FFD9`), and saves each frame as `frame_0.jpg`, `frame_1.jpg`, etc. Verify the frames:

```bash
ls frame_*.jpg
file frame_0.jpg
```

### Step 3: Reconstruct and Play the Footage
Combine the frames into a playable video using `ffmpeg`:

```bash
ffmpeg -framerate 10 -i frame_%d.jpg -c:v libx264 -pix_fmt yuv420p footage.mp4
vlc footage.mp4
```

Watch the footage for a visible flag, such as a sign or object displaying `flag{security_camera}`.

---

