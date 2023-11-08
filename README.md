# Audio Art

---
Audio Art is a project containing a collection of scripts which can convert audio to pieces of art. 

**Want to know more?** Checkout my blog post!

Examples of the types of art works that can be generated are shown below. 
Each image was generated using the same audio file!

| **Script**                                                                   | **Image**                                                                                                                                   |
|------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| [frequency_waves_overlapping.py](src%2Ffrequency_waves_overlapping.py)       | ![final-frequency-waves-overlapping_dep-600.png](images%2Ffreq-waves-overlapping%2Ffinal-frequency-waves-overlapping_dpi-600.png)           |
| [polar_slices.py](src%2Fpolar_slices.py)                                     | ![final-polar-slices_dpi-600.png](images%2Fpolar-slices%2Ffinal-polar-slices_dpi-600.png)                                                   |
| [polar_floral_full.py](src%2Fpolar_floral_full.py)                           | ![final-polar-floral-center-round_dpi-600.png](images%2Fpolar-floral-full%2Ffinal-polar-floral-center-round_dpi-600.png)                    |
| [polar_floral_segments_circle.py](src%2Fpolar_floral_segments_circle.py)     | ![final-polar-floral-segments-circle_dpi-600.png](images%2Fpolar-floral-segments-circle%2Ffinal-polar-floral-segments-circle_dpi-600.png)   |
| [polar_floral_border_and_center.py](src%2Fpolar_floral_border_and_center.py) | ![final-polar-floral-borderAndCenter_dpi-600.png](images%2Fpolar-floral-border-and-center%2Ffinal-polar-floral-borderAndCenter_dpi-600.png) |

## Scannable Art - QR Code
You also have the option to integrate your art with a QR code linked to any weblink/text you want! 

Script: [qr_code_generator.py](src%2Fqr_code_generator.py)

Example: 

![qrcode_bkgThickFloralBorder_logoWaves_dpi-600_VerticalBarsDrawer.png](images%2Fqrcode%2Fblog%2Fsave%2Fqrcode_bkgThickFloralBorder_logoWaves_dpi-600_VerticalBarsDrawer.png)

---
# Installation

1) Clone the repo
2) Create a venv
3) Activate venv
4) `pip install -r requirements.txt`
5) Find the script you want and run it! 
---

# Notes

- Visualisations require wav format. 
  - To convert ogg to wav format requires using pydub
    - To use pydub requires installing ffmpeg (follow https://www.wikihow.com/Install-FFmpeg-on-Windows)
    - For conversion use: [ogg2wav.py](src%2Futils%2Fogg2wav.py)
--- 
# TODO
- add interactive plots? embed in blog/ jupyter notebook? 
- create cmmd line script executions 
- Use config files for scripts 

---

