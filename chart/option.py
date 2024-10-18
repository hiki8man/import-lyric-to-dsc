from pprint import pprint
END_command = b"\x00\x00\x00\x00"

def change_hold_note_show(dsc_data_list):
    num = 0
    fix_dsc_data_list = dsc_data_list.copy()

    op_note_circle_hold   = b'\x06\x00\x00\x00\x05\x00\x00\x00'
    op_note_cross_hold    = b'\x06\x00\x00\x00\x06\x00\x00\x00'
    op_note_square_hold   = b'\x06\x00\x00\x00\x07\x00\x00\x00'
    op_note_triangle_hold = b'\x06\x00\x00\x00\x04\x00\x00\x00'

    for time_data in dsc_data_list:
        list_temp1_hold = [[],[],[],[]]
        list_temp2_hold = []
        list_temp = []
        for i in range(len(time_data["data"])):
            check_hold_note = time_data["data"][i][0:8]
            if check_hold_note == op_note_circle_hold:
                list_temp1_hold[0].append(time_data["data"][i])
            elif check_hold_note == op_note_cross_hold:
                list_temp1_hold[1].append(time_data["data"][i])
            elif check_hold_note == op_note_square_hold:
                list_temp1_hold[2].append(time_data["data"][i])
            elif check_hold_note == op_note_triangle_hold:
                list_temp1_hold[3].append(time_data["data"][i])
            else:
                list_temp.append(time_data["data"][i])
        for i in list_temp1_hold:
            if len(i) > 0:
                list_temp2_hold += i
        list_temp.extend(list_temp2_hold)
        if len(list_temp2_hold) != 0:
            fix_dsc_data_list[num]["data"] = list_temp.copy()
        num += 1
    return fix_dsc_data_list
    
def delete_lyric(dsc_data_list):
    op_lyric = b'\x18\x00\x00\x00'
    num = 0
    fix_dsc_data_list_temp = []
    #导入dsc
    for data in dsc_data_list:
        #建立空白
        fix_dsc_data_list_temp.append({"time":"no","data":[]})
        #检测是否有歌词
        for check_lyric in data["data"]:
            #没有则写入
            if check_lyric[0:4] != op_lyric:
                fix_dsc_data_list_temp[num]["data"].append(check_lyric)
        if len(fix_dsc_data_list_temp[num]["data"]) != 0:
            fix_dsc_data_list_temp[num]["time"] = data["time"]
        num += 1
    fix_dsc_data_list = []
    for write_data in fix_dsc_data_list_temp:
        if write_data["time"] != "no":
            fix_dsc_data_list.append(write_data)
    return fix_dsc_data_list

def get_music_offset(dsc_data_list):
    op_music_play = b'\x19\x00\x00\x00'
    music_play_offset = -1
    #遍历查询
    for data in dsc_data_list:
        #寻找music_play指令
        for i in range(len(data["data"])):
            if data["data"][i] == op_music_play:
                #转换为int
                music_play_offset = int.from_bytes(data["time"][4:] ,byteorder='little')
                break
        if music_play_offset != -1:
            break
    if music_play_offset == -1:
        music_play_offset = 0
    print(music_play_offset)
    return music_play_offset
'''
def merge_dsc_data(input_dsc=[],input_ass=[]):
    merge_dsc_data_list = []
    merge_temp2 = []
    i = 0
    for dsc_data in input_dsc:
        if len(input_ass) > i and dsc_data["time"] != None:
            time_dsc = int.from_bytes(dsc_data["time"][4:] ,byteorder='little')
            time_lyric = int.from_bytes(input_ass[i]["time"][4:] ,byteorder='little')
            if time_dsc < time_lyric:
                merge_temp2.append(dsc_data)
                #print("a")
            else:
                for time_lyric2 in input_ass[i:]:
                    time_lyric = int.from_bytes(time_lyric2["time"][4:] ,byteorder='little')
                    if time_dsc > time_lyric:
                        merge_temp2.append(input_ass[i])
                        i += 1
                        #print("c")
                    elif time_dsc == time_lyric:
                        merge_temp = (input_ass[i])
                        #merge_temp.append(input_ass[i])
                        merge_temp["data"] += dsc_data["data"].copy()
                        merge_temp2.append(merge_temp)
                        i += 1
                        #print("b")
                        break
                    else:
                        merge_temp2.append(dsc_data)
                        #print("exit")
                        break
            if i == len(input_ass):
                merge_temp2.append(dsc_data)
                #print("e")
        else:
            merge_temp2.append(dsc_data)
            #print("d")
    for b in merge_temp2:
        merge_dsc_data_list.append(b)
    return merge_dsc_data_list
'''

def merge_dsc_data(_data1=[],_data2=[]):
    (FstData, SecData) = __get_dsc_data_order(_data1, _data2)
    MergeDSCData = []
    i = 0
    for dsc_data1 in FstData:
        if dsc_data1["time"] == None or i >= len(SecData):
            MergeDSCData.append(dsc_data1)
            continue
        if i == 0 and SecData[i]["time"] == None:
            MergeDSCData.append(SecData[i])
            i += 1
        if __CompareDscTimeSize(dsc_data1,SecData[i]) >= 0:
            for dsc_data2 in SecData[i:]:
                compare_size = __CompareDscTimeSize(dsc_data1,dsc_data2)
                if compare_size > 0:
                    MergeDSCData.append(dsc_data2)
                    i += 1
                    if i >= len(SecData):
                        MergeDSCData.append(dsc_data1)
                elif compare_size == 0:
                    MergeDSCData.append(dsc_data2)
                    MergeDSCData[-1]["data"] += dsc_data1["data"].copy()
                    i += 1
                    break
                else:
                    MergeDSCData.append(dsc_data1)
                    break
        else:
            MergeDSCData.append(dsc_data1)
    
    return MergeDSCData
        
def __RemoveEND(_data):
    Last_command = []
    for command in _data[-1]["data"]:
        if command != END_command:
            Last_command.append(command)
    if len(Last_command) != 0:
        _data[-1]["data"] = Last_command
        return _data
    else:
        return _data[:-1]

def __CompareDscTimeSize(_data1, _data2):
    time1 = int.from_bytes(_data1["time"][4:] ,byteorder='little')
    time2 = int.from_bytes(_data2["time"][4:] ,byteorder='little')
    if time1 > time2:
        return 1
    elif time1 == time2:
        return 0
    else:
        return -1


def __get_dsc_data_order(_data1, _data2):
    if __CompareDscTimeSize(_data1[-1], _data2[-1]) > 0:
        data2 = __RemoveEND(_data2)
        return (_data1, _data2)
    else:
        data1 = __RemoveEND(_data1)
        return (_data2, _data1)


