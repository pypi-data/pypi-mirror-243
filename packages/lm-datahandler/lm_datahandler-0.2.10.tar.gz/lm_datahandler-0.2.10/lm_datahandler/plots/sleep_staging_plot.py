import numpy as np

from lm_datahandler.preprocess.filter import eeg_filter
from lspopt import spectrogram_lspopt
from matplotlib import pyplot as plt, gridspec
from matplotlib.colors import Normalize
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from scipy.io import loadmat, savemat


def plot_spectrogram(fig, ax, eeg, start_time, sf=500, win=15, freq_band=(0.5, 50), cmap="RdBu_r", trim_percentage=5, vmin=None, vmax=None):
    cmap = "Spectral_r"
    assert isinstance(eeg, np.ndarray), "Data must be a 1D NumPy array."
    assert isinstance(sf, (int, float)), "sf must be int or float."
    assert eeg.ndim == 1, "Data must be a 1D (single-channel) NumPy array."
    assert isinstance(win, (int, float)), "win_sec must be int or float."
    assert isinstance(freq_band, tuple) and freq_band.__len__() == 2, "freq_band must be tuple with 2 numbers."
    assert isinstance(freq_band[0], (int, float)), "freq[0] must be int or float."
    assert isinstance(freq_band[1], (int, float)), "freq[1] must be int or float."
    assert freq_band[0] < freq_band[1], "fmin must be strictly inferior to fmax."
    assert freq_band[1] < sf / 2, "fmax must be less than Nyquist (sf / 2)."
    # assert isinstance(vmin, (int, float, type(None))), "vmin must be int, float, or None."
    # assert isinstance(vmax, (int, float, type(None))), "vmax must be int, float, or None."

    nperseg = int(win * sf)
    assert eeg.size > 2 * nperseg, "Data length must be at least 2 * win_sec."
    f, t, Sxx = spectrogram_lspopt(eeg, sf, nperseg=nperseg, noverlap=0)
    Sxx = 10 * np.log10(Sxx)  # Convert uV^2 / Hz --> dB / Hz
    # Select only relevant frequencies (up to 30 Hz)
    good_freqs = np.logical_and(f >= freq_band[0], f <= freq_band[1])
    Sxx = Sxx[good_freqs, :]
    f = f[good_freqs]
    # savemat('E:/dataset/dev_test_data/'+start_time.strftime("%Y%m%d_%H%M%S")+'.mat', {'Sxx':Sxx, 'freq': f})
    Sxx[Sxx < -15] = -15
    t /= 3600  # Convert t to hours

    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)
    vmin_per, vmax_per = np.percentile(Sxx, [0 + trim_percentage, 100 - trim_percentage])
    if vmin is None:
        vmin = vmin_per
    else:
        vmin = max(vmin_per, vmin)
    if vmax is None:
        vmax = vmax_per
    else:
        vmax = min(vmax_per, vmax)

    norm = Normalize(vmin=vmin, vmax=vmax)
    im = ax.pcolormesh(timestamp_num, f, Sxx, norm=norm, cmap=cmap, antialiased=True, shading="auto")
    # ax.set_xlim(0, timestamp_num.max())
    ax.xaxis_date()
    ax.set_ylim([0, 50])
    ax.set_yticks([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel("Frequency [Hz]", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    return fig, ax, im


def plot_avg_diff_acc(fig, ax, acc, start_time, sf=50, win=15):
    assert acc.shape[0] == 3, "ACC should be a 3-D ndarray"
    assert acc.shape[1] % (win * sf) == 0, "The ACC length should be divisible by the epoch length"

    diff_acc = np.abs(acc[:, 1:] - acc[:, 0:-1])
    diff_acc = np.c_[diff_acc, [0, 0, 0]]

    avg_diff_acc = np.sum(np.reshape(np.sum(diff_acc, axis=0), [-1, sf * win]), axis=1) / (sf * win)
    # set max diff acc to 500
    avg_diff_acc[avg_diff_acc > 500] = 500
    data_length = avg_diff_acc.shape[0]

    t = np.arange(data_length) * win / 3600
    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)
    ax.plot(timestamp_num, avg_diff_acc, lw=1.5, color='r')

    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel("Head Movement", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim(timestamp[0], timestamp[-1])

    return fig, ax


def plot_sleep_posture(fig, ax, grade, start_time, sf=50):
    # assert grade.shape[0] == 1, "The grade of head bias should be a 1-D ndarray"
    t = np.arange(grade.shape[0]) / sf / 3600
    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)
    ax.plot(timestamp_num, grade, lw=1.5, color='b')
    ax.set_ylim(-3.5, 3.5)
    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_yticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax.set_yticklabels(['Sleep Face Down', 'Lie on the Left', 'Lie Flat', 'Lie on the Right', 'Sleep Face Down'], )
    ax.set_ylabel("Sleep Postures", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})
    ax.grid(visible=True, axis='y', linewidth=0.5)

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim(timestamp[0], timestamp[-1])


    return fig, ax


def plot_sleep_staging_result(fig, ax, hypno, sleep_variables, start_time, win=15):
    assert len(hypno.shape) == 1, "Hypno should be a 1-D array"

    t = np.arange(hypno.size) * win / 3600
    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)

    n3_sleep = np.ma.masked_not_equal(hypno, 0)
    n2_sleep = np.ma.masked_not_equal(hypno, 1)
    n1_sleep = np.ma.masked_not_equal(hypno, 2)
    rem_sleep = np.ma.masked_not_equal(hypno, 3)
    wake = np.ma.masked_not_equal(hypno, 4)
    abnormal = np.ma.masked_not_equal(hypno, 5)


    ax.plot(timestamp_num, hypno, lw=2, color='k')
    ax.plot(timestamp_num, abnormal, lw=2, color='k')
    ax.plot(timestamp_num, wake, lw=2, color='orange')
    ax.plot(timestamp_num, rem_sleep, lw=2, color='lime')
    ax.plot(timestamp_num, n1_sleep, lw=2, color='yellowgreen')
    ax.plot(timestamp_num, n2_sleep, lw=2, color='deepskyblue')
    ax.plot(timestamp_num, n3_sleep, lw=2, color='royalblue')

    if sleep_variables is not None:
        sl = mdates.date2num(start_time + timedelta(hours=sleep_variables["SOL"]/3600))

        gu = mdates.date2num(start_time + timedelta(hours=t.max() - sleep_variables["GU"]/3600))

        arousal_time = sleep_variables["ART"]
        if sleep_variables["SOL"] > 0:
            ax.axvline(x=sl, color="r", lw=1, linestyle='--')
            ax.text(sl, 4.2, 'SL', fontsize=18, color='r', ha='left', va='bottom')
            ax.axvspan(timestamp_num[0], sl, color='gray', alpha=0.5)

        if sleep_variables["GU"] > 0:
            ax.axvline(x=gu , color="r", lw=1, linestyle='--')
            # ax.text(sl / 3600, 4.2, 'SL', fontsize=16, color='r', ha='left', va='bottom')
            ax.axvspan(gu, timestamp_num[-1], color='gray', alpha=0.5)

        if arousal_time.shape[0] > 0:
            arousal_time = np.asarray(arousal_time)
            b = np.insert(arousal_time, 0, 0)
            diff = b[1:] - b[:-1]
            c = arousal_time[np.where(diff != 1)[0]]
            d = np.append(arousal_time, 0)
            diff = d[1:] - d[:-1]
            e = arousal_time[np.where(diff != 1)[0]]
            boundaries = np.transpose(np.vstack([c, e]))
            for i in range(boundaries.shape[0]):
                # ax.axvline(x=boundaries[i][0]*win/3600, color="r", lw=1, linestyle='--')
                # ax.axvline(x=boundaries[i][1]*win/3600, color="r", lw=1, linestyle='--')
                # ax.text(boundaries[i][1]*win/3600, 4.2, 'Arousal {}'.format(i), fontsize=12, color='r', ha='center', va='bottom')
                ar_start = mdates.date2num(start_time + timedelta(hours=boundaries[i][0] * win / 3600))
                ar_end = mdates.date2num(start_time + timedelta(hours=boundaries[i][1] * win / 3600))
                ax.axvspan(ar_start, ar_end, color='gray', alpha=0.5)
            ax.text(mdates.date2num(start_time + timedelta(hours=t.max() * 0.98)), 4.2,
                    "Arousals: {}s in {} times".format(arousal_time.shape[0] * win, boundaries.shape[0]), fontsize=12,
                    color='r', ha='right', va='bottom')

    ax.set_ylim([-0.1, 5.8])
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_yticklabels(['N3 Sleep', 'N2 Sleep', 'N1 Sleep', 'REM Sleep', 'Wake', 'Abnormal'], )
    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel("Sleep Staging Result", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim([timestamp_num[0], timestamp_num[-1]])
    return fig, ax


def plot_drowsiness_score(fig, ax, drowsiness, start_time, win=15):
    assert np.max(drowsiness) <= 100 and np.min(drowsiness) >= 0, "Drowsiness Score is in the range of [0, 100]"
    # set max diff acc to 500
    data_length = drowsiness.shape[0]

    t = np.arange(data_length) * win / 3600
    timestamp = [start_time + timedelta(hours=hours) for hours in t]
    timestamp_num = mdates.date2num(timestamp)
    ax.plot(timestamp_num, drowsiness, lw=1.5, color='r')

    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14)
    ax.set_ylabel("Sober Score", fontdict={"fontsize": 18})
    ax.set_xlabel("Time [hrs]", fontdict={"fontsize": 18})
    ax.set_ylim([80, 100])

    # extra_ticks = [timestamp_num[0], timestamp_num[-1]]  # 最小值和最大值
    # ax.set_xticks(list(ax.get_xticks()) + extra_ticks)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim(timestamp[0], timestamp[-1])

    return fig, ax


