import serial
import time

# 设置RS485串口
ser = serial.Serial(
    port='COM3',         # 您的串口号，Linux一般为/dev/ttyUSB0
    baudrate=9600,      # 波特率，通常为9600
    bytesize=8,         # 数据位，通常为8位
    parity='N',         # 校验位，通常为无校验
    stopbits=1,         # 停止位，通常为1位
    timeout=1           # 设置超时
)

#检查串口是否打开
if not ser.isOpen():
    ser.open()

# 发送电机控制指令
def send_motor_command(command):
    ser.write(command)
    time.sleep(0.1)  # 等待执行时间

# 示例：启动电机
start_command = bytes([0x01, 0x03, 0x00, 0x01, 0x00, 0x01])  # 启动电机的命令
send_motor_command(start_command)

# 示例：停止电机
stop_command = bytes([0x01, 0x03, 0x00, 0x02, 0x00, 0x00])  # 停止电机的命令
send_motor_command(stop_command)

# 关闭串口
ser.close()
