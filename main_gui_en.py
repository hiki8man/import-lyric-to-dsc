#coding:utf-8
from appJar import gui
import main
from pathlib import Path
import traceback
import os
import pykakasi

def convert_to_romaji(text):
    kks = kakasi.kakasi()
    result_list = kks.convert(text)
    result = ""
    result_len = len(result_list)
    num = 0
    symbols = (
	'、', '。', '’', 
	'”', '｛', '｝',
	'「', '」', 'ー',
	'＝', '_', '+',
	'/', '*', '-',
	'(', ')',
    " ","　",
    "'","?","？"
    )
    for i in result_list:
        num += 1
        result += i['hepburn']
        if num < result_len and result_list[num]['hepburn'] in symbols:
            result += ""
        elif i['hepburn'][-1] not in symbols:
            result += " "
    return result

def open_file(name):
    print(name, "press")
    if name == "Lyric File...":
        ass_path = win.openBox("Select you want to import lyric file......",fileTypes=[('ASS,LRC,PPD Lyric File', ['*.ass','*.lrc','kasi.txt'])])
        if ass_path != "":
            print(ass_path)
            win.setEntry("Lyric Path:",ass_path)
    if name == "DSC File...":
        dsc_path = win.openBox("Select you want to import dsc file......",fileTypes=[('DSC File', '*.dsc')])
        if dsc_path != "":
            if dsc_path != win.getEntry("Output Path:"):
                print(dsc_path)
                win.setEntry("DSC Path:",dsc_path)
            else:
                win.errorBox("Error","You mush change file name to another name!")
    if name == "Save as...":
        dsc_path = win.saveBox("Select you want to save in......",fileTypes=[('DSC File', '*.dsc')])
        if dsc_path != "":
            if dsc_path != win.getEntry("DSC Path:"):
                print(dsc_path)
                win.setEntry("Output Path:",dsc_path)
            else:
                win.errorBox("Error","You mush change file name to another name!")
    if name == "Import to DSC":
        ass_path = win.getEntry("Lyric Path:")
        dsc_path = win.getEntry("DSC Path:")
        save_path = win.getEntry("Output Path:")

        use_lyric_en = win.getCheckBox("use Lyric_en")
        add_mega_db = win.getCheckBox("auto add empty Lyric db")
        use_kakasi = win.getCheckBox("use kakasi auto add romaji lyric")

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
            win.errorBox("Error","Lyric path error!")
        elif dsc_path == "" or Path(dsc_path).exists() == False:
            win.errorBox("Error","DSC path error!")
        elif save_path == "" or (Path(save_path).parent).exists() == False:
            win.errorBox("Error","Output Path error!")
        else:
            try:
                lyric_list ,lyric_dsc_file_name = main.run(dsc_path,ass_path,save_path,PV_ID,color_lyric)
                win.setLabel("check","Done!")

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
                        if use_kakasi:
                            kakasi_temp = convert_to_romaji(lyric['lyric'])
                            lyric_en_temp += f"pv_{PV_ID}.lyric_en.{lyric['id']}={kakasi_temp}\n"
                        elif add_mega_db:
                            lyric_en_temp += f"pv_{PV_ID}.lyric_en.{lyric['id']}=\n"
                lyric_temp = f"#{lyric_file_name}\n{lyric_temp}{lyric_en_temp}"
                lyric_txt_path = Path("temp/lyric.txt")
                with open(lyric_txt_path, "w", encoding="UTF-8") as f:
                    f.write(lyric_temp)
                os.startfile(lyric_txt_path)
                win.infoBox("Tip","Please copy the lyrics db in the pop-up txt file")
            except:
                r = traceback.format_exc()
                win.errorBox("Error",f"Unknow error!\n\n{r}")
                win.setLabel("check","Error")
            else:
                Path(lyric_txt_path).unlink()
                Path(lyric_dsc_file_name).unlink()
                Path("temp").rmdir()


win = gui("Import to DSC")
win.setSize("400x200")
win.setResizable(False)

win.addLabel("check","Lyric Import Tool",0,0,3)
win.addLabelEntry("Lyric Path:",1,0,2)
win.addLabelEntry("DSC Path:",2,0,2)
win.addLabelEntry("Output Path:",3,0,2)

win.addButton("Lyric File...",open_file,1,2)
win.addButton("DSC File...",open_file,2,2)
win.addButton("Save as...",open_file,3,2)
win.addButton("Import to DSC",open_file,4,2)

win.addLabel("use_PV_ID","PV_ID: ",4,0)
win.addSpinBoxRange("PV_ID", 1, 9999,4,1)
win.setSpinBox("PV_ID", 900, callFunction=True)

win.startLabelFrame("MegaMix+ Option",5,0,3)
win.addCheckBox("use Lyric_en",6,0,3)
win.addCheckBox("auto add empty Lyric db",7,0,3)
win.addCheckBox("use kakasi auto add romaji lyric",8,0,3)
win.stopLabelFrame()

win.go()
