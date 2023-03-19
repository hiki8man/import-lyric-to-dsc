import os,sys
import dsc
import chart.option
import pathlib

dsc_file = input("Drop your DSC file in here then press enter\n")
dsc_file_path = pathlib.Path(dsc_file)
dsc_data_list = dsc.read(dsc_file_path)
fix_dsc_data_list = chart.option.change_hold_note_show(dsc_data_list)
fix_dsc_file_path = pathlib.Path.joinpath(dsc_file_path.parent ,dsc_file_path.stem + "_fix.dsc")
fix_dsc_file_path = pathlib.Path(fix_dsc_file_path)
dsc.write(fix_dsc_data_list, fix_dsc_file_path)
print("Done!")
os.system("pause")