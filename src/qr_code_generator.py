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

from utils.file_loading import create_directory


########################################################################################################################
class RunID(Enum):
    F0 = "bkgNone_logoNone"
    F1 = "bkgNone_logoFloralBorderAndCenter"
    F2 = "bkgNone_logoFloralCenter"
    F3 = "bkgFloralBorderAndCenter_logoNone"
    F4 = "bkgFloralThickBorderAndCenter_logoNone"
    F5 = "bkgFloralBorder_logoNone"
    F6 = "bkgFloralThickBorder_logoNone"
    F7 = "bkgFloralThickBorder_logoFloralCenter"
    F8 = "bkgThickFloralBorder_logoWaves"


# TODO: you'll need to copy over the relevant files to the ../images/qrcode/blog/load
id_to_meta_files = {
    RunID.F0: {
        "background": None,
        "logo": None,
        "round_logo": False,
        "logo_radius": 2000,
    },

    RunID.F1: {
        "background": None,
        "logo": "final-polar-floral-borderAndCenter_dpi-600",
        "round_logo": True,
        "logo_radius": 2000,
    },

    RunID.F2: {
        "background": None,
        "logo": "final-polar-floral-center_dpi-600",
        "round_logo": True,
        "logo_radius": 2000,
    },

    RunID.F3: {
        "background": "final-polar-floral-borderAndCenter_dpi-600",
        "logo": None,
        "round_logo": False,
        "logo_radius": 2000,
    },

    RunID.F4: {
        "background": "final-polar-floral-thickBorderAndCenter_dpi-600",
        "logo": None,
        "round_logo": False,
        "logo_radius": 2000,
    },

    RunID.F5: {
        "background": "final-polar-floral-border_dpi-600",
        "logo": None,
        "round_logo": False,
        "logo_radius": 2000,
    },

    RunID.F6: {
        "background": "final-polar-floral-thickBorder_dpi-600",
        "logo": None,
        "round_logo": False,
        "logo_radius": 2000,
    },

    RunID.F7: {
        "background": "final-polar-floral-thickBorder_dpi-600",
        "logo": "final-polar-floral-center_dpi-600",
        "round_logo": True,
        "logo_radius": 2000,
    },

    RunID.F8: {
        "background": "final-polar-floral-thickBorder_dpi-600",
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
    # round an image. Taken from https://github.com/reegan-anne/python_qrcode/blob/main/main.ipynb
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
# TODO - SET PARAMETERS AS REQUIRED
data = sys.argv[1]  # whatever you want the qrcode to link to
SAVE = True
dpi = 600  # set dpi for higher resolution - important if you're gonna canvas print
box_size = 30  # higher box size = better quality image; use 50 for canvas print
ext = ".png"

load_dir = "../images/qrcode/blog/load/"
save_dir = "../images/qrcode/blog/save/"
create_directory(load_dir)
create_directory(save_dir)

########################################################################################################################
# for id in [RunID.F0]:
for id in RunID:
    ID = id
    save_name = ID.value

    round_radius = id_to_meta_files[ID]["logo_radius"]

    bkg_img = os.path.join(load_dir, id_to_meta_files[ID]["background"] + ext) \
        if (id_to_meta_files[ID]["background"] is not None) else None

    logo_img = os.path.join(load_dir, id_to_meta_files[ID]["logo"] + ext) \
        if (id_to_meta_files[ID]["logo"] is not None) else None

    rounded_logo_img = add_suffix_to_filepath(logo_img, "_rounded") if id_to_meta_files[ID]["round_logo"] else None

    print("bkg\t", bkg_img)
    print("logo\t", logo_img)
    print("rounded logo\t", rounded_logo_img)
    ####################################################################################################################

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

    # for module_drawer in [VerticalBarsDrawer]:
    for module_drawer in [RoundedModuleDrawer, CircleModuleDrawer, VerticalBarsDrawer,
                          SquareModuleDrawer, HorizontalBarsDrawer, GappedSquareModuleDrawer]:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, border=6, box_size=box_size)
        qr.add_data(data)

        # set background for qr code - will either be plain white or an image
        qr_img_colour_mask = {}
        if bkg_img:
            qr_img_colour_mask = {"color_mask": ImageColorMask(back_color=(1, 1, 1), color_mask_path=bkg_img)}

        qr_img = qr.make_image(image_factory=StyledPilImage,
                               module_drawer=module_drawer(),
                               embeded_image_path=logo_img,
                               **qr_img_colour_mask
                               )

        if SAVE:
            save_path = create_savepath(save_dir, save_name, module_drawer.__name__, dpi, ext)
            qr_img.save(save_path, dpi=(dpi, dpi))
            print(f"saved at: {save_path}")

print("completed")
qr_img.show()
