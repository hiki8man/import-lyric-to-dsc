import os,sys
from ass import ass_to_dsc, read_ass
from lrc import lrc_to_dsc, read_lrc
import dsc
import chart.option


def run(dsc_file_path ,lyric_file ,merge_dsc_file_path,PV_ID,color_lyric):
    os.chdir(sys.path[0])
    #check output folder
    exe_path = os.getcwd()
    output_path = os.path.join(exe_path,"temp")
    if os.path.isdir(output_path) == False:
        os.mkdir(output_path)
    print(output_path)

    print("Read dsc data......")
    dsc_data_list = dsc.read(dsc_file_path)
    print(len(dsc_data_list))
    print("Done!")

    print("Check music play offset......")
    lyric_offset = chart.option.get_music_offset(dsc_data_list)
    print("Done!")

    if color_lyric == 1:
        print("Read ass data......")
        ass_data = read_ass.read(lyric_file,lyric_offset)
        print("Done!")
        print("Convert ass to dsc......")
        lyric_dsc_file_name ,lyric_file_name = ass_to_dsc.main(ass_data ,lyric_file,PV_ID)
        print("Done!")
    else:
        print("Read lrc data......")
        lrc_data = read_lrc.read(lyric_file , color_lyric,lyric_offset)
        print("Done!")
        print("Convert lrc to dsc......")
        lyric_dsc_file_name ,lyric_file_name = lrc_to_dsc.main(lrc_data ,lyric_file,PV_ID)
        print("Done!")

    lyric_dsc_data_list = dsc.read(lyric_dsc_file_name)
    print("Delete old lyric......")
    no_lyric_dsc_data_list = chart.option.delete_lyric(dsc_data_list)
    print(len(no_lyric_dsc_data_list))
    print("Done!")
    #print(no_lyric_dsc_data_list[56])
    #pprint.pprint(no_lyric_dsc_data_list)
    print("Merge dsc data......")
    merge_dsc_data_list = chart.option.merge_dsc_data(no_lyric_dsc_data_list,lyric_dsc_data_list)
    #pprint.pprint(merge_dsc_data_list)
    print("Done!")

    print("Save merge dsc......")
    output_path_name = dsc.write(merge_dsc_data_list, merge_dsc_file_path)
    print("Done!")
    print("Output:\n" + merge_dsc_file_path)
    return lyric_file_name ,lyric_dsc_file_name