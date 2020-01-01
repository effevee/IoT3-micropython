import os
import gc

def fs_space():
  """ toont de gealloceerde en vrije ruimte in MB van het VFS in flash memory van de ESP32 """
  fs_stat = os.statvfs('/flash')
  fs_alloc = fs_stat[0] * fs_stat[2] / (1024*1024)
  fs_free = fs_stat[0] * fs_stat[3] / (1024*1024)
  return fs_alloc,fs_free

def mem_space():
  """ toont het gealloceerde en vrije RAM geheugen in KB van de ESP32 """
  gc.collect()
  mem_alloc = gc.mem_alloc() / 1024
  mem_free = gc.mem_free() / 1024
  return mem_alloc,mem_free


#print("Filesystem Allocated %.2f MB - Free %.2f MB"%(fs_space()[0],fs_space()[1]))
#print("Memory Allocated %.2f KB - Free %.2f KB"%(mem_space()[0],mem_space()[1]))


