import os

import numpy as np
from matplotlib import pyplot as plt

from lm_datahandler.datahandler import DataHandler
from scipy.io import loadmat

path = r"E:\dataset\X7-PSG\JZ_data\label_and_prediction\final_data"
datas = os.listdir(path)
x7_tst = []
psg_origin_tst = []
psg_fixed_tst = []
x7_se = []
psg_origin_se = []
psg_fixed_se = []
x7_sol = []
psg_origin_sol = []
psg_fixed_sol = []
x7_waso = []
psg_origin_waso = []
psg_fixed_waso = []
data_names = []
for data in datas:
    x7_hypno = loadmat(os.path.join(os.path.join(path, data), "prediction.mat"))['prediction'].squeeze()
    psg_origin_hypno = loadmat(os.path.join(os.path.join(path, data), "psg_trans_label.mat"))['psg_trans_label'].squeeze()
    psg_fixed_hypno = loadmat(os.path.join(os.path.join(path, data), "hypno.mat"))['psg_trans_label'].squeeze()

    if data == '20230520_WZY':
        x7_hypno = x7_hypno[0:-1]
    if data == '20230729_YCM207':
        psg_fixed_hypno = psg_fixed_hypno[0:2393]
        psg_origin_hypno = psg_origin_hypno[0:2393]
    if data == '20230812_YCM231':
        x7_hypno = x7_hypno[0:-1]
    if data == '20230825_YCM254':
        x7_hypno = x7_hypno[0:1333]
    if data == '20230902_YCM131':
        psg_fixed_hypno = psg_fixed_hypno[0:2294]
        psg_origin_hypno = psg_origin_hypno[0:2294]
    if data == '20230908_WM':
        psg_fixed_hypno = psg_fixed_hypno[0:2689]
        psg_origin_hypno = psg_origin_hypno[0:2689]
    if data == '20230908_YCM180':
        psg_fixed_hypno = psg_fixed_hypno[0:2379]
        psg_origin_hypno = psg_origin_hypno[0:2379]

    if data in ['20230715_YCM180', '20230922_YCM191', '20230526_LTY', '20230908_YCM180', '20230630_CW']:
        continue

    if x7_hypno.shape[0] == psg_origin_hypno.shape[0] == psg_fixed_hypno.shape[0]:
        print("---------------- Compute Sleep Variables: {} ------------------".format(data))
        data_handler = DataHandler()
        data_handler.compute_sleep_variables(x7_hypno)
        x7_sleep_variables = data_handler.sleep_variables
        data_handler.compute_sleep_variables(psg_origin_hypno)
        psg_origin_sleep_variables = data_handler.sleep_variables
        data_handler.compute_sleep_variables(psg_fixed_hypno)
        psg_fixed_sleep_variables = data_handler.sleep_variables

        x7_tst.append(x7_sleep_variables['TST']/60)
        psg_origin_tst.append(psg_origin_sleep_variables['TST']/60)
        psg_fixed_tst.append(psg_fixed_sleep_variables['TST']/60)
        x7_se.append(x7_sleep_variables['SE']*100)
        psg_origin_se.append(psg_origin_sleep_variables['SE']*100)
        psg_fixed_se.append(psg_fixed_sleep_variables['SE']*100)
        x7_sol.append(x7_sleep_variables['SOL']/60)
        psg_origin_sol.append(psg_origin_sleep_variables['SOL']/60)
        psg_fixed_sol.append(psg_fixed_sleep_variables['SOL']/60)
        x7_waso.append(x7_sleep_variables['WASO']/60)
        psg_origin_waso.append(psg_origin_sleep_variables['WASO']/60)
        psg_fixed_waso.append(psg_fixed_sleep_variables['WASO']/60)

        data_names.append(data)
    else:
        print("---------------- Hypno length not consistent: {} ----------------".format(data))

x7_tst = np.array(x7_tst)
psg_origin_tst = np.array(psg_origin_tst)
psg_fixed_tst = np.array(psg_fixed_tst)
x7_se = np.array(x7_se)
psg_origin_se = np.array(psg_origin_se)
psg_fixed_se = np.array(psg_fixed_se)
x7_sol = np.array(x7_sol)
psg_origin_sol = np.array(psg_origin_sol)
psg_fixed_sol = np.array(psg_fixed_sol)
x7_waso = np.array(x7_waso)
psg_origin_waso = np.array(psg_origin_waso)
psg_fixed_waso = np.array(psg_fixed_waso)
data_names = np.array(data_names)

fig, ax = plt.subplots(2, 2, figsize=(10, 8))

psg_tst = psg_fixed_tst
diff_tst = psg_tst - x7_tst
mean_tst = np.mean(diff_tst)
sd_tst = np.std(diff_tst, axis=0)

