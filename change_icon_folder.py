import ctypes
from ctypes import POINTER, Structure, c_wchar, c_int, sizeof, byref
from ctypes.wintypes import BYTE, WORD, DWORD, LPWSTR
import win32api
HICON = c_int
LPTSTR = LPWSTR
TCHAR = c_wchar
MAX_PATH = 260
FCSM_ICONFILE = 0x00000010
FCS_FORCEWRITE = 0x00000002
SHGFI_ICONLOCATION = 0x000001000


class GUID(Structure):
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE * 8)]


class SHFOLDERCUSTOMSETTINGS(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('dwMask', DWORD),
        ('pvid', POINTER(GUID)),
        ('pszWebViewTemplate', LPTSTR),
        ('cchWebViewTemplate', DWORD),
        ('pszWebViewTemplateVersion', LPTSTR),
        ('pszInfoTip', LPTSTR),
        ('cchInfoTip', DWORD),
        ('pclsid', POINTER(GUID)),
        ('dwFlags', DWORD),
        ('pszIconFile', LPTSTR),
        ('cchIconFile', DWORD),
        ('iIconIndex', c_int),
        ('pszLogo', LPTSTR),
        ('cchLogo', DWORD)]


class SHFILEINFO(Structure):
    _fields_ = [
        ('hIcon', HICON),
        ('iIcon', c_int),
        ('dwAttributes', DWORD),
        ('szDisplayName', TCHAR * MAX_PATH),
        ('szTypeName', TCHAR * 80)]


def set_icon(folderpath, iconpath):
    shell32 = ctypes.windll.shell32
    fcs = SHFOLDERCUSTOMSETTINGS()
    fcs.dwSize = sizeof(fcs)
    fcs.dwMask = FCSM_ICONFILE
    fcs.pszIconFile = iconpath
    fcs.cchIconFile = 0
    fcs.iIconIndex = 0
    hr = shell32.SHGetSetFolderCustomSettings(byref(fcs), folderpath,
                                              FCS_FORCEWRITE)
    if hr:
        raise WindowsError(win32api.FormatMessage(hr))
    sfi = SHFILEINFO()
    hr = shell32.SHGetFileInfoW(folderpath, 0, byref(sfi), sizeof(sfi),
                                SHGFI_ICONLOCATION)
    if hr == 0:
        raise WindowsError(win32api.FormatMessage(hr))
    index = shell32.Shell_GetCachedImageIndexW(sfi.szDisplayName, sfi.iIcon, 0)
    shell32.SHUpdateImageW(sfi.szDisplayName, sfi.iIcon, 0, index)
