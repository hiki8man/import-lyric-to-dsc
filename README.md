写来给自己用的ASS导入DSC工具，因为我找不到能导入歌词颜色的工具

只支持导入FT系统的谱面，本来这个程序就只用来写FT自制谱导歌词用的

没有英文版，原因同上

部分资料参考了nasty的Open-PD-Script-Editor:https://github.com/nastys/Open-PD-Script-Editor

如果你不知道怎么写ASS文件，可以使用aegisub制作

------------------------------------------

目前实现的功能：

清空原DSC文件里面所有的歌词重新导入

自动生成歌词部分的pv_db

支持导入颜色标签，但颜色标签必须添加在歌词最开头

------------------------------------------

目前已知的一些问题：

没有简化重复歌词的ID，由于mega39+的歌词id限制在150，按理应当尽可能减少重复歌词占用ID的问题，但是我懒就没写

没有检测只有空格或者没有文字的字幕，目前这种情况依旧会默认占用歌词ID。如果需要添加无歌词部分请自行设置好字幕结束时间，程序会自动根据结束时间后是否还有字幕来添加无歌词部分

