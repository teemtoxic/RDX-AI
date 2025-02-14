import psutil
import platform
from datetime import datetime, timedelta
import subprocess
import os
import GPUtil  # For GPU information (needs installation)

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        power_plugged = battery.power_plugged
        status = "plugged in" if power_plugged else "not plugged in"
        return f"Battery is at {percent}% and is {status}"
    return "No battery detected"

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu': cpu_usage,
        'memory': memory.percent,
        'disk': disk.percent
    }

def get_system_uptime():
    """Get system uptime in a human-readable format"""
    uptime_seconds = psutil.boot_time()
    boot_time = datetime.fromtimestamp(uptime_seconds)
    now = datetime.now()
    uptime = now - boot_time
    
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    
    uptime_str = []
    if days > 0:
        uptime_str.append(f"{days} days")
    if hours > 0:
        uptime_str.append(f"{hours} hours")
    if minutes > 0:
        uptime_str.append(f"{minutes} minutes")
        
    return f"PC has been running for {', '.join(uptime_str)}"

def get_cpu_details():
    """Get detailed CPU information"""
    cpu_freq = psutil.cpu_freq()
    cpu_count = psutil.cpu_count()
    cpu_percent_per_core = psutil.cpu_percent(percpu=True)
    
    return {
        'physical_cores': psutil.cpu_count(logical=False),
        'total_cores': cpu_count,
        'current_frequency': f"{cpu_freq.current:.2f}MHz",
        'max_frequency': f"{cpu_freq.max:.2f}MHz",
        'per_core_usage': cpu_percent_per_core
    }

def get_memory_details():
    """Get detailed memory information"""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        'total': f"{memory.total / (1024**3):.2f}GB",
        'available': f"{memory.available / (1024**3):.2f}GB",
        'used': f"{memory.used / (1024**3):.2f}GB",
        'swap_total': f"{swap.total / (1024**3):.2f}GB",
        'swap_used': f"{swap.used / (1024**3):.2f}GB"
    }

def get_disk_details():
    """Get detailed disk information for all partitions"""
    disks = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks[partition.device] = {
                'total': f"{usage.total / (1024**3):.2f}GB",
                'used': f"{usage.used / (1024**3)::.2f}GB",
                'free': f"{usage.free / (1024**3):.2f}GB",
                'filesystem': partition.fstype
            }
        except:
            continue
    return disks

def get_gpu_info():
    """Get GPU information if available"""
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                'name': gpu.name,
                'load': f"{gpu.load*100}%",
                'memory_used': f"{gpu.memoryUsed}MB",
                'memory_total': f"{gpu.memoryTotal}MB",
                'temperature': f"{gpu.temperature}°C"
            })
        return gpu_info
    except:
        return None

def get_network_info():
    """Get network usage information"""
    network = psutil.net_io_counters()
    return {
        'bytes_sent': f"{network.bytes_sent / (1024**2):.2f}MB",
        'bytes_received': f"{network.bytes_recv / (1024**2):.2f}MB",
        'packets_sent': network.packets_sent,
        'packets_received': network.packets_recv
    }

def check_system_resources():
    info = get_system_info()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"""System Status Report - {current_time}
==================================
System Uptime: {get_system_uptime()}
==================================
CPU Information:
{'-' * 20}
{format_dict(get_cpu_details())}

Memory Information:
{'-' * 20}
{format_dict(get_memory_details())}

Disk Information:
{'-' * 20}
{format_dict(get_disk_details())}

Network Information:
{'-' * 20}
{format_dict(get_network_info())}
"""

    gpu_info = get_gpu_info()
    if gpu_info:
        message += f"""
GPU Information:
{'-' * 20}
{format_dict(gpu_info)}
"""

    message += f"""
==================================
Battery: {get_battery_info()}
Internet: {monitor_internet()}
"""
    
    # Create Reports directory if it doesn't exist
    if not os.path.exists("Reports"):
        os.makedirs("Reports")
    
    # Save to file with timestamp
    filename = f"Reports/system_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(message)
    
    # Open the file in notepad
    subprocess.Popen(['notepad.exe', filename])
    
    return message

def monitor_internet():
    try:
        import requests
        response = requests.get("http://www.google.com", timeout=5)
        return "Internet connection is active"
    except:
        return "No internet connection"

def format_dict(d, indent=0):
    """Helper function to format dictionary output"""
    if isinstance(d, list):
        return '\n'.join(format_dict(item, indent) for item in d)
    
    if not isinstance(d, dict):
        return f"{'  ' * indent}{d}"
    
    result = []
    for key, value in d.items():
        if isinstance(value, dict):
            result.append(f"{'  ' * indent}{key}:")
            result.append(format_dict(value, indent + 1))
        elif isinstance(value, list):
            result.append(f"{'  ' * indent}{key}:")
            for item in value:
                result.append(format_dict(item, indent + 1))
        else:
            result.append(f"{'  ' * indent}{key}: {value}")
    return '\n'.join(result)

