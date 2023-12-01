"""sonusai calc_metric_spenh

usage: calc_metric_spenh [-hvtpws] [-i MIXID] [-e WER] [-m WMNAME] PLOC TLOC

options:
    -h, --help
    -v, --verbose               Be verbose.
    -i MIXID, --mixid MIXID     Mixture ID(s) to process, can be range like 0:maxmix+1 [default: *].
    -t, --truth-est-mode        Calculate extraction and metrics using truth (instead of prediction).
    -p, --plot                  Enable PDF plots file generation per mixture.
    -w, --wav                   Generate WAV files per mixture.
    -s, --summary               Enable summary files generation.
    -e WER, --wer-method WER    Word-Error-Rate method: deepgram, google, aixplain_whisper
                                or whisper (locally run) [default: none]
    -m WMNAME, --whisper-model  Whisper model name used in aixplain_whisper and whisper WER methods.
                                [default: tiny]

Calculate speech enhancement metrics of prediction data in PLOC using SonusAI mixture data
in TLOC as truth/label reference. Metric and extraction data files are written into PLOC.

PLOC  directory containing prediction data in .h5 files created from truth/label mixture data in TLOC
TLOC  directory with SonusAI mixture database of truth/label mixture data

For whisper WER methods, the possible models used in local processing (WER = whisper) are:
    {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}
but note most are very computationally demanding and can overwhelm/hang a local system.

Outputs the following to PLOC (where id is mixd number 0:num_mixtures):
    <id>_metric_spenh.txt

    If --plot:
        <id>_metric_spenh.pdf

    If --wav:
        <id>_target.wav
        <id>_target_est.wav
        <id>_noise.wav
        <id>_noise_est.wav
        <id>_mixture.wav

        If --truth-est-mode:
            <id>_target_truth_est.wav
            <id>_noise_truth_est.wav

    If --summary:
        metric_spenh_targetf_summary.txt
        metric_spenh_targetf_summary.csv
        metric_spenh_targetf_list.csv
        metric_spenh_targetf_estats_list.csv

        If --truth-est-mode:
            metric_spenh_targetf_truth_list.csv
            metric_spenh_targetf_estats_truth_list.csv

TBD
Metric and extraction data are written into prediction location PLOC as separate files per mixture.

    -d PLOC, --ploc PLOC        Location of SonusAI predict data.

Inputs:

"""
from dataclasses import dataclass
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sonusai import logger
from sonusai.mixture import AudioF
from sonusai.mixture import AudioT
from sonusai.mixture import Feature
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict

matplotlib.use('SVG')


@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    predict_location: str = None
    predwav_mode: bool = None
    truth_est_mode: bool = None
    enable_plot: bool = None
    enable_wav: bool = None
    wer_method: str = None
    whisper_model: str = None


MP_GLOBAL = MPGlobal()


def power_compress(spec):
    mag = np.abs(spec)
    phase = np.angle(spec)
    mag = mag ** 0.3
    real_compress = mag * np.cos(phase)
    imag_compress = mag * np.sin(phase)
    return real_compress + 1j * imag_compress


def power_uncompress(spec):
    mag = np.abs(spec)
    phase = np.angle(spec)
    mag = mag ** (1. / 0.3)
    real_uncompress = mag * np.cos(phase)
    imag_uncompress = mag * np.sin(phase)
    return real_uncompress + 1j * imag_uncompress


def snr(clean_speech, processed_speech, sample_rate):
    # Check the length of the clean and processed speech. Must be the same.
    clean_length = len(clean_speech)
    processed_length = len(processed_speech)
    if clean_length != processed_length:
        raise ValueError('Both Speech Files must be same length.')

    overall_snr = 10 * np.log10(np.sum(np.square(clean_speech)) / np.sum(np.square(clean_speech - processed_speech)))

    # Global Variables
    winlength = round(30 * sample_rate / 1000)  # window length in samples
    skiprate = int(np.floor(winlength / 4))  # window skip in samples
    MIN_SNR = -10  # minimum SNR in dB
    MAX_SNR = 35  # maximum SNR in dB

    # For each frame of input speech, calculate the Segmental SNR
    num_frames = int(clean_length / skiprate - (winlength / skiprate))  # number of frames
    start = 0  # starting sample
    window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(1, winlength + 1) / (winlength + 1)))

    segmental_snr = np.empty(num_frames)
    EPS = np.spacing(1)
    for frame_count in range(num_frames):
        # (1) Get the Frames for the test and reference speech. Multiply by Hanning Window.
        clean_frame = clean_speech[start:start + winlength]
        processed_frame = processed_speech[start:start + winlength]
        clean_frame = np.multiply(clean_frame, window)
        processed_frame = np.multiply(processed_frame, window)

        # (2) Compute the Segmental SNR
        signal_energy = np.sum(np.square(clean_frame))
        noise_energy = np.sum(np.square(clean_frame - processed_frame))
        segmental_snr[frame_count] = 10 * np.log10(signal_energy / (noise_energy + EPS) + EPS)
        segmental_snr[frame_count] = max(segmental_snr[frame_count], MIN_SNR)
        segmental_snr[frame_count] = min(segmental_snr[frame_count], MAX_SNR)

        start = start + skiprate

    return overall_snr, segmental_snr


def lpcoeff(speech_frame, model_order):
    # (1) Compute Autocorrelation Lags
    winlength = np.size(speech_frame)
    R = np.empty(model_order + 1)
    E = np.empty(model_order + 1)
    for k in range(model_order + 1):
        R[k] = np.dot(speech_frame[0:winlength - k], speech_frame[k: winlength])

    # (2) Levinson-Durbin
    a = np.ones(model_order)
    a_past = np.empty(model_order)
    rcoeff = np.empty(model_order)
    E[0] = R[0]
    for i in range(model_order):
        a_past[0: i] = a[0: i]
        sum_term = np.dot(a_past[0: i], R[i:0:-1])
        rcoeff[i] = (R[i + 1] - sum_term) / E[i]
        a[i] = rcoeff[i]
        if i == 0:
            a[0: i] = a_past[0: i] - np.multiply(a_past[i - 1:-1:-1], rcoeff[i])
        else:
            a[0: i] = a_past[0: i] - np.multiply(a_past[i - 1::-1], rcoeff[i])
        E[i + 1] = (1 - rcoeff[i] * rcoeff[i]) * E[i]
    acorr = R
    refcoeff = rcoeff
    lpparams = np.concatenate((np.array([1]), -a))
    return acorr, refcoeff, lpparams


def llr(clean_speech, processed_speech, sample_rate):
    from scipy.linalg import toeplitz

    # Check the length of the clean and processed speech.  Must be the same.
    clean_length = np.size(clean_speech)
    processed_length = np.size(processed_speech)
    if clean_length != processed_length:
        raise ValueError('Both Speech Files must be same length.')

    # Global Variables
    winlength = (np.round(30 * sample_rate / 1000)).astype(int)  # window length in samples
    skiprate = (np.floor(winlength / 4)).astype(int)  # window skip in samples
    if sample_rate < 10000:
        P = 10  # LPC Analysis Order
    else:
        P = 16  # this could vary depending on sampling frequency.

    # For each frame of input speech, calculate the Log Likelihood Ratio
    num_frames = int((clean_length - winlength) / skiprate)  # number of frames
    start = 0  # starting sample
    window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(1, winlength + 1) / (winlength + 1)))

    distortion = np.empty(num_frames)
    for frame_count in range(num_frames):
        # (1) Get the Frames for the test and reference speech. Multiply by Hanning Window.
        clean_frame = clean_speech[start: start + winlength]
        processed_frame = processed_speech[start: start + winlength]
        clean_frame = np.multiply(clean_frame, window)
        processed_frame = np.multiply(processed_frame, window)

        # (2) Get the autocorrelation lags and LPC parameters used to compute the LLR measure.
        R_clean, Ref_clean, A_clean = lpcoeff(clean_frame, P)
        R_processed, Ref_processed, A_processed = lpcoeff(processed_frame, P)

        # (3) Compute the LLR measure
        numerator = np.dot(np.matmul(A_processed, toeplitz(R_clean)), A_processed)
        denominator = np.dot(np.matmul(A_clean, toeplitz(R_clean)), A_clean)
        distortion[frame_count] = np.log(numerator / denominator)
        start = start + skiprate
    return distortion


