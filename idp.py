import smbus,time
import csv
#import pandas as pd

bus=smbus.SMBus(1)
MPU6050_ADDR = 0x68

ACCEL_XOUT_H=0x3B
ACCEL_YOUT_H=0x3D
ACCEL_CONFIG=0x1C
GYRO_CONFIG= 0x1B
ACCEL_ZOUT_H=0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

    
def MPU6050_start():
    accel_config_sel = [0b00000,0b01000,0b10000,0b11000] # byte registers
    accel_config_vals = [2.0,4.0,8.0,16.0] # g (g = 9.81 m/s^2)
    accel_indx = 0
    
    gyro_config_sel = [0b00000,0b010000,0b10000,0b11000] # byte registers
    gyro_config_vals = [250.0,500.0,1000.0,2000.0] # degrees/sec
    gyro_indx = 0
    bus.write_byte_data(MPU6050_ADDR, GYRO_CONFIG, int(gyro_config_sel[gyro_indx]))
    
    bus.write_byte_data(MPU6050_ADDR, 0x6B, 0)
    bus.write_byte_data(MPU6050_ADDR, ACCEL_CONFIG, int(accel_config_sel[accel_indx]))
    return gyro_config_vals[gyro_indx],accel_config_vals[accel_indx]

def read_raw_bits(register):
    # read accel and gyro values
    high = bus.read_byte_data(MPU6050_ADDR, register)
    low = bus.read_byte_data(MPU6050_ADDR, register+1)

    # combine higha and low for unsigned bit value
    value = ((high << 8) | low)
    
    # convert to +- value
    if(value > 32768):
        value -= 65536
    return value

gyro_sens,accel_sens = MPU6050_start()


#data = []

for index in range(10000):
    
    res_x_h=read_raw_bits(ACCEL_XOUT_H)
    res_y_h=read_raw_bits(ACCEL_YOUT_H)
    res_z_h=read_raw_bits(ACCEL_ZOUT_H)
    
    gyro_x = read_raw_bits(GYRO_XOUT_H)
    gyro_y = read_raw_bits(GYRO_YOUT_H)
    gyro_z = read_raw_bits(GYRO_ZOUT_H)
    
    a_x = (res_x_h/(2.0**15.0))*accel_sens
    a_y = (res_y_h/(2.0**15.0))*accel_sens
    a_z = (res_z_h/(2.0**15.0))*accel_sens
    
    w_x = (gyro_x/(2.0**15.0))*gyro_sens
    w_y = (gyro_y/(2.0**15.0))*gyro_sens
    w_z = (gyro_z/(2.0**15.0))*gyro_sens
    
    row =[a_x,a_y,a_z,w_x,w_y,w_z]
    #data.append(row)
    if(index == 0):
        with open('outp1.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(row)
    else:
        with open('outp1.csv', 'a') as f:
            write = csv.writer(f)
            write.writerow(row)
            f.close()
    #if (index%1000 == 0):
        
    print(row)
    
   
    time.sleep(0.5)
#df = pd.DataFrame(data, columns=["x", "y","z"])

#print(len(data))
#df.to_csv("out.csv")
    
 
