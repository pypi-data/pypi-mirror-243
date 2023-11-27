import psutil
import platform
from datetime import datetime
import screen_brightness_control as sbc
import pyautogui

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def sys_info():
    uname = platform.uname()
    data = {
        "System" : uname.system,
        "Node Name" : uname.node,
        "Release" : uname.release,
        "Version" : uname.version,
        "Machine" : uname.machine,
        "Processor" : uname.processor  
    }
    return data

def boot_time():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    return {"Boot Time" : f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"}

def cpu_info():
    cpufreq = psutil.cpu_freq()
    core = []
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        core.append(f"Core {i}: {percentage}%")
    data ={
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{cpufreq.max:.2f}Mhz",
        "Min Frequency": f"{cpufreq.min:.2f}Mhz",
        "Current Frequency": f"{cpufreq.current:.2f}Mhz",
        "Cores": core,
        "Total CPU Usage" : f"{psutil.cpu_percent()}%"
    }
    return data

def memmory_info():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    virtual = {
        "Total": get_size(svmem.total),
        "Available": get_size(svmem.available),
        "Used": get_size(svmem.used),
        "Percentage": svmem.percent
    }
    swap = {
        "Total": get_size(swap.total),
        "Free": get_size(swap.free),
        "Used": get_size(swap.used),
        "Percentage": swap.percent
    }
    data = {
        "virtual": virtual,
        "swap": swap
    }

def disk_info():
    partitions = psutil.disk_partitions()
    disk_io = psutil.disk_io_counters()
    part = []
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        p = {
            "Device": partition.device,
            "Mountpoint": partition.mountpoint,
            "File system type": partition.fstype,
            "Total Size": get_size(partition_usage.total),
            "Used": get_size(partition_usage.used),
            "Free": get_size(partition_usage.free),
            "Percentage": partition_usage.percent,
        }
        part.append(p)
    data = {
        "partitions": part,
        "Total read": get_size(disk_io.read_bytes),
        "Total write": get_size(disk_io.write_bytes)
    }
    return data

def network_info():
    if_addrs = psutil.net_if_addrs()
    net_io = psutil.net_io_counters()
    addres = []
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                a = {
                    "IP Address": address.address,
                    "Netmask": address.netmask,
                    "Broadcast IP": address.broadcast
                }
                addres.append(a)
                
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                a = {
                    "MAC Address": address.address,
                    "Netmask": address.netmask,
                    "Broadcast MAC": address.broadcast
                }
                addres.append(a)

    data = {
        "Address":addres,
        "Total Bytes Sent": get_size(net_io.bytes_sent),
        "Total Bytes Received": get_size(net_io.bytes_recv)
    }
    return data

def brightness_ctl(bright):
    monitors = sbc.list_monitors()
    sbc.set_brightness(bright, display=monitors[0])

def volume_ctl(x):
    ab = 100
    pyautogui.press('volumedown',ab)
    az = x/2
    pyautogui.press('volumeup',int(az))