import win32clipboard
import cStringIO
import base64
import pyperclip
from PIL import Image
from PIL import ImageGrab


def get_image_from_clipboard():
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        return img
    return None

def get_image_from_hdrop():
    win32clipboard.OpenClipboard()
    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_HDROP):
        files = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        img = None
        try:
            img = Image.open(files[0])
        except IOError:
            pass
    win32clipboard.CloseClipboard()
    return img

def main():
    if img := get_image_from_clipboard() or get_image_from_hdrop():
        img_buffer = cStringIO.StringIO()
        try:
            img.save(img_buffer, format="PNG")
            img_str = 'data:image/png;base64,' + str(base64.b64encode(img_buffer.getvalue()))
            pyperclip.copy(img_str)
        except IOError:
            pass
        img_buffer.close()

if __name__ == '__main__':
    main()
