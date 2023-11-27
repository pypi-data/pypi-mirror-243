import os

import numpy as np
from matplotlib import pyplot as plt
from scipy.io import loadmat
from scipy.stats import pearsonr
import seaborn as sns

def plot_rsp_corr_contrast(path):
    bp = loadmat(os.path.join(path, 'bp.mat'))
    psg = bp['bp_psg']
    x7 = bp['bp_x7']

    bp_psg_delta = psg[0]
    bp_psg_theta = psg[1]
    bp_psg_alpha = psg[2]
    bp_psg_sigma = psg[3]

    bp_x7_delta = x7[0]
    bp_x7_theta = x7[1]
    bp_x7_alpha = x7[2]
    bp_x7_sigma = x7[3]

    corr_delta, p_delta = pearsonr(bp_x7_delta, bp_psg_delta)
    corr_theta, p_theta = pearsonr(bp_psg_theta, bp_x7_theta)
    corr_alpha, p_alpha = pearsonr(bp_psg_alpha, bp_x7_alpha)
    corr_sigma, p_sigma = pearsonr(bp_psg_sigma, bp_x7_sigma)
    print("corr: delta: {}, theta: {}, alpha: {}, sigma: {}".format(corr_delta, corr_theta, corr_alpha, corr_sigma))
    print("p_val: delta: {}, theta: {}, alpha: {}, sigma: {}".format(p_delta, p_theta, p_alpha, p_sigma))

    fig, ax = plt.subplots(4, 1, figsize=(16, 16))
    plt.subplots_adjust(hspace=0.5)
    t = np.arange(psg.shape[1]) / (3600 / 15)
    ax[0].plot(t, bp_psg_delta, color='k')
    ax[0].plot(t, bp_x7_delta, color='r')
    sns.despine()
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)
    ax[0].spines['bottom'].set_visible(False)
    ax[0].spines['left'].set_visible(False)
    ax[0].set_ylim([0.35, 1])
    ax[0].set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    ax[0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax[0].grid(visible=True, axis='y', linewidth=0.3)
    ax[0].set_title('Delta Corr = {:.2f}'.format(corr_delta), loc='right')

    ax[1].plot(t, bp_psg_theta, color='k')
    ax[1].plot(t, bp_x7_theta, color='r')
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].spines['bottom'].set_visible(False)
    ax[1].spines['left'].set_visible(False)
    ax[1].set_ylim([-0.02, 0.3])
    ax[1].set_yticks([0, 0.1, 0.2, 0.3])
    ax[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax[1].grid(visible=True, axis='y', linewidth=0.3)
    ax[1].set_title('Theta Corr = {:.2f}'.format(corr_theta), loc='right')

    ax[2].plot(t, bp_psg_alpha, color='k')
    ax[2].plot(t, bp_x7_alpha, color='r')
    ax[2].spines['top'].set_visible(False)
    ax[2].spines['right'].set_visible(False)
    ax[2].spines['bottom'].set_visible(False)
    ax[2].spines['left'].set_visible(False)
    ax[2].set_ylim([-0.02, 0.2])
    ax[2].set_yticks([0, 0.1, 0.2])
    ax[2].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax[2].grid(visible=True, axis='y', linewidth=0.3)
    ax[2].set_title('Alpha Corr = {:.2f}'.format(corr_alpha), loc='right')

    ax[3].plot(t, bp_psg_sigma, color='k')
    ax[3].plot(t, bp_x7_sigma, color='r')
    ax[3].spines['top'].set_visible(False)
    ax[3].spines['right'].set_visible(False)
    ax[3].spines['bottom'].set_visible(False)
    ax[3].spines['left'].set_visible(False)
    ax[3].set_ylim([-0.02, 0.2])
    ax[3].set_yticks([0, 0.1, 0.2])
    ax[3].grid(visible=True, axis='y', linewidth=0.3)
    ax[3].set_title('Sigma Corr = {:.2f}'.format(corr_sigma), loc='right')

    plt.savefig('rsp_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    plot_rsp_corr_contrast(r'E:\dataset\X7-PSG\JZ_data\label_and_prediction\final_data\20230520_WZY')