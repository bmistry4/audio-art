import os

from PIL import Image, ImageOps, ImageDraw, ImageFont

########################################################################################################################
border_thickness = 3
font_size = 25

folder_path = "../../images/polar-floral-segments-circle"
ext = '.png'

########################################################################################################################
id_to_filenames = {
    1: ['1-sparsify-random', '1-sparsify-random-drop', '1-sparsify-random-drop-window-and-random'],
    2: ['2-radii-offset-0', '2-radii-offset-1'],
    3: ['3-binsNum-1', '3-binsNum-2', '3-binsNum-5', '3-binsNum-10', '3-binsNum-15', '3-binsNum-20'],
    4: ['4-binsSize-50', '4-binsSize-100', '4-binsSize-200', '4-binsSize-300', '4-binsSize-400', '4-binsSize-500'],
    5: ['5-colours-0', '5-colours-1', '5-colours-2', '5-colours-3']
}

id_to_subplot_titles = {
    1: ['random', 'drop', 'window-and-random'],
    2: ['radii-offset = 0', 'radii-offset = 1'],
    3: ['No. bins = 1', 'No. bins = 2', 'No. bins = 5', 'No. bins = 10', 'No. bins = 15', 'No. bins = 20'],
    4: ['Bin size = 50', 'Bin size = 100', 'Bin size = 200', 'Bin size = 300', 'Bin size = 400', 'Bin size = 500'],
    5: ['', '', '', '']
}

id_to_savename = {
    1: "1-sparsify",
    2: "2-radii-offset",
    3: "3-binsNum",
    4: "4-binSize",
    5: "5-colours",
}

id_to_grid_size = {
    1: (1, 3),
    2: (1, 2),
    3: (2, 3),
    4: (2, 3),
    5: (2, 2)
}


########################################################################################################################
def file_names_to_paths(filenames, root=folder_path, extension=ext):
    return list(map(lambda x: os.path.join(root, x + extension), filenames))


def image_grid(imgs, rows, cols, titles):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size  # assume all imgs are same size
    grid = Image.new('RGB', size=(
        cols * w + (2 * border_thickness * len(images)),
        rows * h + (2 * border_thickness * len(images)))
                     )

    for i, img in enumerate(imgs):
        # add boarder
        img = ImageOps.expand(img, border=border_thickness, fill='black')
        # add title
        Im = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", font_size)
        Im.text((w / 2 - len(titles[i] * 5), h / 2 - font_size / 2), titles[i], fill=(0, 0, 0), font=font)
        # add to grid (final image)
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


########################################################################################################################

if __name__ == '__main__':

    id_to_filenames = {k: file_names_to_paths(v) for k, v in id_to_filenames.items()}

    for id in id_to_filenames.keys():
        images = [Image.open(x) for x in id_to_filenames[id]]
        new_im = image_grid(images, *id_to_grid_size[id], id_to_subplot_titles[id])

        # new_im.show()
        new_im.save(os.path.join(folder_path, id_to_savename[id]) + ext)
