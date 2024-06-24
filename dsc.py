#指令列表
#import op_list
from chart import  op_list
list = op_list.list
common_list = {}
for common in list:
   common_list.update({common:list[common]})
   
#写入思路1（使用字符）
#byte_val = bytes(chr(1),encoding="latin1")
#dsc_ft = b'\x21\x09\x05\x14'
#test=b'\x00'
#bitout = open('test.dsc', 'wb')
#bitout.write(dsc_ft+byte_val+test*7)
#bitout.close

#写入思路2（使用字节数组写入）
#byte_val = bytes(bytearray([1,2,3,16]))
#dsc_ft = b'\x21\x09\x05\x14'
#test=b'\x00'
#bitout = open('test.dsc', 'wb')
#print(byte_val)
#bitout.write(dsc_ft+byte_val+test*7)
#bitout.close

#修正使用了 Nas 的编辑器导致头部格式错误而无法使用的BUG
#标准的FT格式DSC头部为列表中第一项，但Nas的编辑器在保存时使用了第二项从而导致原有代码无法正常检测
ft_format = [b'\x21\x09\x05\x14',
             b'\x17\x25\x12\x15',
             b'\x18\x20\x06\x11',
             b'\x21\x01\x03\x16',
             b'\x18\x17\x02\x15',
             b'\x18\x13\x03\x14',
             b'\x16\x23\x01\x14',
             b'\x22\x15\x08\x13',
             b'\x21\x31\x01\x13']

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
        fix_dsc.write(ft_format[0])
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
        if ft_format.count(dsc_format) == 0:
            raise ValueError("it's only support FT format")
        else:
            dsc_data_list=[]
            dsc_id = 4
            data_id = -1
        while dsc_id < len(dsc_data):
            opcode_id = dsc_data[dsc_id]
            if opcode_id == 1:
                data_id += 1
                #将指令与指令对应的内容同时保存至列表
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