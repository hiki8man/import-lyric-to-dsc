def change_hold_note_show(dsc_data_list):
    num = 0
    fix_dsc_data_list = dsc_data_list.copy()
    for time_data in dsc_data_list:
        list_temp1_hold = [0,0,0,0]
        list_temp2_hold = []
        list_temp = []
        for i in range(len(time_data["data"])):
            check_hold_note = time_data["data"][i][0:8]
            if check_hold_note == note_circle_hold:
                list_temp1_hold[0] = time_data["data"][i]
            elif check_hold_note == note_cross_hold:
                list_temp1_hold[1] = time_data["data"][i]
            elif check_hold_note == note_square_hold:
                list_temp1_hold[2] = time_data["data"][i]
            elif check_hold_note == note_triangle_hold:
                list_temp1_hold[3] = time_data["data"][i]
            else:
                list_temp.append(time_data["data"][i])
        for i in list_temp1_hold:
            if i != 0:
                list_temp2_hold.append(i)
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
            else:
                for time_lyric2 in input_ass[i:]:
                    time_lyric = int.from_bytes(time_lyric2["time"][4:] ,byteorder='little')
                    if time_dsc > time_lyric:
                        merge_temp2.append(input_ass[i])
                        i += 1
                    elif time_dsc == time_lyric:
                        merge_temp = (input_ass[i])
                        #merge_temp.append(input_ass[i])
                        merge_temp["data"] += dsc_data["data"].copy()
                        merge_temp2.append(merge_temp)
                        i += 1
                        break
                    else:
                        merge_temp2.append(dsc_data)
                        break
            if i == len(input_ass):
                merge_temp2.append(dsc_data)
        else:
            merge_temp2.append(dsc_data)
    for b in merge_temp2:
        merge_dsc_data_list.append(b)
    return merge_dsc_data_list
