#coding:utf-8
from appJar import gui
import main
from pathlib import Path
import traceback
import os
import cutlet
import unidic_lite

def convert_to_romaji(text):
    cutlet.Cutlet('nihon')
    katsu = cutlet.Cutlet()
    result = katsu.romaji(text,capitalize=False, title=False)
    return result

def open_file(name):
    print(name, "press")
    if name == "歌词文件...":
        ass_path = win.openBox("选择要导入的歌词文件......",fileTypes=[('ass、lrc或ppd歌词文件', ['*.ass','*.lrc','kasi.txt'])])
        if ass_path != "":
            print(ass_path)
            win.setEntry("歌词文件路径：",ass_path)
    elif name == "dsc文件...":
        dsc_path = win.openBox("选择要导入的dsc文件......",fileTypes=[('dsc文件', '*.dsc')])
        if dsc_path != "":
            if dsc_path != win.getEntry("导出文件路径: "):
                print(dsc_path)
                win.setEntry("dsc文件路径：",dsc_path)
            else:
                win.errorBox("错误","选择的文件不能与要导出的DSC文件路径重复！")
    elif name == "保存到.....":
        dsc_path = win.saveBox("设置合并完成后dsc保存路径......",fileTypes=[('dsc文件', '*.dsc')])
        if dsc_path != "":
            if dsc_path != win.getEntry("dsc文件路径："):
                print(dsc_path)
                win.setEntry("导出文件路径: ",dsc_path)
            else:
                win.errorBox("错误","导出的dsc文件名不能与导入的dsc文件名重复！")
    elif name == "导入歌词字幕":
        ass_path = win.getEntry("歌词文件路径：")
        dsc_path = win.getEntry("dsc文件路径：")
        save_path = win.getEntry("导出文件路径: ")

        use_lyric_en = win.getCheckBox("使用Lyric_en")
        add_mega_db = win.getCheckBox("自动添加Mega39+需要的空白Lyric db")
        use_cutlet = win.getCheckBox("使用cutlet添加罗马音歌词")

        PV_ID = win.getSpinBox("PV_ID")
        if len(PV_ID) < 3:
            PV_ID = "{:0>3}".format(str(PV_ID))

        if ass_path[-3:] == "ass":
            color_lyric = 1
        elif ass_path[-3:] == "lrc":
            color_lyric = 0
        elif ass_path[-8:] == "kasi.txt":
            color_lyric = -1
        if ass_path == "" or Path(ass_path).exists() == False:
            win.errorBox("错误","歌词文件路径错误！")
        elif dsc_path == "" or Path(dsc_path).exists() == False:
            win.errorBox("错误","DSC文件路径错误！")
        elif save_path == "" or (Path(save_path).parent).exists() == False:
            win.errorBox("错误","导出文件路径错误！")
        else:
            try:
                lyric_list ,lyric_dsc_file_name = main.run(dsc_path,ass_path,save_path,PV_ID,color_lyric)
                win.setLabel("check","导入成功")

                lyric_file_name = Path(ass_path).stem
                lyric_temp = ""
                lyric_en_temp = ""

                for lyric in lyric_list:
                    if use_lyric_en:
                        lyric_en_temp += f"pv_{PV_ID}.lyric_en.{lyric['id']}={lyric['lyric']}\n"
                        if add_mega_db:
                            lyric_temp += f"pv_{PV_ID}.lyric.{lyric['id']}=\n"
                    else:
                        lyric_temp += f"pv_{PV_ID}.lyric.{lyric['id']}={lyric['lyric']}\n"
                        if use_cutlet:
                            romaji_temp = convert_to_romaji(lyric['lyric'])
                            lyric_en_temp += f"pv_{PV_ID}.lyric_en.{lyric['id']}={romaji_temp}\n"
                        elif add_mega_db:
                            lyric_en_temp += f"pv_{PV_ID}.lyric_en.{lyric['id']}=\n"
                lyric_temp = f"#{lyric_file_name}\n{lyric_temp}{lyric_en_temp}"
                lyric_txt_path = Path("temp/lyric.txt")
                with open(lyric_txt_path, "w", encoding="UTF-8") as f:
                    f.write(lyric_temp)
                os.startfile(lyric_txt_path)
                win.infoBox("提示","请手动复制弹出的txt里面的歌词db")
            except:
                r = traceback.format_exc()
                win.errorBox("错误",f"未知错误！\n\n{r}")
                win.setLabel("check","导入失败")
            else:
                Path(lyric_txt_path).unlink()
                Path(lyric_dsc_file_name).unlink()
                Path("temp").rmdir()

win = gui("导入歌词字幕")
win.setSize("400x200")
win.setResizable(False)

win.addLabel("check","初始化完成",0,0,3)

win.addLabelEntry("歌词文件路径：",1,0,2)
win.addLabelEntry("dsc文件路径：",2,0,2)
win.addLabelEntry("导出文件路径: ",3,0,2)
win.addLabel("use_PV_ID","PV_ID: ",4,0)
win.addSpinBoxRange("PV_ID", 1, 9999,4,1)
win.setSpinBox("PV_ID", 900, callFunction=True)

win.addButton("歌词文件...",open_file,1,2)
win.addButton("dsc文件...",open_file,2,2)
win.addButton("保存到.....",open_file,3,2)
win.addButton("导入歌词字幕",open_file,4,2)

win.startLabelFrame("Mega39+用选项",5,0,3)
win.addCheckBox("使用Lyric_en",6,0,3)
win.addCheckBox("自动添加Mega39+需要的空白Lyric db",7,0,3)
win.addCheckBox("使用cutlet添加罗马音歌词",8,0,3)
win.stopLabelFrame()

win.go()