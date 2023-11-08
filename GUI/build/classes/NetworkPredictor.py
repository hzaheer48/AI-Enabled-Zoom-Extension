import time
import psutil
import numpy as np
from tensorflow import keras
from keras.models import load_model
import joblib

class NetworkPredictor:
    def __init__(self):
        self.loaded_model = load_model("./trained_model.h5")
        self.loaded_scaler = joblib.load("./scaler.pkl")
        self.prev_sent, self.prev_recv = self.get_network_usage()

    def get_network_usage(self):
        network_stats = psutil.net_io_counters()
        return network_stats.bytes_sent, network_stats.bytes_recv

    def calculate_bps(self, prev_sent, prev_recv, current_sent, current_recv, time_interval):
        sent_bps = (current_sent - prev_sent) * 8 / time_interval
        recv_bps = (current_recv - prev_recv) * 8 / time_interval
        
        sent_mbps = sent_bps / 1000000  
        recv_mbps = recv_bps / 1000000  

        return sent_mbps, recv_mbps


    def predict_network_traffic(self):
        interval = 1 
        x_new = []
        while len(x_new)<3:
            time.sleep(interval)
            current_sent, current_recv = self.get_network_usage()
            sent_bps, recv_bps = self.calculate_bps(self.prev_sent, self.prev_recv, current_sent, current_recv, interval)
            self.prev_sent, self.prev_recv = current_sent, current_recv
            total_bps = sent_bps + recv_bps
            scaled_total_bps = self.loaded_scaler.transform(np.array([total_bps]).reshape(-1, 1))
            x_new.append(scaled_total_bps[0][0])
        x_new = [x_new]
        x_new = np.array(x_new)
        x_new = np.reshape(x_new, (x_new.shape[0], x_new.shape[1], 1))
        prediction = self.loaded_model.predict(x_new)
        denormalized_prediction = self.loaded_scaler.inverse_transform(prediction)
        return round(float(denormalized_prediction[0][0]),2)

