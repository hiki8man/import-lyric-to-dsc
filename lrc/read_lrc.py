#指令列表

def read(lrc_file,is_lrc_flie,lyric_offset):
    with open(lrc_file, 'r' ,encoding='UTF-8') as lyric_file:
        lyric_list = lyric_file.readlines()
        id = 0
        lyric_data = []
        #如果源文件为 lrc 则 is_lrc_flie 为 0
        #如果源文件为 ppd歌词文件 则 is_lrc_flie 为 -1
        #同时 lrc 和 ppd歌词文件区别在于开头有无 中括号，因此 +1 获取时间开头位置
        is_lrc_lyric = is_lrc_flie + 1
        for lyric_o_data in lyric_list:
            #print(lyric_o_data)
            if lyric_o_data[is_lrc_lyric:is_lrc_lyric+1].isdigit() == True:
                #print(list)
                #构建数据结构
                lyric_data.append({ "real_id":id+1,
                                    "time":0,
                                    "lyric":""
                                 })
                
                if is_lrc_lyric == 1:
                    print("lrc Type")
                    lyric_data[id]["time"] = convert_time(lyric_o_data[1:lyric_o_data.find("]")]) + lyric_offset
                    lyric_data[id]["lyric"] = lyric_o_data[lyric_o_data.find("]")+1:]
                elif is_lrc_lyric == 0:
                    print("PPD Type")
                    lyric_data[id]["time"] = convert_time_PPD(lyric_o_data[:lyric_o_data.find(":")]) + lyric_offset
                #print(lyric_data[id]["lyric"])
                #去除每行的换行符
                try:
                    if lyric_data[id]["lyric"][-1] == "\n":
                        lyric_data[id]["lyric"] = lyric_data[id]["lyric"][:-1]
                except:
                    print("Last emply lyric")
                #空歌词跳过
                if lyric_data[id]["lyric"] == "\n" or lyric_data[id]["lyric"] == "":
                    lyric_data[id]["id"] = 0
                    lyric_data[id]["lyric"] = ""
                #第一句非空歌词标号
                elif id == 0:
                    lyric_data[id]["id"] = 1
                else:
                    #遍历寻找非空歌词id
                    for i in range(1,id+1):
                        #寻找没有空歌词的部分
                        if lyric_data[id-i]["lyric"] != "":
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

                id += 1
    return lyric_data

def convert_time(time):
    time_m = int(time[0:2]) * 60 * 1000 * 100
    time_s = float(time[3:])
    time_ms = time_s * 1000 * 100
    time = int(time_m + time_ms)
    return time

def convert_time_PPD(time):
    time_s = float(time)
    time_ms = time_s * 1000 * 100
    time = int(time_ms)
    return time