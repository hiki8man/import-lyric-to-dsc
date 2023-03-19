#指令列表
import os

#处理时间
#将数据转换为dsc标准数据
def data_to_byte(data):
    add_zero = 8 - len(data)
    if add_zero < 0:
        print("Error")
    else:
        data = ("0" * add_zero) + data
    if add_zero < 2:
        data_array = [
                       int(data[-2:] ,16),
                       int(data[-4:-2] ,16),
                       int(data[-6:-4] ,16),
                       int(data[-8:-6] ,16)
                     ]
    elif add_zero < 4:
        data_array = [
                       int(data[-2:] ,16),
                       int(data[-4:-2] ,16),
                       int(data[-6:-4] ,16),
                       0
                     ]
    elif add_zero < 6:
        data_array = [
                       int(data[-2:] ,16),
                       int(data[-4:-2] ,16),
                       0,
                       0
                     ]
    elif add_zero < 8:
        data_array = [
                       int(data[-2:] ,16),
                       0,
                       0,
                       0
                     ]
    data_bytes = bytearray(data_array)
    return data_bytes

def main(ass_data ,ass_file,PV_ID):
    id = 1
    to_dsc = []
    #定义FT格式开头四个数据
    ft_format = b'\x21\x09\x05\x14'
    #定义空歌词数据（默认使用0号歌词）
    null_lyric_bytes_data = b'\x18\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff'
    #定义导出的歌词DSC等文件路径
    song_name = os.path.splitext(os.path.basename(ass_file))[0]
    dsc_file_name = song_name + "_lyric.dsc"
    #dsc_file_name = os.path.join("output",dsc_file_name)
    dsc_file_name = os.path.join("temp",dsc_file_name)
    lyric_file_name = song_name + "_lyric_db.txt"
    #lyric_file_name = os.path.join("output",lyric_file_name)
    lyric_file_name = os.path.join("temp",lyric_file_name)
    #写入FT谱面文件头数据
    with open(dsc_file_name, 'wb+') as dsc_file:
        dsc_file.write(ft_format)
    #写入pv_db注释开头
    with open(lyric_file_name, 'w' ,encoding='UTF-8') as lyric_file:
        lyric_file.write("#" + song_name + "\n")

    #读取ass数据
    #使用hex函数转换成字符串，再利用文字位置去除开头的字符变成16位数据
    #歌词颜色通过一个 全是数字 的 列表 转换为 字节数组 实现
    
    #检测是否出现id重复
    last_id = 0
    
    for lyric in ass_data:
        #歌词开始时间
        time_op = b'\x01\x00\x00\x00'
        time_data = hex(lyric["time"])[2:]
        time_bytes = data_to_byte(time_data)
        time_bytes_data = time_op + time_bytes
        #歌词指令头数据
        lyric_op = b'\x18\x00\x00\x00'
        #旧版歌词ID
        lyric_id_data = hex(lyric["id"])[2:]
        lyric_id_bytes = data_to_byte(lyric_id_data)
        #歌词颜色
        lyric_color_bytes = b'\xff\xff\xff\xff'
        #合并所有歌词数据
        lyric_bytes_data = lyric_op + lyric_id_bytes + lyric_color_bytes
        #写入DSC
        with open(dsc_file_name, 'ab+') as dsc_file:
            dsc_file.write(time_bytes_data + lyric_bytes_data)
        #旧版写入pv_db
        print(lyric["lyric"])
        with open(lyric_file_name, 'a' ,encoding='UTF-8') as lyric_file:
            if lyric["id"] != last_id:
                last_id = lyric["id"]
                if lyric["id"] == 0:
                    print("Null Lyric")
                elif lyric["id"] < 1000:
                    lyric_id = "{:0>3}".format(str(lyric["id"]))
                    lyric_file.write(f"pv_{PV_ID}.lyric.{lyric_id}={lyric['lyric']}")
                else:
                    print("id out of range")
    return dsc_file_name ,lyric_file_name