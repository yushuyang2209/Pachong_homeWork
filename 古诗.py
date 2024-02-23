'''
@Project ：爬虫作业 
@File    ：古诗.py
@IDE     ：PyCharm 
@Author  ：于舒洋
@Date    ：2024/2/19 14:31 
'''
import time




def readfile(filename):
    try:
        f = open(filename, "r",encoding="utf-8")

        try:
            contents = []
            while True:
                content = f.readline()
                # print(content)
                if len(content) == 0:
                    break
                contents.append(content)
            return contents
        finally:
            f.close()
            print("文件关闭")
    except Exception as  result :
        print(result)


def writefile(filename,contents):
    try:
        f = open(filename, "w",encoding="utf-8")
        try:
            for content in contents:
                f.write(content)
            print("复制完毕")
        finally:
            f.close()

    except Exception as result:
        print(result)



if __name__ == '__main__':
    f = open("gushi.txt","w",encoding="utf-8")
    f.write("    出塞 \n  唐  王昌龄 \n秦时明月汉时关， \n万里长征人未还。\n但使龙城飞将在，\n不教胡马度阴山。")
    f.close()
    time.sleep(2)
    contents = readfile("gushi.txt")
    print(contents)
    writefile("copy.txt",contents)
    # f = open("copy.txt","r")
    # print(f.readlines())



