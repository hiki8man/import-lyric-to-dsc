#指令列表
from chart import  op_list
list = op_list.list
common_list = {}
for common in list:
   common_list.update({common:list[common]})
   

ft_format = b'\x21\x09\x05\x14'
note_format = b'\x06\x00\x00\x00'
note_circle_hold = note_format + b'\x05\x00\x00\x00'
note_cross_hold  = note_format + b'\x06\x00\x00\x00'
note_square_hold = note_format + b'\x07\x00\x00\x00'
note_triangle_hold = note_format + b'\x04\x00\x00\x00'

import pprint
import os

#读入数据

def write(dsc_data_list, dsc_file_path):
    with open(dsc_file_path, 'wb') as fix_dsc:
        fix_dsc.write(ft_format)
        print(len(dsc_data_list))
        for data in dsc_data_list:
            if data["time"] != None: 
                fix_dsc.write(data["time"])
            for another_data in data["data"]:
                fix_dsc.write(another_data)
                
def read(dsc_file_name):
    with open(dsc_file_name, 'rb') as read_file_dsc:
        read_dsc = read_file_dsc.read()
        dsc_data = []
        for data in read_dsc:
            dsc_data.append(data)
        dsc_format = bytearray(dsc_data[0:4])
        if dsc_format != ft_format:
            print("not ft dsc")
            sys.exit(0)
        else:
            dsc_data_list=[]
            dsc_id = 4
            data_id = -1
        while dsc_id < len(dsc_data):
            opcode_id = dsc_data[dsc_id]
            if opcode_id == 1:
                data_id += 1
                dsc_data_time = bytearray(dsc_data[dsc_id:dsc_id+8])
                dsc_data_list.append({
                                      "time":dsc_data_time,
                                      "data":[]
                                    })
            else:
                if data_id == -1:
                    data_id += 1
                    dsc_data_list.append({
                                          "time":None,
                                          "data":[]
                                        })
                another_end_id = dsc_id + (common_list[opcode_id]["len"] + 1) * 4
                dsc_data_another = bytearray(dsc_data[dsc_id:another_end_id])
                dsc_data_list[data_id]["data"].append(dsc_data_another)
            dsc_id += (common_list[opcode_id]["len"] + 1) * 4
    return dsc_data_list
