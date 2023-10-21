import os
import sys
from enum import Enum

import PIL
import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import ImageColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer, VerticalBarsDrawer, \
    SquareModuleDrawer, HorizontalBarsDrawer, GappedSquareModuleDrawer


########################################################################################################################
class RunID(Enum):
    F1 = "bkgThickFloral_logoFloral"
    F2 = "bkgThickFloral_logoFloralRound"
    F3 = "bkgFloralBorderAndCenter_logoNone"
    F4 = "bkgThickFloral_logoNone"
    F5 = "bkgThickFloral_logoWaves"


id_to_meta_files = {
    RunID.F1: {
        "background": "final-polar-thickBorder_dpi-600",
        "logo": "final-polar-floral-center_dpi-600",
        "round_logo": True,
        "logo_radius": 2000,
    },

    RunID.F2: {
        "background": "final-polar-thickBorder_dpi-600",
        "logo": "final-polar-floral-full-round_dpi-600",
        "round_logo": True,
        "logo_radius": 1400,
    },

    RunID.F3: {
        "background": "final-polar-borderAndCenter_dpi-600",
        "logo": None,
        "round_logo": False,
        "logo_radius": 2000,
    },

    RunID.F4: {
        "background": "final-polar-thickBorder_dpi-600",
        "logo": None,
        "round_logo": False,
        "logo_radius": 2000,
    },

    RunID.F5: {
        "background": "final-polar-thickBorder_dpi-600",
        "logo": "final-frequency-waves-overlapping_dpi-600",
        "round_logo": True,
        "logo_radius": 2000,
    },

}


########################################################################################################################
def add_suffix_to_filepath(filename, suffix):
    base, ext = os.path.splitext(filename)
    new_filename = f"{base}{suffix}{ext}"
    return new_filename


def add_corners(im, rad):
    # https://github.com/reegan-anne/python_qrcode/blob/main/main.ipynb
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def create_savepath(dir, filename, module_drawer, dpi, ext):
    return os.path.join(dir, f"qrcode_{filename}_dpi-{dpi}_{module_drawer}{ext}")


########################################################################################################################
ID = RunID.F2
save_name = ID.value
data = sys.argv[1]
SAVE = True
load_dir = "../images/qrcode/FINAL/"
save_dir = "../images/qrcode/FINAL/saved/"
ext = ".png"
dpi = 1200
round_radius = id_to_meta_files[ID]["logo_radius"]

bkg_img = os.path.join(load_dir, id_to_meta_files[ID]["background"] + ext) \
    if (id_to_meta_files[ID]["background"] is not None) else None

logo_img = os.path.join(load_dir, id_to_meta_files[ID]["logo"] + ext) \
    if (id_to_meta_files[ID]["logo"] is not None) else None

rounded_logo_img = add_suffix_to_filepath(logo_img, "_rounded") if id_to_meta_files[ID]["round_logo"] else None

if bkg_img is None:
    raise Exception("Need a file for background image! having no background isn't supported!")

print("bkg\t", bkg_img)
print("logo\t", logo_img)
print("rounded logo\t", rounded_logo_img)

########################################################################################################################

if not hasattr(PIL.Image, 'Resampling'):
    PIL.Image.Resampling = PIL.Image

# round center image if needed
if rounded_logo_img is not None:
    if not os.path.exists(rounded_logo_img):
        im = Image.open(logo_img)
        im = add_corners(im, round_radius)
        im.save(rounded_logo_img)
        print("saved rounded logo")

    logo_img = rounded_logo_img

# for module_drawer in [RoundedModuleDrawer]:
for module_drawer in [RoundedModuleDrawer, CircleModuleDrawer, VerticalBarsDrawer,
                      SquareModuleDrawer, HorizontalBarsDrawer, GappedSquareModuleDrawer]:
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, border=6, box_size=30)
    qr.add_data(data)
    qr_img = qr.make_image(image_factory=StyledPilImage,
                           module_drawer=module_drawer(),
                           embeded_image_path=logo_img,
                           color_mask=ImageColorMask(back_color=(1, 1, 1), color_mask_path=bkg_img),
                           )

    if SAVE:
        save_path = create_savepath(save_dir, save_name, module_drawer.__name__, dpi, ext)
        # set dpi for higher resolution
        qr_img.save(save_path, dpi=(dpi, dpi))
        print(f"saved at: {save_path}")


print("completed")
# qr_img.show()
