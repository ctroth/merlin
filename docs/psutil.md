# 📊 Psutil Python Module Guide

**Last Updated:** 25 April 2025  
**Supported Python Versions:** 2.6, 2.7, 3.4+

---

## 📌 Overview

`psutil` is a cross-platform Python library used to access system details and process utilities. It is ideal for monitoring resources such as CPU, memory, disks, network, and sensors. The library supports system monitoring, profiling, limiting process resources, and managing running processes.

---

## ⚙️ Installation (Linux: Ubuntu/Debian)

```bash
sudo pip install psutil
```

---

## 🧠 CPU Monitoring

### 1. `psutil.cpu_times()`

Returns system CPU times as a named tuple.

```python
import psutil
print(psutil.cpu_times())
```

---

### 2. `psutil.cpu_percent(interval)`

Returns the CPU utilization as a percentage over a given interval.

```python
import psutil
print(psutil.cpu_percent(1))
```

---

### 3. `psutil.cpu_count(logical=True)`

Returns the number of logical or physical CPU cores.

```python
import psutil
print("Logical cores:", psutil.cpu_count())
print("Physical cores:", psutil.cpu_count(logical=False))
```

---

### 4. `psutil.cpu_stats()`

Returns statistics like context switches and interrupts.

```python
import psutil
print(psutil.cpu_stats())
```

---

### 5. `psutil.cpu_freq()`

Returns current, min, and max CPU frequencies in MHz.

```python
import psutil
print(psutil.cpu_freq())
```

---

### 6. `psutil.getloadavg()`

Returns average system load over 1, 5, and 15 minutes.

```python
import psutil
print(psutil.getloadavg())
```

---

## 💾 Memory Monitoring

### 1. `psutil.virtual_memory()`

Returns virtual memory usage statistics.

```python
import psutil
print(psutil.virtual_memory())
```

---

### 2. `psutil.swap_memory()`

Returns swap memory statistics.

```python
import psutil
print(psutil.swap_memory())
```

---

## 💽 Disk Monitoring

### 1. `psutil.disk_partitions()`

Returns all mounted disk partitions.

```python
import psutil
print(psutil.disk_partitions())
```

---

### 2. `psutil.disk_usage(path)`

Returns disk usage for the specified path.

```python
import psutil
print(psutil.disk_usage('/'))
```

---

## 🌐 Network Monitoring

### 1. `psutil.net_io_counters()`

Returns network I/O statistics.

```python
import psutil
print(psutil.net_io_counters())
```

---

### 2. `psutil.net_connections()`

Returns current socket connections.

```python
import psutil
print(psutil.net_connections())
```

---

### 3. `psutil.net_if_addrs()`

Returns addresses for each network interface.

```python
import psutil
print(psutil.net_if_addrs())
```

---

## 🌡️ Sensor Monitoring

### 1. `psutil.sensors_temperatures()`

Returns temperatures from system sensors.

```python
import psutil
print(psutil.sensors_temperatures())
```

---

### 2. `psutil.sensors_fans()`

Returns fan speed details.

```python
import psutil
print(psutil.sensors_fans())
```

---

### 3. `psutil.sensors_battery()`

Returns battery charge and status information.

```python
import psutil
print(psutil.sensors_battery())
```

---

## 🖥️ Other System Info

### 1. `psutil.boot_time()`

Returns system boot time (in epoch seconds).

```python
import psutil
print(psutil.boot_time())
```

---

### 2. `psutil.users()`

Returns users currently logged into the system.

```python
import psutil
print(psutil.users())
```

---
