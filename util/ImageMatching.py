import cv2
import aircv as ac

# 图片匹配工具类
class ImageMatching():

    # 图片匹配
    def Matching(self, imsrcPath, imobjPath):
        imsrc = ac.imread(imsrcPath)
        imobj = ac.imread(imobjPath)

        # find the match position
        pos = ac.find_template(imsrc, imobj)
        if (pos != None):
            return True
        else:
            return False

# print circle_center_pos
def draw_circle(img):
    imsrc = ac.imread('E:\\SelfWork\\python\ADBcontroller\\resource\\expect\\source.png')
    imobj = ac.imread('E:\\SelfWork\\python\ADBcontroller\\resource\\expect\\success.png')

    # find the match position
    pos = ac.find_template(imsrc, imobj)
    if (pos != None):
        # circle_center_pos = pos['result']
        circle_center_pos = tuple(list(map(int, list(pos['result']))))
        circle_radius = 50
        color = (0, 255, 0)
        line_width = 10

        cv2.circle(img, pos, circle_radius, color, line_width)

        cv2.copyTo()
        cv2.imshow('objDetect', imsrc)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("未找到特征点！")

