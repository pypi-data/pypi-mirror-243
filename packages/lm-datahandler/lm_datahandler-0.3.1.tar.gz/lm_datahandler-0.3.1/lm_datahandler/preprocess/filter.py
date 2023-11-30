import scipy.signal as signal


def eeg_filter(eeg, sf_eeg, highpass, highpass_order, lowpass, lowpass_order, bandstop, bandstop_order):
    if bandstop is not None:
        bandstop_count = len(bandstop)
        for i in range(bandstop_count):
            w0_b = bandstop[i][0] / (sf_eeg / 2)
            w1_b = bandstop[i][1] / (sf_eeg / 2)
            b_b, a_b = signal.butter(bandstop_order, [w0_b, w1_b], btype='bandstop', analog=False)
            zi_b = signal.lfilter_zi(b_b, a_b)

            eeg, _ = signal.lfilter(b=b_b, a=a_b, x=eeg, zi=zi_b)
    if highpass is not None:
        wn_h = 2 * highpass / sf_eeg
        b_h, a_h = signal.butter(highpass_order, wn_h, 'highpass', analog=False)
        zi_h = signal.lfilter_zi(b_h, a_h)

        eeg, _ = signal.lfilter(b_h, a_h, eeg, zi=zi_h)
    if lowpass is not None:
        wn_l = 2 * lowpass / sf_eeg
        b_l, a_l = signal.butter(lowpass_order, wn_l, 'lowpass', analog=False)
        zi_l = signal.lfilter_zi(b_l, a_l)

        eeg, _ = signal.lfilter(b_l, a_l, eeg, zi=zi_l)

    return eeg
