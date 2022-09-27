#coding:utf-8
from appJar import gui
import main
import os
win = gui("导入ass字幕")
win.setSize("400x100")
win.setResizable(False)
win.setFont(12)
win.addLabel("check","初始化完成",0,0,2)
win.addLabelEntry("ass文件路径：")
win.addLabelEntry("dsc文件路径：")
win.addLabelEntry("导出文件路径: ")
def open_file(name):
    print(name, "press")
    if name == "ass文件...":
        ass_path = win.openBox("选择要导入的ass文件......",fileTypes=[('ass文件', '*.ass')])
        if ass_path != "":
            print(ass_path)
            win.setEntry("ass文件路径：",ass_path)
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
    elif name == "导入ass字幕":
        ass_path = win.getEntry("ass文件路径：")
        dsc_path = win.getEntry("dsc文件路径：")
        save_path = win.getEntry("导出文件路径: ")
        try:
            lyric_file_name ,ass_dsc_file_name = main.run(dsc_path,ass_path,save_path)
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
win.addButton("ass文件...",open_file,1,1)
win.addButton("dsc文件...",open_file,2,1)
win.addButton("保存到.....",open_file,3,1)
win.addButton("导入ass字幕",open_file,4,0,2)
win.go()