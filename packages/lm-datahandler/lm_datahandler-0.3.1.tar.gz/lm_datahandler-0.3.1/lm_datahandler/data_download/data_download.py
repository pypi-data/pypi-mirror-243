import json
import time
from datetime import datetime
import redis
import requests
import os
import numpy as np
from scipy.io import loadmat


def download_lm_data_from_server(params, data_save_path):
    assert data_save_path is not None, "Data save path should not be none."

    download_url = params['url']

    response = requests.post(download_url, data=json.dumps(params), headers={'Content-Type': 'application/json'})

    data_infos = json.loads(response.text)

    if not os.path.exists(data_save_path):
        os.makedirs(data_save_path)

    result_list = []
    for data_info in data_infos:
        data_info["recordStartDate"] = data_info["recordStartDate"][0:8] + "_" + data_info["recordStartDate"][
                                                                                 9:11] + "_" + data_info[
                                                                                                   "recordStartDate"][
                                                                                               12:14] + "_" + data_info[
                                                                                                                  "recordStartDate"][
                                                                                                              15:17]
        data_info["recordEndDate"] = data_info["recordEndDate"][0:8] + "_" + data_info["recordEndDate"][9:11] + "_" + \
                                     data_info["recordEndDate"][12:14] + "_" + data_info["recordEndDate"][15:17]
        dir_name = str(data_info["phone"]) + "_" + data_info["recordStartDate"] + "_" + data_info["recordEndDate"]
        data_path = os.path.join(data_save_path, dir_name)
        if os.path.exists(data_path):
            continue
        os.makedirs(data_path)
        result_list.append(dir_name)
        print("downloading data: " + dir_name)

        oss_path_dict = {
            "eeg.eeg": data_info["eegData"]["ossUrl"] if data_info['eegData'] is not None else '',
            "acc.acc": data_info["accData"]["ossUrl"] if data_info['accData'] is not None else '',
            "emg.emg": data_info["emgData"]["ossUrl"] if data_info['emgData'] is not None else '',
            "sti.sti": data_info["stiData"]["ossUrl"] if data_info['stiData'] is not None else '',
            "n3.log": data_info["n3LogData"]["ossUrl"] if data_info['n3LogData'] is not None else '',
            "sti.log": data_info["stiLogData"]["ossUrl"] if data_info['stiLogData'] is not None else '',
            "ble.ble": data_info["bleData"]["ossUrl"] if data_info['bleData'] is not None else '',
            "light.light": data_info['lightData']["ossUrl"] if data_info['lightData'] is not None else ''
        }
        for k in oss_path_dict:
            v = oss_path_dict[k]
            if v is not None and v != '':
                response = requests.get(v)
                with open(data_path + "/" + k, 'wb') as f:
                    f.write(response.content)
                print("file download finish: " + dir_name + "/" + k)
        with open(data_path + "/sleep_analyse.txt", 'w') as f:
            json.dump(data_info, f)

    return result_list


# def concat_eeg_and_acc_bytes()

def test():
    r = redis.Redis(host='localhost', port=6379, db=0)
    zx = r.get('zx')
    data_path = r"E:\dataset\dev_test_data\4649_X8"
    eeg_file_data = open(os.path.join(data_path, "eeg.eeg"), 'rb')
    acc_file_data = open(os.path.join(data_path, "acc.acc"), 'rb')

    eeg_bytes = eeg_file_data.read()
    acc_bytes = acc_file_data.read()

    eeg_package = list(eeg_bytes)[534:]
    acc_package = list(acc_bytes)[534:]

    epoch = 2000

    id = "4649"
    for i in range(epoch):
        i = i + 1000
        eeg_i = eeg_package[i * 218 * 10 * 15:(i + 1) * 218 * 10 * 15]
        acc_i = acc_package[i * 48 * 10 * 15:(i + 1) * 48 * 10 * 15]
        eeg_i.extend(acc_i)
        data_i = eeg_i
        data_bytes_i = bytes(data_i)

        data_key = 'record:cache:{}'.format(id)
        data_time = int(datetime.now().timestamp() * 1000)
        split = [218 * 10 * 15, 48 * 10 * 15]

        r.delete(data_key)

        r.set(data_key, data_bytes_i, ex=60)

        download_url = 'http://localhost:5000/online_sleep_analysis_by_epoch'
        params = {
            'id': id,
            'split': split,
            'time': data_time,
            'data_key': data_key
        }
        before_time = datetime.now().timestamp()
        post_response = requests.post(download_url, json=json.dumps(params))

        result_url = 'http://localhost:5000/get_online_sleep_staging_res_by_id'
        params = {
            'id': id
        }
        get_response = requests.get(result_url, params=params)
        end_time = datetime.now().timestamp()
        print("Time cost: {}, epoch {}: {}, sleep staging result: {}".format(end_time - before_time, i,
                                                                             post_response.text, get_response.text))
        time.sleep(5)


if __name__ == '__main__':
    test()
