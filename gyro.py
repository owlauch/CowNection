#!/usr/bin/python
import smbus
import math
import time
import datetime
import httplib, urllib

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
 
bus = smbus.SMBus(1) 
address = 0x68       
 
bus.write_byte_data(address, power_mgmt_1, 0) 


def Giroscopio():	
    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)
   
    f = ( str(gyroskop_xout)+";"+str(gyroskop_xout)+";"
     +str(gyroskop_yout)+";"+str(gyroskop_yout / 131)+";"
     +str(gyroskop_zout)+";"+str(gyroskop_zout / 131)+";"
        ) 

    return f; 

def Acelerometro(): 
    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)
    beschleunigung_xout_skaliert = read_word_2c(0x3b) / 16384.0
    beschleunigung_yout_skaliert = read_word_2c(0x3d) / 16384.0
    beschleunigung_zout_skaliert = read_word_2c(0x3f) / 16384.0
    # print "Acelerometro_x: ", ("%6d" % beschleunigung_xout), " escala: ", beschleunigung_xout_skaliert
    # print "Acelerometro_y: ", ("%6d" % beschleunigung_yout), " escala: ", beschleunigung_yout_skaliert
    # print "Acelerometro_z: ", ("%6d" % beschleunigung_zout), " escala: ", beschleunigung_zout_skaliert
    f = (
         str (beschleunigung_xout)+ ";"+str(beschleunigung_xout_skaliert)+";"
        +str (beschleunigung_yout)+ ";"+str(beschleunigung_yout_skaliert)+";"
        +str (beschleunigung_zout)+ ";"+str(beschleunigung_zout_skaliert)+";"
        + ";"+str(beschleunigung_zout_skaliert)+";"
    )
    return f;

def Busola():
    beschleunigung_xout_skaliert = read_word_2c(0x3b) / 16384.0
    beschleunigung_yout_skaliert = read_word_2c(0x3d) / 16384.0
    beschleunigung_zout_skaliert = read_word_2c(0x3f) / 16384.0

    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)
    
    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)
    # print "X NORTE: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
    # print "Y SUL: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)

    f = (
         str(get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))+";"
        +str(get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))+"\n"
    )
    return f;


def main():
    text = "Data;Giro_x;esc_x;Giro_y;esc_y;Giro_z;esc_z;Acel_x;esc_x;Acel_y;esc_y;Acel_z;esc_z;Bus_x;Bus_y\n";
    for x in range(600):
        time.sleep(1.0);
        # ts = time.time()
        # text += str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))+";"
        # text += Acelerometro();
        # text += Giroscopio();
        # text += Busola();
        # f = open('parametros.txt','w')
        # f.write(text)
        # f.close()

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = "Giroscopio="+Acelerometro()

        conn = httplib.HTTPConnection("192.168.1.19:3000")
        conn.request("POST", "", payload, headers)
        response = conn.getresponse()

    return;
    
main();
