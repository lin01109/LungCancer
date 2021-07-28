import numpy
from matplotlib import pyplot

if __name__ == '__main__':
    ct = numpy.load("..\\cts\\ct501.npy")
    seg = numpy.load("..\\segs\\seg501.npy")
    re = ct * seg

    for i in range(0, 109):
        for j in range(0, 512):
            for k in range(0, 512):
                if re[i][j][k] != 0:
                    print(i)
    # 输出的i对应的即为不为0的分割

    # 查看CT和分割是否相符合
    pyplot.imshow(ct[108], cmap='gray')
    pyplot.show()
    pyplot.imshow(re[108], cmap='gray')
    pyplot.show()

    # for i in range(99, 109):
    #     pyplot.imshow(ct[i], cmap='gray')
    #     pyplot.show()
    #     pyplot.imshow(re[i], cmap='gray')
    #     pyplot.show()
