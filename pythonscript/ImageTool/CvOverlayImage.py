
import cv2 as cv
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
# from PIL.Image import core as _imaging


class CvOverlayImage(object):
    """
    [summary]
      OpenCV形式の画像に指定画像を重ねる
    """

    def __init__(self):
        pass

    @classmethod
    def overlay(
            cls,
            cv_background_image,
            cv_overlay_image,
            point,
    ):
        """
        [summary]
          OpenCV形式の画像に指定画像を重ねる
        Parameters
        ----------
        cv_background_image : [OpenCV Image]
        cv_overlay_image : [OpenCV Image]
        point : [(x, y)]
        Returns : [OpenCV Image]
        """
        overlay_height, overlay_width = cv_overlay_image.shape[:2]

        # OpenCV形式の画像をPIL形式に変換(α値含む)
        # 背景画像
        cv_rgb_bg_image = cv.cvtColor(cv_background_image, cv.COLOR_BGR2RGB)
        pil_rgb_bg_image = Image.fromarray(cv_rgb_bg_image)
        pil_rgba_bg_image = pil_rgb_bg_image.convert('RGBA')
        # オーバーレイ画像
        cv_rgb_ol_image = cv.cvtColor(cv_overlay_image, cv.COLOR_BGRA2RGBA)
        pil_rgb_ol_image = Image.fromarray(cv_rgb_ol_image)
        pil_rgba_ol_image = pil_rgb_ol_image.convert('RGBA')

        # composite()は同サイズ画像同士が必須のため、合成用画像を用意
        pil_rgba_bg_temp = Image.new('RGBA', pil_rgba_bg_image.size,
                                     (255, 255, 255, 0))
        # 座標を指定し重ね合わせる
        pil_rgba_bg_temp.paste(pil_rgba_ol_image, point, pil_rgba_ol_image)
        result_image = Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)

        # OpenCV形式画像へ変換
        cv_bgr_result_image = cv.cvtColor(np.asarray(result_image), cv.COLOR_RGBA2BGRA)

        return cv_bgr_result_image

if __name__ == '__main__':
    basepath = "/home/shoda/Documents/mitsu"
    # cv_background_image = Image.open("pythonscript/ImageTool/ninja_hashiru.png")
    
    tiffimg = Image.open(basepath + '/depth/0000000001.tiff')
    tiffimg.save(basepath + '/tp_depth/0000000001.png', 'png')

    tiffimg = Image.open(basepath + '/tp_depth/0000000001.png')
    rgb_im = tiffimg.convert('RGB') 
    rgb_im.save(basepath + '/tp_depth/0000000001.jpeg', 'jpeg')

    cv_overlay_image = Image.open(basepath + "/tp_depth/0000000001.jpeg")
    cv_overlay_rimage = cv_overlay_image.copy()
    cv_overlay_rimage.putalpha(192)
    cv_overlay_rimage.save(basepath + "/tp_depth/0000000001trans.png")

    point = (0, 0)

    fig_origin = cv.imread(basepath + "/regi_clean/0000000001.jpg")
    fig_fixed = cv.imread(basepath + "/regi_clean_fixed/0000000000.jpg")
    fig_depth = cv.imread(basepath + "/tp_depth/0000000001trans.png", -1)

    image = CvOverlayImage.overlay(fig_origin, fig_depth, point)
    image2 = CvOverlayImage.overlay(fig_fixed, fig_depth, point)

    cv.imshow("origin", image)
    cv.imshow("fixed", image2)
    cv.imwrite(basepath + '/diff_origin.png',image)
    cv.imwrite(basepath + '/diff_fixed.png',image2)
    cv.waitKey(0)
    cv.destroyAllWindows() 