ax[0][0].scatter(psg_tst, diff_tst, color='black', s=20)
# for i in range(len(data_names)):
#     ax[0][0].annotate("{}".format(data_names[i]), (psg_tst[i], diff_tst[i]), textcoords="offset points", xytext=(0, 10), ha='center')
ax[0][0].axhline(mean_tst, color='red', linestyle='-')
ax[0][0].axhline(mean_tst + 1.96 * sd_tst, color='red', linestyle='--')
ax[0][0].axhline(mean_tst - 1.96 * sd_tst, color='red', linestyle='--')
ax[0][0].axhline(0, color='black', linestyle='-')
ax[0][0].set_xlabel('PSG ' + 'TST(min)')
ax[0][0].set_ylabel('Diff of ' + 'TST between PSG and LM')
# ax[0][0].set_ylim([-20, 20])
# ax[0][0].set_xticks([0, 1, 2, 3, 4])
ax[0][0].spines['right'].set_visible(False)
ax[0][0].spines['top'].set_visible(False)
ax[0][0].spines['bottom'].set_visible(False)

# ----------------------sol------------------------------
psg_sol = psg_fixed_sol
diff_sol = psg_sol - x7_sol
mean_sol = np.mean(diff_sol)
sd_sol = np.std(diff_sol, axis=0)

ax[0][1].scatter(psg_sol, diff_sol, color='black', s=20)
# for i in range(len(data_names)):
#     ax[0][1].annotate("{}".format(data_names[i]), (psg_sol[i], diff_sol[i]), textcoords="offset points", xytext=(0, 10), ha='center')
ax[0][1].axhline(mean_sol, color='red', linestyle='-')
ax[0][1].axhline(mean_sol + 1.96 * sd_sol, color='red', linestyle='--')
ax[0][1].axhline(mean_sol - 1.96 * sd_sol, color='red', linestyle='--')
ax[0][1].axhline(0, color='black', linestyle='-')
ax[0][1].set_xlabel('PSG ' + 'SOL(min)')
ax[0][1].set_ylabel('Diff of ' + 'SOL between PSG and LM')
# ax[0][1].set_ylim([-8, 8])
# ax[0][1].set_xticks([0, 1, 2, 3, 4])
ax[0][1].spines['right'].set_visible(False)
ax[0][1].spines['top'].set_visible(False)
ax[0][1].spines['bottom'].set_visible(False)

# ----------------------waso------------------------------
psg_waso = psg_fixed_waso
diff_waso = psg_waso - x7_waso
mean_waso = np.mean(diff_waso)
sd_waso = np.std(diff_waso, axis=0)

ax[1][0].scatter(psg_waso, diff_waso, color='black', s=20)
# for i in range(len(data_names)):
#     ax[1][0].annotate("{}".format(data_names[i]), (psg_waso[i], diff_waso[i]), textcoords="offset points", xytext=(0, 10), ha='center')
ax[1][0].axhline(mean_waso, color='red', linestyle='-')
ax[1][0].axhline(mean_waso + 1.96 * sd_waso, color='red', linestyle='--')
ax[1][0].axhline(mean_waso - 1.96 * sd_waso, color='red', linestyle='--')
ax[1][0].axhline(0, color='black', linestyle='-')
ax[1][0].set_xlabel('PSG ' + 'WASO(min)')
ax[1][0].set_ylabel('Diff of ' + 'WASO between PSG and LM')
# ax[1][0].set_ylim([-8, 8])
# ax[1][0].set_xticks([0, 1, 2, 3, 4])
ax[1][0].spines['right'].set_visible(False)
ax[1][0].spines['top'].set_visible(False)
ax[1][0].spines['bottom'].set_visible(False)

# ----------------------se------------------------------
psg_se = psg_fixed_se
diff_se = psg_se - x7_se
mean_se = np.mean(diff_se)
sd_se = np.std(diff_se, axis=0)

ax[1][1].scatter(psg_se, diff_se, color='black', s=20)
# for i in range(len(data_names)):
#     ax[1][1].annotate("{}".format(data_names[i]), (psg_se[i], diff_se[i]), textcoords="offset points", xytext=(0, 10), ha='center')
ax[1][1].axhline(mean_se, color='red', linestyle='-')
ax[1][1].axhline(mean_se + 1.96 * sd_se, color='red', linestyle='--')
ax[1][1].axhline(mean_se - 1.96 * sd_se, color='red', linestyle='--')
ax[1][1].axhline(0, color='black', linestyle='-')
ax[1][1].set_xlabel('PSG ' + 'SE(%)')
ax[1][1].set_ylabel('Diff of ' + 'SE between PSG and LM')
# ax[1][1].set_ylim([-8, 8])
# ax[1][1].set_xticks([0, 1, 2, 3, 4])
ax[1][1].spines['right'].set_visible(False)
ax[1][1].spines['top'].set_visible(False)
ax[1][1].spines['bottom'].set_visible(False)

plt.savefig(r'E:\dataset\X7-PSG\JZ_data\label_and_prediction\ba.png', dpi=300, bbox_inches='tight')
plt.show()
