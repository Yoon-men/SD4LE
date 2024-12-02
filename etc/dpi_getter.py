"""
DPI-Getter 

ver 1.0.0

> 사용자의 모니터 DPI를 얻어서 퍼센트로 변환해줍니다.

* get_dpi: 사용자 모니터의 DPI를 얻습니다.
* dpi_to_percent: DPI를 퍼센트로 변환합니다.

~ Thu, Sep 23, 2024 ~
"""

#* ------------------------------------------------------------ *#

import ctypes

#* ------------------------------------------------------------ *#


def get_dpi() -> int:
    """
    ## 사용자 모니터의 DPI를 얻습니다.
    """ 
    # 모니터 DPI 설정을 얻기 위한 준비
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    # 기본 모니터의 DPI를 얻음
    hdc = user32.GetDC(0)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88은 LOGPIXELSX의 값을 나타냄
    user32.ReleaseDC(0, hdc)
    
    return dpi


def dpi_to_percent(dpi: int) -> int: 
    """
    ## DPI를 퍼센트로 변환합니다.

    Windows 표준 DPI는 96입니다.

    예: 96 DPI -> 100%, 120 DPI -> 125%, 등등
    """
    return (dpi * 100) // 96



if __name__ == "__main__": 
    dpi = get_dpi()
    percent = dpi_to_percent(dpi)
    print(f"현재 배율은 {percent}%입니다.")