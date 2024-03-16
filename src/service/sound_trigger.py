from src.hardware.sound_sensor import soundSensor


N_BUFFER = 20
cir_queue = [0] * N_BUFFER
cir_queue_index = 0
cir_sum = 0

def soundTrigger():
    avg = getSoundAvg()
    if(avg > 0.1):
        return True
    else:
        return False

def getSoundAvg():
    return cir_sum / N_BUFFER



def _add_to_cir_queue(value):
    global cir_queue_index
    global cir_sum
    cir_sum -= cir_queue[cir_queue_index]
    cir_queue[cir_queue_index] = value
    cir_sum += value
    cir_queue_index = (cir_queue_index + 1) % N_BUFFER

def reload_sound_loop():
    _add_to_cir_queue(1 if soundSensor() < 0.5 else 0)

def reset_queue():
    global cir_queue
    global cir_queue_index
    global cir_sum
    cir_queue = [0] * N_BUFFER
    cir_queue_index = 0
    cir_sum = 0
    for i in range(N_BUFFER):
        _add_to_cir_queue(0)