def wss(clean_speech, processed_speech, sample_rate):
    from scipy.fftpack import fft

    # Check the length of the clean and processed speech, which must be the same.
    clean_length = np.size(clean_speech)
    processed_length = np.size(processed_speech)
    if clean_length != processed_length:
        raise ValueError('Files must have same length.')

    # Global variables
    winlength = (np.round(30 * sample_rate / 1000)).astype(int)  # window length in samples
    skiprate = (np.floor(np.divide(winlength, 4))).astype(int)  # window skip in samples
    max_freq = (np.divide(sample_rate, 2)).astype(int)  # maximum bandwidth
    num_crit = 25  # number of critical bands

    USE_FFT_SPECTRUM = 1  # defaults to 10th order LP spectrum
    n_fft = (np.power(2, np.ceil(np.log2(2 * winlength)))).astype(int)
    n_fftby2 = (np.multiply(0.5, n_fft)).astype(int)  # FFT size/2
    Kmax = 20.0  # value suggested by Klatt, pg 1280
    Klocmax = 1.0  # value suggested by Klatt, pg 1280

    # Critical Band Filter Definitions (Center Frequency and Bandwidths in Hz)
    cent_freq = np.array([50.0000, 120.000, 190.000, 260.000, 330.000, 400.000, 470.000,
                          540.000, 617.372, 703.378, 798.717, 904.128, 1020.38, 1148.30,
                          1288.72, 1442.54, 1610.70, 1794.16, 1993.93, 2211.08, 2446.71,
                          2701.97, 2978.04, 3276.17, 3597.63])
    bandwidth = np.array([70.0000, 70.0000, 70.0000, 70.0000, 70.0000, 70.0000, 70.0000,
                          77.3724, 86.0056, 95.3398, 105.411, 116.256, 127.914, 140.423,
                          153.823, 168.154, 183.457, 199.776, 217.153, 235.631, 255.255,
                          276.072, 298.126, 321.465, 346.136])

    bw_min = bandwidth[0]  # minimum critical bandwidth

    # Set up the critical band filters.
    # Note here that Gaussianly shaped filters are used.
    # Also, the sum of the filter weights are equivalent for each critical band filter.
    # Filter less than -30 dB and set to zero.
    min_factor = np.exp(-30.0 / (2.0 * 2.303))  # -30 dB point of filter
    crit_filter = np.empty((num_crit, n_fftby2))
    for i in range(num_crit):
        f0 = (cent_freq[i] / max_freq) * n_fftby2
        bw = (bandwidth[i] / max_freq) * n_fftby2
        norm_factor = np.log(bw_min) - np.log(bandwidth[i])
        j = np.arange(n_fftby2)
        crit_filter[i, :] = np.exp(-11 * np.square(np.divide(j - np.floor(f0), bw)) + norm_factor)
        cond = np.greater(crit_filter[i, :], min_factor)
        crit_filter[i, :] = np.where(cond, crit_filter[i, :], 0)
    # For each frame of input speech, calculate the Weighted Spectral Slope Measure
    num_frames = int(clean_length / skiprate - (winlength / skiprate))  # number of frames
    start = 0  # starting sample
    window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(1, winlength + 1) / (winlength + 1)))

    distortion = np.empty(num_frames)
    for frame_count in range(num_frames):
        # (1) Get the Frames for the test and reference speech. Multiply by Hanning Window.
        clean_frame = clean_speech[start: start + winlength] / 32768
        processed_frame = processed_speech[start: start + winlength] / 32768
        clean_frame = np.multiply(clean_frame, window)
        processed_frame = np.multiply(processed_frame, window)
        # (2) Compute the Power Spectrum of Clean and Processed
        # if USE_FFT_SPECTRUM:
        clean_spec = np.square(np.abs(fft(clean_frame, n_fft)))
        processed_spec = np.square(np.abs(fft(processed_frame, n_fft)))

        # (3) Compute Filterbank Output Energies (in dB scale)
        clean_energy = np.matmul(crit_filter, clean_spec[0:n_fftby2])
        processed_energy = np.matmul(crit_filter, processed_spec[0:n_fftby2])

        clean_energy = 10 * np.log10(np.maximum(clean_energy, 1E-10))
        processed_energy = 10 * np.log10(np.maximum(processed_energy, 1E-10))

        # (4) Compute Spectral Slope (dB[i+1]-dB[i])
        clean_slope = clean_energy[1:num_crit] - clean_energy[0: num_crit - 1]
        processed_slope = processed_energy[1:num_crit] - processed_energy[0: num_crit - 1]

        # (5) Find the nearest peak locations in the spectra to each critical band.
        #     If the slope is negative, we search to the left. If positive, we search to the right.
        clean_loc_peak = np.empty(num_crit - 1)
        processed_loc_peak = np.empty(num_crit - 1)

        for i in range(num_crit - 1):
            # find the peaks in the clean speech signal
            if clean_slope[i] > 0:  # search to the right
                n = i
                while (n < num_crit - 1) and (clean_slope[n] > 0):
                    n = n + 1
                clean_loc_peak[i] = clean_energy[n - 1]
            else:  # search to the left
                n = i
                while (n >= 0) and (clean_slope[n] <= 0):
                    n = n - 1
                clean_loc_peak[i] = clean_energy[n + 1]

            # find the peaks in the processed speech signal
            if processed_slope[i] > 0:  # search to the right
                n = i
                while (n < num_crit - 1) and (processed_slope[n] > 0):
                    n = n + 1
                processed_loc_peak[i] = processed_energy[n - 1]
            else:  # search to the left
                n = i
                while (n >= 0) and (processed_slope[n] <= 0):
                    n = n - 1
                processed_loc_peak[i] = processed_energy[n + 1]

        # (6) Compute the WSS Measure for this frame. This includes determination of the weighting function.
        dBMax_clean = np.max(clean_energy)
        dBMax_processed = np.max(processed_energy)
        '''
        The weights are calculated by averaging individual weighting factors from the clean and processed frame.
        These weights W_clean and W_processed should range from 0 to 1 and place more emphasis on spectral peaks
        and less emphasis on slope differences in spectral valleys.
        This procedure is described on page 1280 of Klatt's 1982 ICASSP paper.
        '''
        Wmax_clean = np.divide(Kmax, Kmax + dBMax_clean - clean_energy[0: num_crit - 1])
        Wlocmax_clean = np.divide(Klocmax, Klocmax + clean_loc_peak - clean_energy[0: num_crit - 1])
        W_clean = np.multiply(Wmax_clean, Wlocmax_clean)

        Wmax_processed = np.divide(Kmax, Kmax + dBMax_processed - processed_energy[0: num_crit - 1])
        Wlocmax_processed = np.divide(Klocmax, Klocmax + processed_loc_peak - processed_energy[0: num_crit - 1])
        W_processed = np.multiply(Wmax_processed, Wlocmax_processed)

        W = np.divide(np.add(W_clean, W_processed), 2.0)
        slope_diff = np.subtract(clean_slope, processed_slope)[0: num_crit - 1]
        distortion[frame_count] = np.dot(W, np.square(slope_diff)) / np.sum(W)
        # this normalization is not part of Klatt's paper, but helps to normalize the measure.
        # Here we scale the measure by the sum of the weights.
        start = start + skiprate
    return distortion