if __name__ == '__main__':
    data = loadmat(r"E:\WeChat Files\WeChat Files\wxid_591u8n4nmbgc22\FileStorage\File\2023-11\DSI_mouse_EEG_data.mat")["eeg"]
    data = data.squeeze()
    nan_index = np.where(np.isnan(data) == True)[0]
    data[nan_index] = 0
    # data = data[1000*500*15:]
    data = eeg_filter(data, 500, 0.5, 3, None, None, [[49, 51]], 3)
    data = data[0:(data.shape[0]//7500)*7500]*100

    subplot_count = 1
    fig_height = subplot_count * 4 + 1
    height_ratio = (np.ones(subplot_count) * 4).tolist()
    plot_spectral = True
    plot_drowsiness = False
    if plot_spectral:
        height_ratio[0] = 5.0
    # fig, ax = plt.subplots(subplot_count, 1, figsize=(16, fig_height), height_ratio=height_ratio)
    fig = plt.figure(figsize=(20, fig_height))
    gs = gridspec.GridSpec(subplot_count, 1, height_ratios=height_ratio)
    # fig.subplots_adjust(hspace=0.5)
    # if subplot_count == 1:
    #     ax = [ax]
    i = 0
    if plot_spectral:
        ax_1 = fig.add_subplot(gs[i, 0])

        time_str = "2023-11-05 23:22:10"
        # 格式化字符串
        format_str = "%Y-%m-%d %H:%M:%S"

        # 解析时间字符串为datetime对象
        dt = datetime.strptime(time_str, format_str)

        plot_spectrogram(fig, ax_1, data, dt, 500, vmin=-20)
        i += 1

    # drowsiness = 100*np.array([0.949566,0.940485,0.918951,0.913689,0.814250,0.910094,0.833887,0.847659,0.781511,0.830760,0.818576,0.756395,0.722096,0.773878,0.884041,0.798175,0.733650,0.782996,0.807354,0.858805,0.827476,0.849979,0.823926,0.886163,0.866865,0.881388,0.879849,0.831100,0.814905,0.843740,0.784604,0.781440,0.844881,0.790061,0.805440,0.838357,0.856742,0.839643,0.794035,0.818129,0.877661,0.850930,0.911427,0.865486,0.884787,0.842065,0.916168,0.892712,0.890143,0.844781,0.860471,0.873163,0.835366,0.925969,0.893791,0.843043,0.869694,0.879857,0.840772,0.831951,0.883983,0.828696,0.860657,0.886464,0.861849,0.891494,0.888817,0.907554,0.818990,0.833591,0.817365,0.741598,0.751067,0.791634,0.840315,0.774830,0.784192,0.840889,0.783542,0.815453,0.790675,0.776993,0.880568,0.911884,0.851987,0.920858,0.882694,0.914478,0.900058,0.931137,0.895521,0.909304,0.895899,0.895754,0.885200,0.884711,0.915419,0.909551,0.827640,0.827023,0.793801,0.772531,0.817430,0.867497,0.814762,0.802533,0.799526,0.819900,0.859031,0.827437,0.838488,0.906698,0.910554,0.934002,0.916932,0.893070,0.934532,0.965096,0.975776,0.978777,0.980407,0.979669,0.976484,0.969249,0.981555,0.984413,0.981943,0.984651,0.985778,0.986373,0.979917,0.981712,0.969412,0.962478,0.973276,0.978841,0.970523,0.971137,0.977631,0.973483,0.977476,0.962800,0.935865,0.953025,0.940564,0.936952,0.942395,0.946851,0.955269,0.949344,0.956376,0.944101,0.944284,0.952212,0.932129,0.935891,0.930913,0.954506,0.946728,0.962031,0.967007,0.969016,0.969641,0.970826,0.959646,0.964473,0.966633,0.974309,0.965972,0.976858,0.974282,0.966040,0.968858,0.978035,0.978961,0.974291,0.960367,0.971076,0.944982,0.964158,0.946310,0.943990,0.952748,0.960686,0.951288,0.949722,0.951284,0.953520,0.946556,0.951279,0.936596,0.960888,0.948576,0.954985,0.953936,0.949304,0.945197,0.960481,0.945212,0.969839,0.969654,0.951396,0.958311,0.888747,0.955284,0.967345,0.936207,0.954038,0.960360,0.964249,0.956268,0.929539,0.936673,0.935071,0.934219,0.927272,0.892582,0.928693,0.940075,0.942642,0.912352,0.892763,0.897999,0.912574,0.914466,0.913720,0.915239,0.905493,0.950192,0.948028,0.907168,0.955756,0.954374,0.956179,0.953670,0.940241,0.940234,0.939878,0.952337,0.951164,0.954246,0.960026,0.952262,0.949641,0.948824,0.961284,0.953758,0.958783,0.961390,0.964883,0.947552,0.969314,0.961456,0.969068,0.961838,0.961727,0.949882,0.956980,0.963613,0.960739,0.950434,0.956131,0.953417,0.944297,0.948141,0.945712,0.955774,0.956401,0.960297,0.974163,0.970485,0.963334,0.950908,0.942150,0.949908,0.952677,0.955930,0.955075,0.971317,0.976246,0.961811,0.965686,0.968902,0.963003,0.971967,0.972942,0.969764,0.968522,0.975477,0.973215,0.975744,0.972296,0.979880,0.977344,0.957356,0.940235,0.959232,0.944530,0.942445,0.953919,0.954933,0.957718,0.967198,0.955882,0.955039,0.953648,0.964494,0.972360,0.968592,0.979687,0.988638,0.988942,0.989513,0.988470,0.990485,0.988100,0.987026,0.988877,0.988658,0.987096,0.985359,0.986929,0.986078,0.986087,0.983454,0.987150,0.986410,0.988383,0.987722,0.986990,0.987337,0.989822,0.988839,0.988302,0.988123,0.989013,0.990423,0.986695,0.986699,0.986248,0.986109,0.985909,0.981929,0.977584,0.960755,0.943776,0.951110,0.951693,0.951664,0.976010,0.977484,0.970790,0.954989,0.952203,0.959631,0.957353,0.959072,0.949586,0.933523,0.955100,0.958386,0.967313,0.958950,0.968661,0.954824,0.936186,0.914084,0.928941,0.940071,0.939349,0.946992,0.961861,0.969292,0.970828,0.980113,0.965516,0.970091,0.961864,0.970072,0.976700,0.977618,0.967613,0.960755,0.968118,0.954108,0.964952,0.958563,0.961729,0.967096,0.954462,0.961416,0.958028,0.942866,0.957042,0.934383,0.945753,0.964527,0.966923,0.960479,0.955375,0.976293,0.967300,0.988950,0.977709,0.972179,0.968728,0.967783,0.972203,0.970656,0.960253])
    # drowsiness = drowsiness[115:]
    # if plot_drowsiness:
    #     ax_2 = fig.add_subplot(gs[i, 0])
    #     plot_drowsiness_score(fig, ax_2, drowsiness, dt)
        i += 1
    plt.tight_layout()

    plt.savefig(r"E:\WeChat Files\WeChat Files\wxid_591u8n4nmbgc22\FileStorage\File\2023-11\DSI_mouse_EEG_data.png", dpi=300, bbox_inches='tight')