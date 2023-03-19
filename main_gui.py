#coding:utf-8
from appJar import gui
import main
import os

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
            win.setLabel("check","导入成功")
            os.startfile(lyric_file_name)
            print(lyric_file_name)
            win.infoBox("提示","请手动复制弹出的txt文件里面的歌词db")
        except Exception as r:
            print(r)
            win.setLabel("check","导入失败")
        os.remove(ass_dsc_file_name)
        os.remove(lyric_file_name)
        os.removedirs("temp")

win = gui("导入歌词字幕")
win.setSize("400x100")
win.setResizable(False)
win.setFont(12)

win.addLabel("check","初始化完成",0,0,3)
win.addLabelEntry("歌词文件路径：",1,0,2)
win.addLabelEntry("dsc文件路径：",2,0,2)
win.addLabelEntry("导出文件路径: ",3,0,2)

win.addButton("歌词文件...",open_file,1,2)
win.addButton("dsc文件...",open_file,2,2)
win.addButton("保存到.....",open_file,3,2)
win.addButton("导入歌词字幕",open_file,4,2)

win.addLabel("use_PV_ID","PV_ID: ",4,0)
win.addSpinBoxRange("PV_ID", 1, 9999,4,1)
win.setSpinBox("PV_ID", 900, callFunction=True)

win.go()