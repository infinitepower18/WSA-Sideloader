from PIL import Image, ImageDraw
from PySimpleGUI import Button, BUTTON_TYPE_READ_FORM, FILE_TYPES_ALL_FILES, theme_background_color, theme_button_color
import io
import ctypes
from base64 import b64encode

def RoundedButton(button_text=' ', corner_radius=0, button_type=BUTTON_TYPE_READ_FORM, target=(None, None),
                  tooltip=None, file_types=FILE_TYPES_ALL_FILES, initial_folder=None, default_extension='',
                  disabled=False, change_submits=False, enable_events=False,
                  image_size=(None, None), image_subsample=None, border_width=None, size=(None, None),
                  auto_size_button=None, button_color=None, disabled_button_color=None, highlight_colors=None, 
                  mouseover_colors=(None, None), use_ttk_buttons=None, font=None, bind_return_key=False, focus=False, 
                  pad=None, key=None, right_click_menu=None, expand_x=False, expand_y=False, visible=True, 
                  metadata=None):
    if None in size:
        multi = int(4 * (ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100))
        size = (((len(button_text) if size[0] is None else size[0]) * 5 + 20) * multi,
                20 * multi if size[1] is None else size[1])
    if button_color is None:
        button_color = theme_button_color()
    btn_img = Image.new('RGBA', size, (0, 0, 0, 0))
    corner_radius = int(corner_radius/2*min(size))
    poly_coords = (
        (corner_radius, 0),
        (size[0] - corner_radius, 0),
        (size[0], corner_radius),
        (size[0], size[1] - corner_radius),
        (size[0] - corner_radius, size[1]),
        (corner_radius, size[1]),
        (0, size[1] - corner_radius),
        (0, corner_radius),
    )
    pie_coords = [
        [(size[0] - corner_radius * 2, size[1] - corner_radius * 2, size[0], size[1]),
         [0, 90]],
        [(0, size[1] - corner_radius * 2, corner_radius * 2, size[1]), [90, 180]],
        [(0, 0, corner_radius * 2, corner_radius * 2), [180, 270]],
        [(size[0] - corner_radius * 2, 0, size[0], corner_radius * 2), [270, 360]],
    ]
    brush = ImageDraw.Draw(btn_img)
    brush.polygon(poly_coords, button_color[1])
    for coord in pie_coords:
        brush.pieslice(coord[0], coord[1][0], coord[1][1], button_color[1])
    data = io.BytesIO()
    btn_img.thumbnail((size[0] // 3, size[1] // 3), resample=Image.LANCZOS)
    btn_img.save(data, format='png', quality=95)
    btn_img = b64encode(data.getvalue())
    return Button(button_text=button_text, button_type=button_type, target=target, tooltip=tooltip,
                  file_types=file_types, initial_folder=initial_folder, default_extension=default_extension,
                  disabled=disabled, change_submits=change_submits, enable_events=enable_events,
                  image_data=btn_img, image_size=image_size,
                  image_subsample=image_subsample, border_width=border_width, size=size,
                  auto_size_button=auto_size_button, button_color=(button_color[0], theme_background_color()),
                  disabled_button_color=disabled_button_color, highlight_colors=highlight_colors,
                  mouseover_colors=mouseover_colors, use_ttk_buttons=use_ttk_buttons, font=font,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key, right_click_menu=right_click_menu,
                  expand_x=expand_x, expand_y=expand_y, visible=visible, metadata=metadata)