def calc_speech_metrics(hypothesis: np.ndarray,
                        reference: np.ndarray) -> tuple[float, int, int, int, float]:
    """
    Calculate speech metrics pesq_mos, CSIG, CBAK, COVL, segSNR.  These are all related and thus included
    in one function. Reference: matlab script "compute_metrics.m".

    Usage:
        pesq, csig, cbak, covl, ssnr = compute_metrics(hypothesis, reference, Fs, path)
        reference: clean audio as array
        hypothesis: enhanced audio as array
        Audio must have sampling rate = 16000 Hz.

    Example call:
        pesq_output, csig_output, cbak_output, covl_output, ssnr_output = \
                calc_speech_metrics(predicted_audio, target_audio)
    """
    from sonusai.metrics import calc_pesq

    Fs = 16000

    # compute the WSS measure
    wss_dist_vec = wss(reference, hypothesis, Fs)
    wss_dist_vec = np.sort(wss_dist_vec)
    alpha = 0.95  # value from CMGAN ref implementation
    wss_dist = np.mean(wss_dist_vec[0: round(np.size(wss_dist_vec) * alpha)])

    # compute the LLR measure
    llr_dist = llr(reference, hypothesis, Fs)
    ll_rs = np.sort(llr_dist)
    llr_len = round(np.size(llr_dist) * alpha)
    llr_mean = np.mean(ll_rs[0: llr_len])

    # compute the SNRseg
    snr_dist, segsnr_dist = snr(reference, hypothesis, Fs)
    snr_mean = snr_dist
    segSNR = np.mean(segsnr_dist)

    # compute the pesq (use Sonusai wrapper, only fs=16k, mode=wb support)
    pesq_mos = calc_pesq(hypothesis=hypothesis, reference=reference)
    # pesq_mos = pesq(sampling_rate1, data1, data2, 'wb')

    # now compute the composite measures
    CSIG = 3.093 - 1.029 * llr_mean + 0.603 * pesq_mos - 0.009 * wss_dist
    CSIG = max(1, CSIG)
    CSIG = min(5, CSIG)  # limit values to [1, 5]
    CBAK = 1.634 + 0.478 * pesq_mos - 0.007 * wss_dist + 0.063 * segSNR
    CBAK = max(1, CBAK)
    CBAK = min(5, CBAK)  # limit values to [1, 5]
    COVL = 1.594 + 0.805 * pesq_mos - 0.512 * llr_mean - 0.007 * wss_dist
    COVL = max(1, COVL)
    COVL = min(5, COVL)  # limit values to [1, 5]

    return pesq_mos, CSIG, CBAK, COVL, segSNR


def mean_square_error(hypothesis: np.ndarray,
                      reference: np.ndarray,
                      squared: bool = False) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate root-mean-square error or mean square error

    :param hypothesis: [frames, bins]
    :param reference: [frames, bins]
    :param squared: calculate mean square rather than root-mean-square
    :return: mean, mean per bin, mean per frame
    """
    sq_err = np.square(reference - hypothesis)

    # mean over frames for value per bin
    err_b = np.mean(sq_err, axis=0)
    # mean over bins for value per frame
    err_f = np.mean(sq_err, axis=1)
    # mean over all
    err = np.mean(sq_err)

    if not squared:
        err_b = np.sqrt(err_b)
        err_f = np.sqrt(err_f)
        err = np.sqrt(err)

    return err, err_b, err_f


def mean_abs_percentage_error(hypothesis: np.ndarray,
                              reference: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate mean abs percentage error

    If inputs are complex, calculates average: mape(real)/2 + mape(imag)/2

    :param hypothesis: [frames, bins]
    :param reference: [frames, bins]
    :return: mean, mean per bin, mean per frame
    """
    if not np.iscomplexobj(reference) and not np.iscomplexobj(hypothesis):
        abs_err = 100 * np.abs((reference - hypothesis) / (reference + np.finfo(np.float32).eps))
    else:
        reference_r = np.real(reference)
        reference_i = np.imag(reference)
        hypothesis_r = np.real(hypothesis)
        hypothesis_i = np.imag(hypothesis)
        abs_err_r = 100 * np.abs((reference_r - hypothesis_r) / (reference_r + np.finfo(np.float32).eps))
        abs_err_i = 100 * np.abs((reference_i - hypothesis_i) / (reference_i + np.finfo(np.float32).eps))
        abs_err = (abs_err_r / 2) + (abs_err_i / 2)

    # mean over frames for value per bin
    err_b = np.around(np.mean(abs_err, axis=0), 3)
    # mean over bins for value per frame
    err_f = np.around(np.mean(abs_err, axis=1), 3)
    # mean over all
    err = np.around(np.mean(abs_err), 3)

    return err, err_b, err_f


