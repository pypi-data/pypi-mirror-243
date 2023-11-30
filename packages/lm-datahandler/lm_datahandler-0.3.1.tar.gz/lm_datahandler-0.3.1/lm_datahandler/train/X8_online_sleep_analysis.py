import time

import lightgbm as lgb
import numpy as np
import redis
from lm_datahandler.datahandler import DataHandler
from scipy import signal
from scipy.io import loadmat

r = redis.Redis(host='localhost', port=6379, db=0)

wn_h = 2 * 0.5 / 500
b_h, a_h = signal.butter(3, wn_h, 'highpass', analog=False)
zi_h_0 = signal.lfilter_zi(b_h, a_h)

w0_b = 49 / (500 / 2)
w1_b = 51 / (500 / 2)
b_b, a_b = signal.butter(3, [w0_b, w1_b], btype='bandstop', analog=False)
zi_b_0 = signal.lfilter_zi(b_b, a_b)

clf = lgb.Booster(
    model_file=r'E:\githome\lm_datahandler\lm_datahandler\train\realtime_sleepstaging_15s_eeg_acc_120iter_20231120_214814.txt')
data_handler = DataHandler()

'''
输入：
    eeg: 单通道eeg，要求长度为7500
    acc：3通道acc，要求总长度为750，排列方式为c1,c2,c3,c1,c2,c3
    id：记录的唯一标识
输出（该接口不直接返回结果，只返回执行情况）：
    1：成功执行
    -1：输入数据长度不对
'''


def online_sleep_analysis_by_epoch(eeg, acc, id):
    # eeg = (eeg - 32767) / 65536 * 2.5 * 1000 * 1000 / 100
    # acc = acc - 32767
    eeg = np.array(eeg).squeeze()
    acc = np.array(acc).squeeze()
    if not (eeg.shape[0] == 7500 and acc.shape[0] == 750 * 3):
        return -1
    acc = acc.reshape([750, 3]).transpose()

    # sso: sleep staging online
    key_zi_b = "x8_sso_{}_zi_b".format(id)
    key_zi_h = "x8_sso_{}_zi_h".format(id)
    key_cached_feature = "x8_sso_{}_cached_feature".format(id)
    key_id = "x8_sso_{}".format(id)

    if not r.exists(key_id):
        zi_b = zi_b_0
        zi_h = zi_h_0
        cached_feature = None
    else:
        zi_b = r.lrange(key_zi_b, 0, -1)
        zi_h = r.lrange(key_zi_h, 0, -1)
        cached_feature = r.lrange(key_cached_feature, 0, -1)

    zi_b = zi_b_0 if zi_b is None else [float(x) for x in zi_b]
    zi_h = zi_h_0 if zi_h is None else [float(x) for x in zi_h]
    cached_feature = None if cached_feature is None else [float(x) for x in cached_feature]
    if cached_feature is not None:
        cached_epoch = len(cached_feature) // 60
        for i in range(cached_epoch):
            print(cached_feature[i * 60: (i + 1) * 60])

    eeg, zi_b = signal.lfilter(b_b, a_b, eeg, zi=zi_b)
    eeg, zi_h = signal.lfilter(b_h, a_h, eeg, zi=zi_h)

    sleep_stage_res, wear_detect_res, cached_feature = data_handler.predict_with_single_epoch(eeg, acc, clf,
                                                                                              cached_feature)

    # 存相关数据
    r.delete(key_cached_feature)
    r.delete(key_zi_b)
    r.delete(key_zi_h)
    r.delete(key_id)
    cached_feature_arr = cached_feature.values.reshape(-1)
    for item in cached_feature_arr:
        r.rpush(key_cached_feature, item)
    for item in zi_b:
        r.rpush(key_zi_b, item)
    for item in zi_h:
        r.rpush(key_zi_h, item)
    r.set(key_id, id)

    key_ss_result = "x8_sso_{}_result".format(id)
    r.set(key_ss_result, sleep_stage_res)

    # 定义Lua脚本，批量设置过期时间：30s
    lua_script = """
        local id = ARGV[1]

        local key_cached_feature = 'x8_sso_' .. id .. '_cached_feature'
        local key_zi_b = 'x8_sso_' .. id .. '_zi_b'
        local key_zi_h = 'x8_sso_' .. id .. '_zi_h'
        local key_id = 'x8_sso_' .. id
        local key_ss_result = 'x8_sso_' .. id .. '_result'
        
        -- 设置超时时间统一为30s
        redis.call('EXPIRE', key_cached_feature, 30)
        redis.call('EXPIRE', key_zi_b, 30)
        redis.call('EXPIRE', key_zi_h, 30)
        redis.call('EXPIRE', key_id, 30)
        redis.call('EXPIRE', key_ss_result, 30)
        """

    # 执行Lua脚本
    r.eval(lua_script, 0, id)

    # zi_b = r.get(key_zi_b)
    # zi_h = r.get(key_zi_h)
    # cached_feature = r.lrange(key_cached_feature, 0, -1)


if __name__ == '__main__':
    data = loadmat(r"E:\dataset\X7-PSG\JZ_data\label_and_prediction\final_data\20230520_WZY\eeg_and_acc.mat")
    eeg = data["eeg"].squeeze()
    acc = (data["acc"] - 32767)

    epoch = eeg.shape[0] // 7500
    eeg = eeg.squeeze()[0: epoch * 7500]
    acc = acc.squeeze()[:, 0: epoch * 750]
    acc = acc.transpose().reshape([-1])
    # acc = acc.reshape([-1])
    id = "2023520_wzy"
    for i in range(epoch):
        eeg_i = eeg[i * 7500:(i + 1) * 7500]
        acc_i = acc[i * 750 * 3:(i + 1) * 750 * 3]
        online_sleep_analysis_by_epoch(eeg_i, acc_i, id)
        time.sleep(5)
        print("epoch: {}, sleep staging result: {}".format(i, r.get("x8_sso_{}_result".format(id))))
        print("------------------------------------------------------------------------")
        # time.sleep(10)
