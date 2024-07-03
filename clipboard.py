import platform

def copy_image_to_clipboard(output):
    if platform.system() == 'Windows':
        import win32clipboard
        data = output.getvalue()[14:]  # Remove BMP header
        
        # Open the clipboard and set the data
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    else:
        pass