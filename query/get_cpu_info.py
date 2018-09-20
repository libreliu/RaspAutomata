import os

def get_cpu_info():
    with open("/proc/cpuinfo") as f:
        data = f.read()
    
    cpus = data.count("processor\t:")
    model_name = (data[data.find("model name\t: ")+13:].split("\n"))[0]
    ret['cpus'] = cpus
    ret['model_name'] = model_name
    ret['data'] = data
    return ret
