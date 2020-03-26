emmmm
## introduction

这是一个使用ESP8266制作的，采用micropython编写的 系统(?)，其用于配合fdd的“学海水温侦测系统”进行实时的数据显示
网址:<a href="https://github.com/flwfdd/Study-Sea-weather-detection-system">https://github.com/flwfdd/Study-Sea-weather-detection-system</a>

## hardware

1. ESP8266
   采用了Node MCU的开发板（主要好接线+便宜），采用了micropython编写。由于挂在墙上，就不考虑功耗了吧？
   以及，为了满足性能要求，小小的超了个频

2. 1.44‘ TFT(使用ST7735驱动)
   一块超级小的屏幕，用它的原因主要是因为便宜。(处处透露着贫穷的气息)
   但软件实际可以支持所有采用此驱动的屏幕(包括s)

3. 一个10w的LED灯
   发热贼恐怖，需要的原因后面一起讲

4. 放大镜*1
   还记得前面说屏幕小喵？那自己来DIY一个投影仪吧！想多大有多大

## power
目前正在使用墙插（光是看着那个LED灯的功耗就木有更好的办法了好伐）
5v in->稳压->ESP8266->TFT
           ->升压12v ->LED

## software
由于没有找到ESP8266对应的st7735 module,其中的st7735.py由ESP32的模块改来(原地址:<a herf=https://github.com/GuyCarver/MicroPython/blob/master/lib/ST7735.py>here</a>)
但由于mycropython只给ESP8266提供了8k的栈空间,且目前我暂时未找到扩大方法,光是把font加载进去(有5kb)就已经不行了(且bytearray无法声明静态)。所以，为了避免内存错误，请务必并进行改造及预编译了的.mpy文件
另外，随意在main中import可能也会崩(内存真的到了极限了)，所以...请谨慎import
顺便，获取的东西是now.js，示例见fdd的工程

(本来应该有更多功能的(如声音唤醒)，手残焊坏了两颗板子，于是删了...后面可能会加上...)
(其实，理论上来说，只要唤醒+晚上关闭，是能做到用太阳能供电的？)