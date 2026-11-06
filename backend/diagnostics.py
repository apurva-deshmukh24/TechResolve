
import psutil
import requests
import socket

from datetime import datetime


# 1. Check Internet Connection
def check_internet():

    try:

        response = requests.get(
            "https://www.google.com",
            timeout=5
        )

        response.raise_for_status()

        return {
            "status": "Healthy",
            "message": "Internet connection is working."
        }

    except requests.RequestException:

        return {
            "status": "Critical",
            "message": "Internet connection is unavailable."
        }


# 2. Check System Performance
def check_performance():

    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory().percent

    if cpu >= 90 or ram >= 90:

        status = "Critical"

    elif cpu >= 75 or ram >= 75:

        status = "Warning"

    else:

        status = "Healthy"

    return {
        "status": status,
        "cpu": cpu,
        "ram": ram,
        "message": "System performance checked."
    }


# 3. Check Disk Storage
def check_storage():

    disk = psutil.disk_usage("C:\\")

    free_space = round(
        disk.free / (1024 ** 3),
        2
    )

    if disk.percent >= 95:

        status = "Critical"

    elif disk.percent >= 85:

        status = "Warning"

    else:

        status = "Healthy"

    return {
        "status": status,
        "used": disk.percent,
        "free_gb": free_space,
        "message": "Storage checked."
    }


# 4. Check DNS Resolution
def check_dns():

    try:

        socket.gethostbyname("google.com")

        return {
            "status": "Healthy",
            "message": "DNS resolution is working."
        }

    except socket.gaierror:

        return {
            "status": "Critical",
            "message": "DNS resolution failed."
        }


# 5. Generate Complete Diagnostic Report
def run_diagnostics():

    return {

        "internet": check_internet(),

        "performance": check_performance(),

        "storage": check_storage(),

        "dns": check_dns(),

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }
