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

def main(ass_data ,ass_file,PV_ID):
    #定义FT格式开头四个数据
    ft_format = b'\x21\x09\x05\x14'
    #定义空歌词数据（默认使用0号歌词）
    null_lyric_bytes_data = b'\x18\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff'
    #定义导出的歌词DSC等文件路径
    song_name = Path(ass_file).stem
    dsc_file_name = song_name + "_lyric.dsc"
    dsc_file_name = Path("temp").joinpath(dsc_file_name)

    #写入FT谱面文件头数据
    with open(dsc_file_name, 'wb+') as dsc_file:
        dsc_file.write(ft_format)

    #读取ass数据
    #使用hex函数转换成字符串，再利用文字位置去除开头的字符变成16位数据
    #歌词颜色通过一个 全是数字 的 列表 转换为 字节数组 实现
    
    #创建歌词列表
    lyric_db_list = []
    #检测是否出现id重复
    last_id = 0
    for lyric in ass_data:
        #歌词开始时间
        start_time_op = b'\x01\x00\x00\x00'
        #将时间数据转换为16位数据
        start_time_data = hex(lyric["start"])[2:]
        start_time_bytes = data_to_byte(start_time_data)
        #将16位数据组合
        start_time_bytes_data = start_time_op + start_time_bytes
        #歌词指令头数据
        lyric_op = b'\x18\x00\x00\x00'
        #旧版歌词ID
        lyric_id_data = hex(lyric["id"])[2:]
        lyric_id_bytes = data_to_byte(lyric_id_data)
        #歌词颜色
        lyric_color_array = [lyric["B"],lyric["G"],lyric["R"],lyric["A"]]
        lyric_color_bytes = bytearray(lyric_color_array)
        #合并所有歌词数据
        lyric_bytes_data = lyric_op + lyric_id_bytes + lyric_color_bytes
        #写入DSC
        with open(dsc_file_name, 'ab+') as dsc_file:
            dsc_file.write(start_time_bytes_data + lyric_bytes_data)
            #检测是否时间轴中间有无歌词数据段
            #由于ass时间有结束时间，因此如果两个字幕结束时间和开始时间没有衔接就会变成空白字幕
            #我们需要为此添加一个检测，如果存在空白字幕则手动加入空白歌词
            #这里利用了 real_id 起始数值为 1 逐渐递增实现检测下一句歌词的开始时间
            #恁妈我为啥要这么写代码，太抽象了
            if lyric["real_id"] < len(ass_data) and lyric["end"] != ass_data[lyric["real_id"]]["start"]:
                #转换时间数据为16位数据
                start_time_data = hex(lyric["end"])[2:]
                start_time_bytes = data_to_byte(start_time_data)
                #添加头指令
                start_time_bytes_data = start_time_op + start_time_bytes
                #写入DSC
                dsc_file.write(start_time_bytes_data + null_lyric_bytes_data)
            #检测是否为最后一句歌词
            #原因同上
            elif lyric["real_id"] == len(ass_data):
                #转换时间数据为16位数据
                start_time_data = hex(lyric["end"])[2:]
                start_time_bytes = data_to_byte(start_time_data)
                #添加头指令
                start_time_bytes_data = start_time_op + start_time_bytes
                #写入DSC
                dsc_file.write(start_time_bytes_data + null_lyric_bytes_data)
        #将歌词数据写入歌词列表
            if lyric["id"] < 1000 and lyric["id"] != 0 and last_id != lyric["id"]:
                last_id = lyric["id"]
                print(last_id)
                lyric_db_list.append({"id":"{:0>3}".format(str(lyric["id"])),
                                    "lyric":lyric['lyric']
                                  })
    return dsc_file_name ,lyric_db_list