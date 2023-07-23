#指令列表
from pathlib import Path

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

def main(lrc_data ,lrc_file):
    #定义FT格式开头四个数据
    ft_format = b'\x21\x09\x05\x14'
    #定义导出的歌词DSC等文件路径
    song_name = Path(lrc_file).stem
    dsc_file_name = song_name + "_lyric.dsc"
    dsc_file_name = Path("temp").joinpath(dsc_file_name)
    #os.path.join("temp",dsc_file_name)
    
    #写入FT谱面文件头数据
    dsc_file = open(dsc_file_name, 'wb+')
    dsc_file.write(ft_format)

    #读取lrc数据
    #使用hex函数转换成字符串，再利用文字位置去除开头的字符变成16位数据
    #由于lrc不支持设置颜色，因此默认设置为白色
    
    lyric_db_list = []
    last_id = 0
    for lyric in lrc_data:
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
        #歌词颜色，默认白色
        lyric_color_bytes = b'\xff\xff\xff\xff'
        #合并所有歌词数据
        lyric_bytes_data = lyric_op + lyric_id_bytes + lyric_color_bytes
        #写入DSC
        dsc_file.write(time_bytes_data + lyric_bytes_data)
        print(lyric["lyric"])
        if lyric["id"] < 1000 and lyric["id"] != 0 and last_id != lyric["id"]:
            last_id = lyric["id"]
            print(last_id)
            lyric_db_list.append({"id":"{:0>3}".format(str(lyric["id"])),
                                  "lyric":lyric['lyric']
                                  })
    dsc_file.close()

    return dsc_file_name,lyric_db_list