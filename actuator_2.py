from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

# 配置Modbus客户端
client = ModbusClient(
    method='rtu',  # 使用RTU模式
    port='com7',  # 串口地址，Windows系统可以是 COM3, COM4 等
    baudrate=115200,  # 波特率，与驱动器设置一致
    stopbits=1,
    bytesize=8,
    parity='N',
    timeout=1
)

def connect_to_driver():
    """尝试连接驱动器"""
    if client.connect():
        print("连接成功！")
    else:
        print("连接失败，请检查连接设置。")
        exit()

def set_motor_current(slave_id, current):
    try:
        address = 0x0191
        client.write_register(address, current, unit=slave_id)
        print(f"成功设置从站 {slave_id} 的电流为 {current}。")
    except Exception as e: 
        print(f"设置电流失败: {e}")

def set_speed_model():
    try:
        address = 0x6200
        client.write_register(address, 0x0002, unit=1)
        print("成功设置速度模式。")
    except Exception as e:
        print(f"设置速度模式失败: {e}")

def motor_direction(slave_id, direction):
    try:
        address = 0x0007
        client.write_register(address, direction, unit=slave_id)
        print(f"成功设置从站 {slave_id} 的方向为 {direction}。")
    except Exception as e:
        print(f"设置方向失败: {e}")


def set_motor_speed(slave_id, speed):
    """
    设置步进电机的速度
    :param slave_id: Modbus从站地址
    :param speed: 转速，具体数值范围需参考驱动器手册
    """
    try:
        # 假设速度寄存器地址为 0x0100（需查阅驱动器文档）
        address = 0x6203
        client.write_register(address, speed, unit=slave_id)
        print(f"成功设置从站 {slave_id} 的速度为 {speed}。")
    except Exception as e:
        print(f"设置速度失败: {e}")

def start_motor(slave_id):
    """
    启动步进电机
    :param slave_id: Modbus从站地址
    """
    try:
        # 假设启动寄存器地址为 0x0200，速度模式启动值为 0x0010（需查阅驱动器文档）
        address = 0x6002
        client.write_register(address, 0x0010, unit=slave_id)
        print(f"成功启动从站 {slave_id} 的电机。")
    except Exception as e:
        print(f"启动电机失败: {e}")

def stop_motor(slave_id):
    """
    停止步进电机
    :param slave_id: Modbus从站地址
    """
    try:
        # 停止寄存器地址为 0x0200，停止值为 0（需查阅驱动器文档）
        address = 0x6002
        client.write_register(address, 0x0040, unit=slave_id)
        print(f"成功停止从站 {slave_id} 的电机。")
    except Exception as e:
        print(f"停止电机失败: {e}")

def main():
    connect_to_driver()

    slave_id = 1  # Modbus从站地址，需根据设备实际设置
    try:
        # 示例：设置速度、启动、运行一段时间后停止
        set_speed_model()
        motor_direction(slave_id, 1)  # 设置方向，0为上升，1为下降
        #set_motor_current(slave_id, 15)
        set_motor_speed(slave_id, 200)  # 设置速度为500（单位需参考驱动器文档）
        start_motor(slave_id)
        time.sleep(2)  # 电机运行5秒
        stop_motor(slave_id)
    finally:
        client.close()  # 关闭连接
        print("关闭Modbus连接。")

if __name__ == "__main__":
    main()
