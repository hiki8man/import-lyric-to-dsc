#coding:utf-8
from appJar import gui
import main
import os

def open_file(name):
    print(name, "press")
    if name == "Lyric File...":
        ass_path = win.openBox("Select you want to import lyric file......",fileTypes=[('ASS,LRC,PPD Lyric File', ['*.ass','*.lrc','kasi.txt'])])
        if ass_path != "":
            print(ass_path)
            win.setEntry("Lyric Path:",ass_path)
    elif name == "DSC File...":
        dsc_path = win.openBox("Select you want to import dsc file......",fileTypes=[('DSC File', '*.dsc')])
        if dsc_path != "":
            if dsc_path != win.getEntry("Output Path:"):
                print(dsc_path)
                win.setEntry("DSC Path:",dsc_path)
            else:
                win.errorBox("Error","You mush change file name to another name!")
    elif name == "Save as...":
        dsc_path = win.saveBox("Select you want to save in......",fileTypes=[('DSC File', '*.dsc')])
        if dsc_path != "":
            if dsc_path != win.getEntry("DSC Path:"):
                print(dsc_path)
                win.setEntry("Output Path:",dsc_path)
            else:
                win.errorBox("Error","You mush change file name to another name!")
    elif name == "Import to DSC":
        ass_path = win.getEntry("Lyric Path:")
        dsc_path = win.getEntry("DSC Path:")
        save_path = win.getEntry("Output Path:")
        PV_ID = win.getSpinBox("PV_ID")
        if len(PV_ID) < 3:
            PV_ID = "{:0>3}".format(str(PV_ID))
        if ass_path[-3:] == "ass":
            color_lyric = 1
        elif ass_path[-3:] == "lrc":
            color_lyric = 0
        elif ass_path[-8:] == "kasi.txt":
            color_lyric = -1
        try:
            lyric_file_name ,ass_dsc_file_name = main.run(dsc_path,ass_path,save_path,PV_ID,color_lyric)
            win.setLabel("check","Done!")
            os.startfile(lyric_file_name)
            print(lyric_file_name)
            win.infoBox("Tip","Please copy the lyrics db in the pop-up txt file")
        except Exception as r:
            print(r)
            win.setLabel("check","Error")
        os.remove(ass_dsc_file_name)
        os.remove(lyric_file_name)
        os.removedirs("temp")

win = gui("Import to DSC")
win.setSize("400x100")
win.setResizable(False)
win.setFont(12)

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

win.go()