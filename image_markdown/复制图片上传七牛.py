import win32clipboard
import cStringIO
import base64
import pyperclip
from PIL import Image
from PIL import ImageGrab
import qiniu
import datetime
import json

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

def upload(img_buf):
    keys = json.load(file("auth.json"))
    ak = keys['access_key']
    sk = keys['secret_key']
    bucket_name = keys['bucket_name']
    au = qiniu.Auth(ak, sk)
    token = au.upload_token(bucket_name)
    file_name = datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f") + '.png'
    if keys["sub_path"]:
        file_name = keys["sub_path"] + '/' + file_name
    ret, info = qiniu.put_data(token, file_name, img_buf.getvalue())
##    print ret
##    print info
    ret_str = ''
    if ret is not None:
        ret_str = keys["domain"] + '/' + ret['key']
    print ret_str
    return ret_str

def main():
    img = get_image_from_clipboard()
    if not img:
        img = get_image_from_hdrop()
    if img:
        img_buffer = cStringIO.StringIO()
        try:
            img.save(img_buffer, format="PNG")
            #img_str = '![](data:image/png;base64,%s)' % str(base64.b64encode(img_buffer.getvalue()))
            img_str = upload(img_buffer)
            if img_str:
                #print img_str
                pyperclip.copy(img_str)
        except IOError:
            pass
        img_buffer.close()

if __name__ == '__main__':
    main()
