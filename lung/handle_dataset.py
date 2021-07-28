import numpy
import pydicom
import os
import SimpleITK as sitk
import pydicom_seg
from matplotlib import pyplot

if __name__ == '__main__':
    count = 0
    f = open('..\\result.txt', 'w')
    seg_array = numpy.array([0])
    file1 = ""  # ct
    file2 = ""  # seg
    origin = "D:\\summer\\NSCLC-Radiomics\\manifest-1603198545583\\NSCLC-Radiomics\\LUNG1-"  # todo 修改此处数据集路径
    seg_count = 0
    for i in range(1, 520):
        if i <= 422:
            number = origin + i.__str__().zfill(3)
            path1 = number + "\\" + os.listdir(number)[0]
            paths = os.listdir(path1)
            tmp1 = ""
            tmp2 = ""
            for path in paths:
                if "Segmentation" in path:  # 说明是分割文件目录
                    file2 = path1 + "\\" + path
                    tmp = os.listdir(file2)
                    if len(tmp) == 1:
                        file2 = file2 + "\\" + tmp[0]
                    else:
                        print("seg size fault")
                        exit()
                else:
                    if tmp1 != "":
                        tmp2 = path
                    else:
                        tmp1 = path
            if tmp1 < tmp2:
                file1 = path1 + "\\" + tmp1
            else:
                file1 = path1 + "\\" + tmp2
        else:
            k = i - 422
            if k == 9:
                continue
            number = "D:\\summer\\NSCLC-Radiogenomics\\manifest-1622561851074\\NSCLC Radiogenomics\\R01-" + k.__str__().zfill(3)  # todo 修改此处数据集路径
            path1 = number
            paths = os.listdir(number)
            for path in paths:
                if "PET" in path:
                    continue
                else:
                    path1 = path1 + "\\" + path
                    break
            paths = os.listdir(path1)
            for path in paths:
                if "seg" in path:
                    file2 = path1 + "\\" + path
                else:
                    file1 = path1 + "\\" + path

            paths = os.listdir(file2)
            if len(paths) != 1:
                print(k.__str__() + "R seg不为1")
            else:
                file2 = file2 + "\\" + paths[0]

        f.write(file1)
        f.write('\n')
        f.write(file2)
        f.write('\n')
        print(file1)
        print(file2)

        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(file1)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        image_array = sitk.GetArrayFromImage(image)

        pyplot.imshow(image_array[0])

        seg = pydicom.read_file(file2)

        seg_reader = pydicom_seg.SegmentReader()
        seg_list_p = seg_reader.read(seg)

        if len(seg_list_p.available_segments) == 1:
            seg_array = seg_list_p.segment_data(1)
        else:
            sign = 0
            for segment_number in seg_list_p.available_segments:
                info = seg_list_p.segment_infos[segment_number]["SegmentDescription"]
                # print(info.value)
                if "GTV" in info.value:
                    # 说明是肿瘤区域
                    sign = 1
                    print(info.value)
                    seg_count = seg_count + 1
                    seg_array = seg_list_p.segment_data(segment_number)
                    break
            if sign == 0:
                print(i.__str__() + "未找到seg")
                exit()

        if image_array.shape != seg_array.shape:
            print(str(i) + "CT和seg shape不一致")
            f.write(str(i) + "CT和seg shape不一致")
            f.write('\n')
        else:
            numpy.save("..\\cts\\ct" + count.__str__() + ".npy", image_array)
            numpy.save("..\\segs\\seg" + count.__str__() + ".npy", seg_array)
            print("存储了ct" + count.__str__())
            print("存储了seg" + count.__str__())
            f.write("存储了ct" + count.__str__())
            f.write('\n')
            f.write("存储了seg" + count.__str__())
            f.write('\n')
            count = count + 1
