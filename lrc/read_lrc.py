#指令列表

def read(lrc_file,is_lrc_flie):
    with open(lrc_file, 'r' ,encoding='UTF-8') as lyric_file:
        lyric_list = lyric_file.readlines()
        id = 0
        lyric_data = []
        is_lrc_lyric = 1
        for lyric_o_data in lyric_list:
            print(lyric_o_data.find("["))
            if is_lrc_flie == -1:
                is_lrc_lyric = 0
            if lyric_o_data[is_lrc_lyric:is_lrc_lyric+2].isdigit() == True:
                #使用逗号分隔 ass文件 不同数据部分
                #print(list)
                #构建数据结构
                lyric_data.append({ "real_id":id+1,
                                    "time":0,
                                    "lyric":""
                                 })
                if is_lrc_lyric == 1:
                    lyric_data[id]["time"] = convert_time(lyric_o_data[1:lyric_o_data.find("]")])
                    lyric_data[id]["lyric"] = lyric_o_data[lyric_o_data.find("]")+1:]
                elif is_lrc_lyric == 0:
                    lyric_data[id]["time"] = convert_time_PPD(lyric_o_data[1:lyric_o_data.find(":")])
                    lyric_data[id]["lyric"] = lyric_o_data[lyric_o_data.find(":")+1:]
                #空歌词跳过
                if lyric_data[id]["lyric"] == "\n" or lyric_data[id]["lyric"] == "":
                    lyric_data[id]["id"] = 0
                #第一句非空歌词标号
                elif id == 0:
                    lyric_data[id]["id"] = 1
                else:
                    #遍历寻找非空歌词id
                    for i in range(1,id+1):
                        #寻找没有空歌词的部分
                        if lyric_data[id-i]["lyric"] != "\n":
                            #检测当前歌词是否与上一句歌词重复
                            #根据情况设置ID值，摆烂直接浅复制值，反正小工具要啥效率
                            if lyric_data[id]["lyric"] == lyric_data[id-i]["lyric"]:
                                lyric_data[id]["id"] = lyric_data[id-i]["id"]
                                break
                            else:
                                lyric_data[id]["id"] = lyric_data[id-i]["id"] + 1
                                break
                        #前面全是空歌词则赋予初始值1
                        elif lyric_data[id-i]["lyric"] == "\n" and (id - i) == 0:
                            lyric_data[id]["id"] = 1
                print(lyric_data[id]["id"])
                id += 1
    return lyric_data

def convert_time(time):
    time_m = int(time[0:2]) * 60 * 100 * 10
    time_s = float(time[3:])
    time_ms = time_s * 100 * 10
    time = int(time_m + time_ms) * 100
    return time

def convert_time_PPD(time):
    time_s = float(time[3:])
    time_ms = time_s * 100 * 10
    time = int(time_ms) * 100
    return time