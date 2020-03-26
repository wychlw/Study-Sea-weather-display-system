import time
import ntptime
import urequests as requests
from ST7735 import TFT
from machine import SPI,Pin
from math import floor
from micropython import const

class main():

    x_min=15
    x_max=120
    y_top=50
    y_bottom=120
    temp=[]
    pres=[]
    water=[]
    humi=[]
    date=[]
    ntp_url='ntp4.aliyun.com'
    dat_url='put your own address here'
    last_time_update=None
    
    def __init__(self,wlan,SSID,PASSWD):
        #init wlan
        self.wlan=wlan
        self.SSID=SSID
        self.PASSWD=PASSWD

        #init time
        print('ntp_url:',self.ntp_url)
        ntptime.host=self.ntp_url
        print('ntp_host:',ntptime.host)
        ntptime.time()
        ntptime.settime()
        self.last_time_update=time.time()
        print('init_time:',time.localtime(self.last_time_update+3600*8))

        #init data
        print('dat_url:',self.dat_url)

        #init display mod
        '''
        mode:
            0:cycle
            1:temp only
            2:pres only
            3:water only
            4:humi only
        '''
        self.mode=0
        '''
        last:
            0:temp
            1:pres
            2:water
            3:humi
        '''
        self.last=0
        
        #init tft
        print('init TFT...')
        spi = SPI(1, baudrate=32000000, polarity=0, phase=0)
        self.tft=TFT(spi,2,16,0)
        self.tft.init_7735(self.tft.GREENTAB128x128)
        self.tft.fill(TFT.WHITE)
        self.tft.text((5,10),"initlizing",TFT.YELLOW,2,nowrap=True)
        self.tft.text((5,50),"please wait",TFT.YELLOW,2,nowrap=True)

        self.run()


    def run(self):
        while True:
            self.display_time()
            self.get_dat()
            self.display_data()
            time.sleep(5)

    def get_time(self):
        time_now=time.time()
        if time_now-self.last_time_update>=3600:
            ntptime.time()
            ntptime.settime()
            time_now=time.time()
            self.last_time_update=time_now
        return time.localtime(time_now+3600*8)

    def display_time(self):
        time_now=self.get_time()
        print("p time",time_now)
        self.tft.fill(TFT.BLACK)
        self.tft.text((5,5),str(time_now[0])+' '+str(time_now[1])+' '+str(time_now[2]),TFT.GRAY,1.8,nowrap=True)
        self.tft.text((35,20),str(time_now[3])+':'+str(time_now[4])+':'+str(time_now[5]),TFT.GRAY,1.8,nowrap=True)

    def get_dat(self):
        req=requests.get(self.dat_url)
        data=req.json()
        if len(self.date)>0 and self.date[len(self.date)-1]==data['date']:
            return
        if len(self.temp)>=10:
            self.temp.pop(0)
            self.water.pop(0)
            self.humi.pop(0)
            self.pres.pop(0)
            self.date.pop(0)
        self.temp.append(data['tmp2'])
        self.water.append(data['tmp0'])
        self.humi.append(data['humi'])
        self.pres.append(data['pres'])
        self.date.append(data['date'])
        return

    def display_data(self):

        def draw_axis(self):

            self.tft.line((self.x_min,self.y_top),(self.x_min,self.y_bottom),TFT.WHITE)
            self.tft.line((self.x_min,self.y_bottom),(self.x_max,self.y_bottom),TFT.WHITE)
            self.tft.line((self.x_min,self.y_top),(self.x_min-5,self.y_top+5),TFT.WHITE)
            self.tft.line((self.x_min,self.y_top),(self.x_min+5,self.y_top+5),TFT.WHITE)
            self.tft.line((self.x_max,self.y_bottom),(self.x_max-5,self.y_bottom+5),TFT.WHITE)
            self.tft.line((self.x_max,self.y_bottom),(self.x_max-5,self.y_bottom-5),TFT.WHITE)
            self.tft.text((self.x_min,self.y_top-10),"y",TFT.WHITE,1,nowrap=True)
            self.tft.text((self.x_max,self.y_bottom-10),"x",TFT.WHITE,1,nowrap=True)
            for i in range(self.x_min,self.x_max,floor((self.x_max-self.x_min)/10)):
                self.tft.line((i,self.y_bottom-2),(i,self.y_bottom+3),TFT.WHITE)

        def draw_points(self,data):
            self.y_top=self.y_top+10
            x_dis=floor((self.x_max-self.x_min)/10)
            x_now=self.x_min
            dat_min=100000
            dat_max=-100000
            for i in data:
                if i<dat_min:
                    dat_min=i
                if i>dat_max:
                    dat_max=i

            if dat_min>dat_max:
                return

            points=[]
            which=0
            if dat_min==dat_max:
                for i in data:
                    points.append((floor(x_now),floor(self.y_bottom+(self.y_top-self.y_bottom)/2)))
                    self.tft.circle(points[which],2,TFT.YELLOW)
                    self.tft.text((points[which][0]-5,points[which][1]+5),str(i),TFT.CYAN,0.5,nowrap=True)
                    self.tft.text((points[which][0]-5,points[which][1]-10),self.date[which][11:16],TFT.CYAN,0.6,nowrap=True)
                    if which>0:
                        self.tft.line(points[which-1],points[which],TFT.YELLOW)
                    which=which+1
                    x_now=x_now+x_dis
            else:
                for i in data:
                    points.append((floor(x_now),floor(self.y_bottom+(self.y_top-self.y_bottom)*((i-dat_min)/(dat_max-dat_min)))))
                    self.tft.circle(points[which],2,TFT.YELLOW)
                    self.tft.text((points[which][0]-5,points[which][1]+5),str(i),TFT.CYAN,0.5,nowrap=True)
                    self.tft.text((points[which][0]-5,points[which][1]-10),self.date[which][11:16],TFT.CYAN,0.6,nowrap=True)
                    if which>0:
                        self.tft.line(points[which-1],points[which],TFT.YELLOW)
                    which=which+1
                    x_now=x_now+x_dis

            self.y_top=self.y_top-10

        draw_axis(self)

        if self.mode==0:
            
            if self.last==0:
                self.last=1
                self.tft.text((50,45),"pres",TFT.YELLOW,1,nowrap=True)
                draw_points(self,self.pres)

            elif self.last==1:
                self.last=2
                self.tft.text((50,45),"water",TFT.YELLOW,1,nowrap=True)
                draw_points(self,self.water)

            elif self.last==2:
                self.last=3
                self.tft.text((50,45),"humi",TFT.YELLOW,1,nowrap=True)
                draw_points(self,self.humi)

            elif self.last==3:
                self.last=0
                self.tft.text((50,45),"temp",TFT.YELLOW,1,nowrap=True)
                draw_points(self,self.temp)

        elif self.mode==1:
            self.last=0
            self.tft.text((50,45),"temp",TFT.YELLOW,1,nowrap=True)
            draw_points(self,self.temp)

        elif self.mode==2:
            self.last=1
            self.tft.text((50,45),"pres",TFT.YELLOW,1,nowrap=True)
            draw_points(self,self.pres)

        elif self.mode==3:
            self.last=2
            self.tft.text((50,45),"water",TFT.YELLOW,1,nowrap=True)
            draw_points(self,self.water)

        elif self.mode==4:
            self.last=3
            self.tft.text((50,45),"humi",TFT.YELLOW,1,nowrap=True)
            draw_points(self,self.humi)