def log_error(reference: np.ndarray, hypothesis: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate log error

    :param reference: complex or real [frames, bins]
    :param hypothesis: complex or real [frames, bins]
    :return: mean, mean per bin, mean per frame
    """
    reference_sq = np.real(reference * np.conjugate(reference))
    hypothesis_sq = np.real(hypothesis * np.conjugate(hypothesis))
    log_err = abs(10 * np.log10((reference_sq + np.finfo(np.float32).eps) / (hypothesis_sq + np.finfo(np.float32).eps)))
    # log_err = abs(10 * np.log10(reference_sq / (hypothesis_sq + np.finfo(np.float32).eps) + np.finfo(np.float32).eps))

    # mean over frames for value per bin
    err_b = np.around(np.mean(log_err, axis=0), 3)
    # mean over bins for value per frame
    err_f = np.around(np.mean(log_err, axis=1), 3)
    # mean over all
    err = np.around(np.mean(log_err), 3)

    return err, err_b, err_f


def phase_distance(reference: np.ndarray,
                   hypothesis: np.ndarray,
                   eps: float = 1e-9) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate weighted phase distance error (weight normalization over bins per frame)

    :param reference: complex [frames, bins]
    :param hypothesis: complex [frames, bins]
    :param eps: epsilon value
    :return: mean, mean per bin, mean per frame
    """
    ang_diff = np.angle(reference) - np.angle(hypothesis)
    phd_mod = (ang_diff + np.pi) % (2 * np.pi) - np.pi
    rh_angle_diff = phd_mod * 180 / np.pi  # angle diff in deg

    # Use complex divide to intrinsically keep angle diff +/-180 deg, but avoid div by zero (real hyp)
    # hyp_real = np.real(hypothesis)
    # near_zeros = np.real(hyp_real) < eps
    # hyp_real = hyp_real * (np.logical_not(near_zeros))
    # hyp_real = hyp_real + (near_zeros * eps)
    # hypothesis = hyp_real + 1j*np.imag(hypothesis)
    # rh_angle_diff = np.angle(reference / hypothesis) * 180 / np.pi  # angle diff +/-180

    # weighted mean over all (scalar)
    reference_mag = np.abs(reference)
    ref_weight = reference_mag / (np.sum(reference_mag) + eps)  # frames x bins
    err = np.around(np.sum(ref_weight * rh_angle_diff), 3)

    # weighted mean over frames (value per bin)
    err_b = np.zeros(reference.shape[1])
    for bi in range(reference.shape[1]):
        ref_weight = reference_mag[:, bi] / (np.sum(reference_mag[:, bi], axis=0) + eps)
        err_b[bi] = np.around(np.sum(ref_weight * rh_angle_diff[:, bi]), 3)

    # weighted mean over bins (value per frame)
    err_f = np.zeros(reference.shape[0])
    for fi in range(reference.shape[0]):
        ref_weight = reference_mag[fi, :] / (np.sum(reference_mag[fi, :]) + eps)
        err_f[fi] = np.around(np.sum(ref_weight * rh_angle_diff[fi, :]), 3)

    return err, err_b, err_f


def plot_mixpred(mixture: AudioT,
                 mixture_f: AudioF,
                 target: Optional[AudioT] = None,
                 feature: Optional[Feature] = None,
                 predict: Optional[Predict] = None,
                 tp_title: str = '') -> plt.Figure:
    from sonusai.mixture import SAMPLE_RATE

    num_plots = 2
    if feature is not None:
        num_plots += 1
    if predict is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    p = 0
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[p].plot(x_axis, mixture, label='Mixture', color='mistyrose')
    ax[0].set_ylabel('magnitude', color='tab:blue')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    if target is not None:  # Plot target time-domain waveform on top of mixture
        ax[0].plot(x_axis, target, label='Target', color='tab:blue')
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[p].set_title('Waveform')

    # Plot the mixture spectrogram
    p += 1
    ax[p].imshow(np.transpose(mixture_f), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Mixture')

    if feature is not None:
        p += 1
        ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Feature')

    if predict is not None:
        p += 1
        im = ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + tp_title)
        plt.colorbar(im, location='bottom')

    return fig


def plot_pdb_predtruth(predict: np.ndarray,
                       truth_f: Optional[np.ndarray] = None,
                       metric: Optional[np.ndarray] = None,
                       tp_title: str = '') -> plt.Figure:
    """Plot predict and optionally truth and a metric in power db, e.g. applies 10*log10(predict)"""
    num_plots = 2
    if truth_f is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    tmp = 10 * np.log10(predict.transpose() + np.finfo(np.float32).eps)
    im = ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')
    plt.colorbar(im, location='bottom')

    if truth_f is not None:
        p += 1
        tmp = 10 * np.log10(truth_f.transpose() + np.finfo(np.float32).eps)
        im = ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')
        plt.colorbar(im, location='bottom')

    # Plot the predict avg, and optionally truth avg and metric lines
    pred_avg = 10 * np.log10(np.mean(predict, axis=-1) + np.finfo(np.float32).eps)
    p += 1
    x_axis = np.arange(len(pred_avg), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, pred_avg, color='black', linestyle='dashed', label='Predict mean over freq.')
    ax[p].set_ylabel('mean db', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_f is not None:
        truth_avg = 10 * np.log10(np.mean(truth_f, axis=-1) + np.finfo(np.float32).eps)
        ax[p].plot(x_axis, truth_avg, color='green', linestyle='dashed', label='Truth mean over freq.')

    if metric is not None:  # instantiate 2nd y-axis that shares the same x-axis
        ax2 = ax[p].twinx()
        color2 = 'red'
        ax2.plot(x_axis, metric, color=color2, label='sig distortion (mse db)')
        ax2.set_xlim(x_axis[0], x_axis[-1])
        ax2.set_ylim([0, np.max(metric)])
        ax2.set_ylabel('spectral distortion (mse db)', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        ax[p].set_title('SNR and SNR mse (mean over freq. db)')
    else:
        ax[p].set_title('SNR (mean over freq. db)')
        # ax[0].tick_params(axis='y', labelcolor=color)
    return fig


def plot_epredtruth(predict: np.ndarray,
                    predict_wav: np.ndarray,
                    truth_f: Optional[np.ndarray] = None,
                    truth_wav: Optional[np.ndarray] = None,
                    metric: Optional[np.ndarray] = None,
                    tp_title: str = '') -> plt.Figure:
    """Plot predict spectrogram and waveform and optionally truth and a metric)"""
    num_plots = 2
    if truth_f is not None:
        num_plots += 1
    if metric is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    im = ax[p].imshow(predict.transpose(), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')
    plt.colorbar(im, location='bottom')

    if truth_f is not None:  # plot truth if provided and use same colormap as predict
        p += 1
        ax[p].imshow(truth_f.transpose(), im.cmap, aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')

    # Plot the predict wav, and optionally truth avg and metric lines
    p += 1
    x_axis = np.arange(len(predict_wav), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, predict_wav, color='black', linestyle='dashed', label='Speech Estimate')
    ax[p].set_ylabel('Amplitude', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_wav is not None:
        ntrim = len(truth_wav) - len(predict_wav)
        if ntrim > 0:
            truth_wav = truth_wav[0:-ntrim]
        ax[p].plot(x_axis, truth_wav, color='green', linestyle='dashed', label='True Target')

    # Plot the metric lines
    if metric is not None:
        p += 1
        if metric.ndim > 1:  # if it has multiple dims, plot 1st
            metric1 = metric[:, 0]
        else:
            metric1 = metric  # if single dim, plot it as 1st
        x_axis = np.arange(len(metric1), dtype=np.float32)  # / SAMPLE_RATE
        ax[p].plot(x_axis, metric1, color='red', label='Target LogErr')
        ax[p].set_ylabel('log error db', color='red')
        ax[p].set_xlim(x_axis[0], x_axis[-1])
        ax[p].set_ylim([-0.01, np.max(metric1) + .01])
        if metric.ndim > 1:
            if metric.shape[1] > 1:
                metr2 = metric[:, 1]
                ax2 = ax[p].twinx()
                color2 = 'blue'
                ax2.plot(x_axis, metr2, color=color2, label='phase dist (deg)')
                # ax2.set_ylim([-180.0, +180.0])
                if np.max(metr2) - np.min(metr2) > .1:
                    ax2.set_ylim([np.min(metr2), np.max(metr2)])
                ax2.set_ylabel('phase dist (deg)', color=color2)
                ax2.tick_params(axis='y', labelcolor=color2)
                # ax[p].set_title('SNR and SNR mse (mean over freq. db)')

    return fig


def _process_mixture(mixid: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    from os.path import basename
    from os.path import join
    from os.path import splitext

    import h5py
    from numpy import inf
    from pystoi import stoi

    from sonusai import SonusAIError
    from sonusai import logger
    from sonusai.metrics import calc_pcm
    from sonusai.metrics import calc_wer
    from sonusai.metrics import calc_wsdr
    from sonusai.mixture import forward_transform
    from sonusai.mixture import inverse_transform
    from sonusai.mixture import read_audio
    from sonusai.utils import calc_asr
    from sonusai.utils import float_to_int16
    from sonusai.utils import reshape_outputs
    from sonusai.utils import stack_complex
    from sonusai.utils import unstack_complex
    from sonusai.utils import write_wav

    mixdb = MP_GLOBAL.mixdb
    predict_location = MP_GLOBAL.predict_location
    predwav_mode = MP_GLOBAL.predwav_mode
    truth_est_mode = MP_GLOBAL.truth_est_mode
    enable_plot = MP_GLOBAL.enable_plot
    enable_wav = MP_GLOBAL.enable_wav
    wer_method = MP_GLOBAL.wer_method
    whisper_model = MP_GLOBAL.whisper_model

    # 1)  Read predict data, var predict with shape [BatchSize,Classes] or [BatchSize,Tsteps,Classes]
    output_name = join(predict_location, mixdb.mixture(mixid).name)
    predict = None
    if truth_est_mode:
        # in truth estimation mode we use the truth in place of prediction to see metrics with perfect input
        # don't bother to read prediction, and predict var will get assigned to truth later
        # mark outputs with tru suffix, i.e. 0000_truest_*
        base_name = splitext(output_name)[0] + '_truest'
    else:
        base_name, ext = splitext(output_name)  # base_name used later
        if not predwav_mode:
            try:
                with h5py.File(output_name, 'r') as f:
                    predict = np.array(f['predict'])
            except Exception as e:
                raise SonusAIError(f'Error reading {output_name}: {e}')
            # reshape to always be [frames,classes] where ndim==3 case frames = batch * tsteps
            if predict.ndim > 2:  # TBD generalize to somehow detect if timestep dim exists, some cases > 2 don't have
                # logger.debug(f'Prediction reshape from {predict.shape} to remove timestep dimension.')
                predict, _ = reshape_outputs(predict=predict, truth=None, timesteps=predict.shape[1])
        else:
            base_name, ext = splitext(output_name)
            prfname = join(base_name + '.wav')
            audio = read_audio(prfname)
            predict = forward_transform(audio, mixdb.ft_config)
            if mixdb.feature[0:1] == 'h':
                predict = power_compress(predict)
            predict = stack_complex(predict)

    # 2) Collect true target, noise, mixture data, trim to predict size if needed
    target = mixdb.mixture_target(mixid)
    target_f = mixdb.mixture_target_f(mixid, target=target)
    noise = mixdb.mixture_noise(mixid)
    noise_f = mixdb.mixture_noise_f(mixid, noise=noise)
    mixture = mixdb.mixture_mixture(mixid, target=target, noise=noise)
    mixture_f = mixdb.mixture_mixture_f(mixid, mixture=mixture)
    segsnr_f = mixdb.mixture_segsnr(mixid, target=target, noise=noise)
    segsnr_f[segsnr_f == inf] = 7.944e8  # 99db
    segsnr_f[segsnr_f == -inf] = 1.258e-10  # -99db
    # need to use inv-tf to match #samples & latency shift properties of predict inv tf
    targetfi = inverse_transform(target_f, mixdb.it_config)
    noisefi = inverse_transform(noise_f, mixdb.it_config)
    # mixturefi = mixdb.inverse_transform(mixture_f)

    # gen feature, truth - note feature only used for plots
    # TBD parse truth_f for different formats and also multi-truth
    feature, truth_f = mixdb.mixture_ft(mixid, mixture=mixture)
    truth_type = mixdb.target_file(mixdb.mixture(mixid).targets[0].file_id).truth_settings[0].function
    if truth_type == 'target_mixture_f':
        half = truth_f.shape[-1] // 2
        truth_f = truth_f[..., :half]  # extract target_f only

    if not truth_est_mode:
        if predict.shape[0] < target_f.shape[0]:  # target_f, truth_f, mixture_f, etc. same size
            trimf = target_f.shape[0] - predict.shape[0]
            logger.debug(f'Warning: prediction frames less than mixture, trimming {trimf} frames from all truth.')
            target_f = target_f[0:-trimf, :]
            targetfi, _ = inverse_transform(target_f, mixdb.it_config)
            trimt = target.shape[0] - targetfi.shape[0]
            target = target[0:-trimt]
            noise_f = noise_f[0:-trimf, :]
            noise = noise[0:-trimt]
            mixture_f = mixture_f[0:-trimf, :]
            mixture = mixture[0:-trimt]
            truth_f = truth_f[0:-trimf, :]
        elif predict.shape[0] > target_f.shape[0]:
            raise SonusAIError(
                f'Error: prediction has more frames than true mixture {predict.shape[0]} vs {truth_f.shape[0]}')

    # 3) Extraction - format proper complex and wav estimates and truth (unstack, uncompress, inv tf, etc.)
    if truth_est_mode:
        predict = truth_f  # substitute truth for the prediction (for test/debug)
        predict_complex = unstack_complex(predict)  # unstack
        # if feat has compressed mag and truth does not, compress it
        if mixdb.feature[0:1] == 'h' and mixdb.target_file(1).truth_settings[0].function[0:10] != 'targetcmpr':
            predict_complex = power_compress(predict_complex)  # from uncompressed truth
    else:
        predict_complex = unstack_complex(predict)

    truth_f_complex = unstack_complex(truth_f)
    if mixdb.feature[0:1] == 'h':  # 'hn' or 'ha' or 'hd', etc.:  # if feat has compressed mag
        # estimate noise in uncompressed-mag domain
        noise_est_complex = mixture_f - power_uncompress(predict_complex)
        predict_complex = power_uncompress(predict_complex)  # uncompress if truth is compressed
    else:  # cn, c8, ..
        noise_est_complex = mixture_f - predict_complex

    target_est_wav = inverse_transform(predict_complex, mixdb.it_config)
    noise_est_wav = inverse_transform(noise_est_complex, mixdb.it_config)

    # 4) Metrics
    # Target/Speech logerr - PSD estimation accuracy symmetric mean log-spectral distortion
    lerr_tg, lerr_tg_bin, lerr_tg_frame = log_error(reference=truth_f_complex, hypothesis=predict_complex)
    # Noise logerr - PSD estimation accuracy
    lerr_n, lerr_n_bin, lerr_n_frame = log_error(reference=noise_f, hypothesis=noise_est_complex)
    # PCM loss metric
    ytrue_f = np.concatenate((truth_f_complex[:, np.newaxis, :], noise_f[:, np.newaxis, :]), axis=1)
    ypred_f = np.concatenate((predict_complex[:, np.newaxis, :], noise_est_complex[:, np.newaxis, :]), axis=1)
    pcm, pcm_bin, pcm_frame = calc_pcm(hypothesis=ypred_f, reference=ytrue_f, with_log=True)

    # Phase distance
    phd, phd_bin, phd_frame = phase_distance(hypothesis=predict_complex, reference=truth_f_complex)

    # Noise td logerr
    # lerr_nt, lerr_nt_bin, lerr_nt_frame = log_error(noisefi, noise_truth_est_audio)

    # # SA-SDR (time-domain source-aggragated SDR)
    ytrue = np.concatenate((targetfi[:, np.newaxis], noisefi[:, np.newaxis]), axis=1)
    ypred = np.concatenate((target_est_wav[:, np.newaxis], noise_est_wav[:, np.newaxis]), axis=1)
    # # note: w/o scale is more pessimistic number
    # sa_sdr, _ = calc_sa_sdr(hypothesis=ypred, reference=ytrue)
    target_stoi = stoi(targetfi, target_est_wav, 16000, extended=False)

    wsdr, wsdr_cc, wsdr_cw = calc_wsdr(hypothesis=ypred, reference=ytrue, with_log=True)
    # logger.debug(f'wsdr weight sum for mixid {mixid} = {np.sum(wsdr_cw)}.')
    # logger.debug(f'wsdr cweights = {wsdr_cw}.')
    # logger.debug(f'wsdr ccoefs for mixid {mixid} = {wsdr_cc}.')

    # Speech intelligibility measure - PESQ
    if int(mixdb.mixture(mixid).snr) > -99:
        # len = target_est_wav.shape[0]
        pesq_speech, csig_tg, cbak_tg, covl_tg, sgsnr_tg = calc_speech_metrics(target_est_wav, targetfi)
        pesq_mixture, csig_mx, cbak_mx, covl_mx, sgsnr_mx = calc_speech_metrics(mixture, target)
        # pesq_speech_tst = calc_pesq(hypothesis=target_est_wav, reference=target)
        # pesq_mixture_tst = calc_pesq(hypothesis=mixture, reference=target)
        # pesq improvement
        pesq_impr = pesq_speech - pesq_mixture
        # pesq improvement %
        pesq_impr_pc = pesq_impr / (pesq_mixture + np.finfo(np.float32).eps) * 100
    else:
        pesq_speech = 0
        pesq_mixture = 0
        pesq_impr_pc = np.float32(0)
        csig_mx = 0
        csig_tg = 0
        cbak_mx = 0
        cbak_tg = 0
        covl_mx = 0
        covl_tg = 0

    # Calc WER
    asr_tt = ''
    asr_mx = ''
    asr_tge = ''
    if wer_method == 'none' or mixdb.mixture(mixid).snr == -99:  # noise only, ignore/reset target asr
        wer_mx = float('nan')
        wer_tge = float('nan')
        wer_pi = float('nan')
    else:
        if MP_GLOBAL.mixdb.asr_manifests:
            asr_tt = MP_GLOBAL.mixdb.mixture_asr_data(mixid)[0]  # ignore mixup
        else:
            asr_tt = calc_asr(target, engine=wer_method, whisper_model_name=whisper_model).text  # target truth

        if asr_tt:
            asr_mx = calc_asr(mixture, engine=wer_method, whisper_model=whisper_model).text
            asr_tge = calc_asr(target_est_wav, engine=wer_method, whisper_model=whisper_model).text

            wer_mx = calc_wer(asr_mx, asr_tt).wer * 100  # mixture wer
            wer_tge = calc_wer(asr_tge, asr_tt).wer * 100  # target estimate wer
            if wer_mx == 0.0:
                if wer_tge == 0.0:
                    wer_pi = 0.0
                else:
                    wer_pi = -999.0
            else:
                wer_pi = 100 * (wer_mx - wer_tge) / wer_mx
        else:
            print(f'Warning: mixid {mixid} asr truth is empty, setting to 0% wer')
            wer_mx = float(0)
            wer_tge = float(0)
            wer_pi = float(0)

    # 5) Save per mixture metric results
    # Single row in table of scalar metrics per mixture
    mtable1_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi%', 'MXWER', 'WER', 'WERi%', 'WSDR', 'STOI',
                   'PCM', 'SPLERR', 'NLERR', 'PD', 'MXCSIG', 'CSIG', 'MXCBAK', 'CBAK', 'MXCOVL', 'COVL',
                   'SPFILE', 'NFILE']
    ti = mixdb.mixture(mixid).targets[0].file_id
    ni = mixdb.mixture(mixid).noise.file_id
    metr1 = [mixdb.mixture(mixid).snr, pesq_mixture, pesq_speech, pesq_impr_pc, wer_mx, wer_tge, wer_pi, wsdr,
             target_stoi, pcm, lerr_tg, lerr_n, phd, csig_mx, csig_tg, cbak_mx, cbak_tg, covl_mx, covl_tg,
             basename(mixdb.target_file(ti).name), basename(mixdb.noise_file(ni).name)]
    mtab1 = pd.DataFrame([metr1], columns=mtable1_col, index=[mixid])

    # Stats of per frame estimation metrics
    metr2 = pd.DataFrame({'SSNR':  segsnr_f,
                          'PCM':   pcm_frame,
                          'SLERR': lerr_tg_frame,
                          'NLERR': lerr_n_frame,
                          'SPD':   phd_frame})
    metr2 = metr2.describe()  # Use pandas stat function
    metr2['SSNR'][1:] = metr2['SSNR'][1:].apply(
        lambda x: 10 * np.log10(x + 1.01e-10))  # Change SSNR stats to dB, except count
    # create a single row in multi-column header
    new_labels = pd.MultiIndex.from_product([metr2.columns,
                                             ['Avg', 'Min', 'Med', 'Max', 'Std']],
                                            names=['Metric', 'Stat'])
    dat1row = metr2.loc[['mean', 'min', '50%', 'max', 'std'], :].T.stack().to_numpy().reshape((1, -1))
    mtab2 = pd.DataFrame(dat1row,
                         index=[mixid],
                         columns=new_labels)
    mtab2.insert(0, 'MXSNR', mixdb.mixture(mixid).snr, False)  # add MXSNR as the first metric column

    all_metrics_table_1 = mtab1  # return to be collected by process
    all_metrics_table_2 = mtab2  # return to be collected by process

    metric_name = base_name + '_metric_spenh.txt'
    with open(metric_name, 'w') as f:
        print('Speech enhancement metrics:', file=f)
        print(mtab1.round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
        print('', file=f)
        print(f'Extraction statistics over {mixture_f.shape[0]} frames:', file=f)
        print(metr2.round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
        print('', file=f)
        print(f'Target path: {mixdb.target_file(ti).name}', file=f)
        print(f'Noise path: {mixdb.noise_file(ni).name}', file=f)
        if wer_method != 'none':
            print(f'WER method: {wer_method} and whisper model (if used):  {whisper_model}', file=f)
            if mixdb.asr_manifests:
                print(f'ASR truth from manifest:  {asr_tt}', file=f)
            else:
                print(f'ASR truth from wer method:  {asr_tt}', file=f)
            print(f'ASR result for mixture:  {asr_mx}', file=f)
            print(f'ASR result for prediction:  {asr_tge}', file=f)

        print(f'Augmentations: {mixdb.mixture(mixid)}', file=f)

    # 7) write wav files
    if enable_wav:
        write_wav(name=base_name + '_mixture.wav', audio=float_to_int16(mixture))
        write_wav(name=base_name + '_target.wav', audio=float_to_int16(target))
        # write_wav(name=base_name + '_targetfi.wav', audio=float_to_int16(targetfi))
        write_wav(name=base_name + '_noise.wav', audio=float_to_int16(noise))
        write_wav(name=base_name + '_target_est.wav', audio=float_to_int16(target_est_wav))
        write_wav(name=base_name + '_noise_est.wav', audio=float_to_int16(noise_est_wav))

        # debug code to test for perfect reconstruction of the extraction method
        # note both 75% olsa-hanns and 50% olsa-hann modes checked to have perfect reconstruction
        # target_r = mixdb.inverse_transform(target_f)
        # noise_r = mixdb.inverse_transform(noise_f)
        # _write_wav(name=base_name + '_target_r.wav', audio=float_to_int16(target_r))
        # _write_wav(name=base_name + '_noise_r.wav', audio=float_to_int16(noise_r)) # chk perfect rec

    # 8) Write out plot file
    if enable_plot:
        from matplotlib.backends.backend_pdf import PdfPages
        plot_fname = base_name + '_metric_spenh.pdf'

        # Reshape feature to eliminate overlap redundancy for easier to understand spectrogram view
        # Original size (frames, stride, num_bands), decimates in stride dimension only if step is > 1
        # Reshape to get frames*decimated_stride, num_bands
        step = int(mixdb.feature_samples / mixdb.feature_step_samples)
        if feature.ndim != 3:
            raise SonusAIError(f'feature does not have 3 dimensions: frames, stride, num_bands')

        # for feature cn*00n**
        feat_sgram = unstack_complex(feature)
        feat_sgram = 20 * np.log10(abs(feat_sgram) + np.finfo(np.float32).eps)
        feat_sgram = feat_sgram[:, -step:, :]  # decimate,  Fx1xB
        feat_sgram = np.reshape(feat_sgram, (feat_sgram.shape[0] * feat_sgram.shape[1], feat_sgram.shape[2]))

        with PdfPages(plot_fname) as pdf:
            # page1 we always have a mixture and prediction, target optional if truth provided
            tfunc_name = mixdb.target_file(1).truth_settings[0].function  # first target, assumes all have same
            if tfunc_name == 'mapped_snr_f':
                # leave as unmapped snr
                predplot = predict
                tfunc_name = mixdb.target_file(1).truth_settings[0].function
            elif tfunc_name == 'target_f' or 'target_mixture_f':
                predplot = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            else:
                # use dB scale
                predplot = 10 * np.log10(predict + np.finfo(np.float32).eps)
                tfunc_name = tfunc_name + ' (db)'

            mixspec = 20 * np.log10(abs(mixture_f) + np.finfo(np.float32).eps)
            pdf.savefig(plot_mixpred(mixture=mixture,
                                     mixture_f=mixspec,
                                     target=target,
                                     feature=feat_sgram,
                                     predict=predplot,
                                     tp_title=tfunc_name))

            # ----- page 2, plot unmapped predict, opt truth reconstructed and line plots of mean-over-f
            # pdf.savefig(plot_pdb_predtruth(predict=pred_snr_f, tp_title='predict snr_f (db)'))

            # page 3 speech extraction
            tg_spec = 20 * np.log10(abs(target_f) + np.finfo(np.float32).eps)
            tg_est_spec = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            # n_spec = np.reshape(n_spec,(n_spec.shape[0] * n_spec.shape[1], n_spec.shape[2]))
            pdf.savefig(plot_epredtruth(predict=tg_est_spec,
                                        predict_wav=target_est_wav,
                                        truth_f=tg_spec,
                                        truth_wav=targetfi,
                                        metric=np.vstack((lerr_tg_frame, phd_frame)).T,
                                        tp_title='speech estimate'))

            # page 4 noise extraction
            n_spec = 20 * np.log10(abs(noise_f) + np.finfo(np.float32).eps)
            n_est_spec = 20 * np.log10(abs(noise_est_complex) + np.finfo(np.float32).eps)
            pdf.savefig(plot_epredtruth(predict=n_est_spec,
                                        predict_wav=noise_est_wav,
                                        truth_f=n_spec,
                                        truth_wav=noisefi,
                                        metric=lerr_n_frame,
                                        tp_title='noise estimate'))

            # Plot error waveforms
            # tg_err_wav = targetfi - target_est_wav
            # tg_err_spec = 20*np.log10(np.abs(target_f - predict_complex))

        plt.close('all')

    return all_metrics_table_1, all_metrics_table_2


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    predict_location = args['PLOC']
    wer_method = args['--wer-method'].lower()
    truth_est_mode = args['--truth-est-mode']
    enable_plot = args['--plot']
    enable_wav = args['--wav']
    enable_summary = args['--summary']
    truth_location = args['TLOC']
    whisper_model = args['--whisper-model'].lower()

    import glob
    from os.path import basename
    from os.path import isdir
    from os.path import join
    from os.path import split

    from tqdm import tqdm

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import DEFAULT_NOISE
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import read_audio
    from sonusai.utils import calc_asr
    from sonusai.utils import pp_tqdm_imap

    # Check prediction subdirectory
    if not isdir(predict_location):
        print(f'The specified predict location {predict_location} is not a valid subdirectory path, exiting ...')

    # allpfiles = listdir(predict_location)
    allpfiles = glob.glob(predict_location + "/*.h5")
    predict_logfile = glob.glob(predict_location + "/*predict.log")
    predwav_mode = False
    if len(allpfiles) <= 0 and not truth_est_mode:
        allpfiles = glob.glob(predict_location + "/*.wav")  # check for wav files
        if len(allpfiles) <= 0:
            print(f'Subdirectory {predict_location} has no .h5 or .wav files, exiting ...')
        else:
            logger.info(f'Found {len(allpfiles)} prediction .wav files.')
            predwav_mode = True
    else:
        logger.info(f'Found {len(allpfiles)} prediction .h5 files.')

    if len(predict_logfile) == 0:
        logger.info(f'Warning, predict location {predict_location} has no prediction log files.')
    else:
        logger.info(f'Found predict log {basename(predict_logfile[0])} in predict location.')

    # Setup logging file
    create_file_handler(join(predict_location, 'calc_metric_spenh.log'))
    update_console_handler(verbose)
    initial_log_messages('calc_metric_spenh')

    mixdb = MixtureDatabase(truth_location)
    mixids = mixdb.mixids_to_list(mixids)
    logger.info(
        f'Found mixdb of {mixdb.num_mixtures} total mixtures, with {mixdb.num_classes} classes in {truth_location}')
    logger.info(f'Only running specified subset of {len(mixids)} mixtures')

    enable_asr_warmup = False
    if wer_method == 'none':
        fnb = 'metric_spenh_'
    elif wer_method == 'google':
        fnb = 'metric_spenh_ggl_'
        logger.info(f'WER enabled with method {wer_method}')
        enable_asr_warmup = True
    elif wer_method == 'deepgram':
        fnb = 'metric_spenh_dgram_'
        logger.info(f'WER enabled with method {wer_method}')
        enable_asr_warmup = True
    elif wer_method == 'aixplain_whisper':
        fnb = 'metric_spenh_whspx_' + whisper_model + '_'
        logger.info(f'WER enabled with method {wer_method} and whisper model {whisper_model}')
        enable_asr_warmup = True
    elif wer_method == 'whisper':
        fnb = 'metric_spenh_whspl_' + whisper_model + '_'
        logger.info(f'WER enabled with method {wer_method} and whisper model {whisper_model}')
        enable_asr_warmup = True
    elif wer_method == 'aaware_whisper':
        fnb = 'metric_spenh_whspaaw_' + whisper_model + '_'
        logger.info(f'WER enabled with method {wer_method} and whisper model {whisper_model}')
        enable_asr_warmup = True
    elif wer_method == 'fastwhisper':
        fnb = 'metric_spenh_fwhsp_' + whisper_model + '_'
        logger.info(f'WER enabled with method {wer_method} and whisper model {whisper_model}')
        enable_asr_warmup = True
    else:
        logger.error(f'Unrecognized WER method: {wer_method}')
        return

    if enable_asr_warmup:
        DEFAULT_SPEECH = split(DEFAULT_NOISE)[0] + '/speech_ma01_01.wav'
        audio = read_audio(DEFAULT_SPEECH)
        logger.info(f'Warming up asr method, note for cloud service this could take up to a few min ...')
        asr_chk = calc_asr(audio, engine=wer_method, whisper_model_name=whisper_model)
        logger.info(f'Warmup completed, results {asr_chk}')

    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.predict_location = predict_location
    MP_GLOBAL.predwav_mode = predwav_mode
    MP_GLOBAL.truth_est_mode = truth_est_mode
    MP_GLOBAL.enable_plot = enable_plot
    MP_GLOBAL.enable_wav = enable_wav
    MP_GLOBAL.wer_method = wer_method
    MP_GLOBAL.whisper_model = whisper_model

    # Individual mixtures use pandas print, set precision to 2 decimal places
    # pd.set_option('float_format', '{:.2f}'.format)
    progress = tqdm(total=len(mixids), desc='calc_metric_spenh')
    all_metrics_tables = pp_tqdm_imap(_process_mixture, mixids, progress=progress, num_cpus=None)
    progress.close()

    all_metrics_table_1 = pd.concat([item[0] for item in all_metrics_tables])
    all_metrics_table_2 = pd.concat([item[1] for item in all_metrics_tables])

    if not enable_summary:
        return

    # 9) Done with mixtures, write out summary metrics
    # Calculate SNR summary avg of each non-random snr
    all_mtab1_sorted = all_metrics_table_1.sort_values(by=['MXSNR', 'SPFILE'])
    all_mtab2_sorted = all_metrics_table_2.sort_values(by=['MXSNR'])
    mtab_snr_summary = None
    mtab_snr_summary_em = None
    for snri in range(0, len(mixdb.snrs)):
        tmp = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(numeric_only=True).to_frame().T
        # avoid nan when subset of mixids specified
        if ~np.isnan(tmp.iloc[0].to_numpy()[0]).any():
            mtab_snr_summary = pd.concat([mtab_snr_summary, tmp])

        tmp = all_mtab2_sorted[all_mtab2_sorted['MXSNR'] == mixdb.snrs[snri]].mean(numeric_only=True).to_frame().T
        # avoid nan when subset of mixids specified (mxsnr will be nan if no data):
        if ~np.isnan(tmp.iloc[0].to_numpy()[0]).any():
            mtab_snr_summary_em = pd.concat([mtab_snr_summary_em, tmp])

    # Correct percentages in snr summary table
    mtab_snr_summary['PESQi%'] = 100 * (mtab_snr_summary['PESQ'] - mtab_snr_summary['MXPESQ']) / np.maximum(
        mtab_snr_summary['MXPESQ'], 0.01)
    for i in range(len(mtab_snr_summary)):
        if mtab_snr_summary['MXWER'].iloc[i] == 0.0:
            if mtab_snr_summary['WER'].iloc[i] == 0.0:
                mtab_snr_summary['WERi%'].iloc[i] = 0.0
            else:
                mtab_snr_summary['WERi%'].iloc[i] = -999.0
        else:
            mtab_snr_summary['WERi%'].iloc[i] = 100 * (mtab_snr_summary['MXWER'].iloc[i] -
                                                       mtab_snr_summary['WER'].iloc[i]) / \
                                                mtab_snr_summary['MXWER'].iloc[i]

    # Calculate avg metrics over all mixtures except -99
    all_mtab1_sorted_nom99 = all_mtab1_sorted[all_mtab1_sorted.MXSNR != -99]
    all_nom99_mean = all_mtab1_sorted_nom99.mean(numeric_only=True)

    # correct the percentage averages with a direct calculation (PESQ% and WER%):
    # ser.iloc[pos]
    all_nom99_mean['PESQi%'] = (100 * (all_nom99_mean['PESQ'] - all_nom99_mean['MXPESQ'])
                                / np.maximum(all_nom99_mean['MXPESQ'], 0.01))  # pesq%
    # all_nom99_mean[3] = 100 * (all_nom99_mean[2] - all_nom99_mean[1]) / np.maximum(all_nom99_mean[1], 0.01)  # pesq%
    if all_nom99_mean['MXWER'] == 0.0:
        if all_nom99_mean['WER'] == 0.0:
            all_nom99_mean['WERi%'] = 0.0
        else:
            all_nom99_mean['WERi%'] = -999.0
    else:  # wer%
        all_nom99_mean['WERi%'] = 100 * (all_nom99_mean['MXWER'] - all_nom99_mean['WER']) / all_nom99_mean['MXWER']

    num_mix = len(mixids)
    if num_mix > 1:
        # Print pandas data to files using precision to 2 decimals
        # pd.set_option('float_format', '{:.2f}'.format)
        csp = 0

        if not truth_est_mode:
            ofname = join(predict_location, fnb + 'summary.txt')
        else:
            ofname = join(predict_location, fnb + 'summary_truest.txt')

        with open(ofname, 'w') as f:
            print(f'WER enabled with method {wer_method}, whisper model, if used: {whisper_model}', file=f)
            print(f'Speech enhancement metrics avg over all {len(all_mtab1_sorted_nom99)} non -99 SNR mixtures:',
                  file=f)
            print(all_nom99_mean.to_frame().T.round(2).to_string(float_format=lambda x: "{:.2f}".format(x),
                                                                 index=False), file=f)
            print(f'\nSpeech enhancement metrics avg over each SNR:', file=f)
            print(mtab_snr_summary.round(2).to_string(float_format=lambda x: "{:.2f}".format(x), index=False), file=f)
            print('', file=f)
            print(f'Extraction statistics stats avg over each SNR:', file=f)
            # with pd.option_context('display.max_colwidth', 9):
            # with pd.set_option('float_format', '{:.1f}'.format):
            print(mtab_snr_summary_em.round(1).to_string(float_format=lambda x: "{:.1f}".format(x), index=False),
                  file=f)
            print('', file=f)
            # pd.set_option('float_format', '{:.2f}'.format)

            print(f'Speech enhancement metrics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_1.describe().round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
            print('', file=f)
            print(f'Extraction statistics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_2.describe().round(2).to_string(float_format=lambda x: "{:.1f}".format(x)), file=f)
            print('', file=f)

            print('Speech enhancement metrics all-mixtures list:', file=f)
            # print(all_metrics_table_1.head().style.format(precision=2), file=f)
            print(all_metrics_table_1.round(2).to_string(float_format=lambda x: "{:.2f}".format(x)), file=f)
            print('', file=f)
            print('Extraction statistics all-mixtures list:', file=f)
            print(all_metrics_table_2.round(2).to_string(float_format=lambda x: "{:.1f}".format(x)), file=f)

        # Write summary to .csv file
        if not truth_est_mode:
            csv_name = join(predict_location, fnb + 'summary.csv')
        else:
            csv_name = join(predict_location, fnb + 'summary_truest.csv')
        header_args = {
            'mode':     'a',
            'encoding': 'utf-8',
            'index':    False,
            'header':   False,
        }
        table_args = {
            'mode':     'a',
            'encoding': 'utf-8',
        }
        label = f'Speech enhancement metrics avg over all {len(all_mtab1_sorted_nom99)} non -99 SNR mixtures:'
        pd.DataFrame([label]).to_csv(csv_name, header=False, index=False)  # open as write
        all_nom99_mean.to_frame().T.round(2).to_csv(csv_name, index=False, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        pd.DataFrame([f'Speech enhancement metrics avg over each SNR:']).to_csv(csv_name, **header_args)
        mtab_snr_summary.round(2).to_csv(csv_name, index=False, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        pd.DataFrame([f'Extraction statistics stats avg over each SNR:']).to_csv(csv_name, **header_args)
        mtab_snr_summary_em.round(2).to_csv(csv_name, index=False, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        label = f'Speech enhancement metrics stats over {num_mix} mixtures:'
        pd.DataFrame([label]).to_csv(csv_name, **header_args)
        all_metrics_table_1.describe().round(2).to_csv(csv_name, **table_args)
        pd.DataFrame(['']).to_csv(csv_name, **header_args)
        label = f'Extraction statistics stats over {num_mix} mixtures:'
        pd.DataFrame([label]).to_csv(csv_name, **header_args)
        all_metrics_table_2.describe().round(2).to_csv(csv_name, **table_args)
        label = f'WER enabled with method {wer_method}, whisper model, if used: {whisper_model}'
        pd.DataFrame([label]).to_csv(csv_name, **header_args)

        if not truth_est_mode:
            csv_name = join(predict_location, fnb + 'list.csv')
        else:
            csv_name = join(predict_location, fnb + 'list_truest.csv')
        pd.DataFrame(['Speech enhancement metrics list:']).to_csv(csv_name, header=False, index=False)  # open as write
        all_metrics_table_1.round(2).to_csv(csv_name, **table_args)

        if not truth_est_mode:
            csv_name = join(predict_location, fnb + 'estats_list.csv')
        else:
            csv_name = join(predict_location, fnb + 'estats_list_truest.csv')
        pd.DataFrame(['Extraction statistics list:']).to_csv(csv_name, header=False, index=False)  # open as write
        all_metrics_table_2.round(2).to_csv(csv_name, **table_args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
