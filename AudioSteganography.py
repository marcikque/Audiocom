# Credit for this code goes to Guang Yang
# Developed and published on GitHub: GY19A/improved_audio_phase_encoding
#
# BSD 2-Clause License
#
# Copyright (c) 2024, TY19X
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import warnings

def embed_message(input_filename, output_filename, message):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        rate, audio = wavfile.read(input_filename)
    if len(audio.shape) > 1:
        audio = audio[:, 0]  # Convert to mono by selecting the first channel
    audio = audio.copy()

    # Calculate message length in bits
    msg_len = 8 * len(message)
    # Calculate segment length, ensuring it's a power of 2
    seg_len = int(2 * 2**np.ceil(np.log2(2*msg_len)))
    # Calculate the number of segments needed
    seg_num = int(np.ceil(len(audio) / seg_len))

    # Resize the audio array to fit the number of segments
    audio.resize(seg_num * seg_len, refcheck=False)

    # Convert message to binary representation
    msg_bin = np.ravel([[int(y) for y in format(ord(x), '08b')] for x in message])
    # Convert binary to phase shifts (-pi/8 for 1, pi/8 for 0)
    msg_pi = msg_bin.copy()
    msg_pi[msg_pi == 0] = -1
    msg_pi = msg_pi * -np.pi / 2  # Use smaller phase to improve audio quality 1/8 may cause low BER, so change back to 1/2

    # Reshape audio into segments and perform FFT
    segs = audio.reshape((seg_num, seg_len))
    segs = np.fft.fft(segs)
    M = np.abs(segs)  # Magnitude
    P = np.angle(segs)  # Phase

    seg_mid = seg_len // 2

    # Embed message into the phase of the middle frequencies
    for i in range(seg_num):
        start = i * len(msg_pi) // seg_num
        end = (i + 1) * len(msg_pi) // seg_num
        P[i, seg_mid - (end - start):seg_mid] = msg_pi[start:end]
        P[i, seg_mid + 1:seg_mid + 1 + (end - start)] = -msg_pi[start:end][::-1]

    # Reconstruct the audio with modified phase
    segs = M * np.exp(1j * P)
    audio = np.fft.ifft(segs).real.ravel().astype(np.int16)

    # Write the modified audio to the output file
    wavfile.write(output_filename, rate, audio)


def extract_message(input_filename, msg_len):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        rate, audio = wavfile.read(input_filename)
    seg_len = int(2 * 2**np.ceil(np.log2(2*msg_len)))
    seg_num = int(np.ceil(len(audio) / seg_len))
    seg_mid = seg_len // 2

    extracted_bits = []

    for i in range(seg_num):
        x = np.fft.fft(audio[i * seg_len:(i + 1) * seg_len])
        extracted_phase = np.angle(x)
        start = i * msg_len // seg_num
        end = (i + 1) * msg_len // seg_num
        extracted_bits.extend((extracted_phase[seg_mid - (end - start):seg_mid] < 0).astype(np.int8))

    extracted_bits = np.array(extracted_bits[:msg_len])
    chars = extracted_bits.reshape((-1, 8)).dot(1 << np.arange(8 - 1, -1, -1)).astype(np.uint8)
    message = ''.join(chr(c) for c in chars)
    return message

def calculate_accuracy(original_msg, extracted_msg):
    original_bits = ''.join(f'{ord(c):08b}' for c in original_msg)
    extracted_bits = ''.join(f'{ord(c):08b}' for c in extracted_msg)

    total_bits = len(original_bits)
    incorrect_bits = sum(o != e for o, e in zip(original_bits, extracted_bits))
    bit_error_rate = incorrect_bits / total_bits

    message_accuracy = 1 if original_msg == extracted_msg else 0

    return bit_error_rate, message_accuracy

def calculate_max_message_length(input_filename):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        rate, audio = wavfile.read(input_filename)
    if len(audio.shape) > 1:
        audio = audio[:, 0]
    audio_len = len(audio)

    seg_len = int(2 * 2**np.ceil(np.log2(2*audio_len)))
    seg_num = int(np.ceil(audio_len / seg_len))

    max_bits_per_seg = (seg_len // 2 - 1) // 2
    max_bits = seg_num * max_bits_per_seg
    max_bytes = max_bits // 8

    return max_bytes

def find_non_zero_segment(audio, seg_len=1024):
    for i in range(0, len(audio), seg_len):
        segment = audio[i:i+seg_len]
        if np.max(segment) > 0:
            return segment
    return audio[:seg_len]

def plot_spectrum_and_phase(original_audio, modified_audio, rate, message):
    msg_len = 8 * len(message)
    seg_len = int(2 * 2**np.ceil(np.log2(2*msg_len)))

    original_segment = find_non_zero_segment(original_audio, seg_len)
    modified_segment = find_non_zero_segment(modified_audio, seg_len)

    original_segment = original_segment / np.max(np.abs(original_segment))
    modified_segment = modified_segment / np.max(np.abs(modified_segment))

    original_segs = np.fft.fft(original_segment)
    modified_segs = np.fft.fft(modified_segment)

    original_M = np.abs(original_segs)
    original_P = np.angle(original_segs)

    modified_M = np.abs(modified_segs)
    modified_P = np.angle(modified_segs)

    freqs = np.fft.fftfreq(seg_len, 1/rate)

    plt.figure(figsize=(12, 18))

    plt.subplot(3, 1, 1)
    plt.plot(original_segment, label='Original', color='blue')
    plt.plot(modified_segment, label='Modified', color='red')
    plt.title('Time-Domain Comparison')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(freqs[:seg_len // 2], original_M[:seg_len // 2], label='Original', color='blue')
    plt.plot(freqs[:seg_len // 2], modified_M[:seg_len // 2], label='Modified', color='red')
    plt.title('Spectrum Comparison')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(freqs[:seg_len // 2], original_P[:seg_len // 2], label='Original', color='blue')
    plt.plot(freqs[:seg_len // 2], modified_P[:seg_len // 2], label='Modified', color='red')
    plt.title('Phase Comparison')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (radians)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_audio_spectrums(original_file, modified_file, message):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        rate, original_audio = wavfile.read(original_file)
    if len(original_audio.shape) > 1:
        original_audio = original_audio[:, 0]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        rate, modified_audio = wavfile.read(modified_file)
    if len(modified_audio.shape) > 1:
        modified_audio = modified_audio[:, 0]

    plot_spectrum_and_phase(original_audio, modified_audio, rate, message)




##### Example Usage
# input_filename = 'example.wav'
# output_filename = 'improve_phase_coding.wav'
# message = "testtest"
#
# max_length = calculate_max_message_length(input_filename)
# print(f"Maximum message length in bytes: {max_length}")
#
# embed_message(input_filename, output_filename, message)
# extracted_message = extract_message(output_filename, 8 * len(message))
# print(f'Extracted Message: {extracted_message}')
#
# ber, accuracy = calculate_accuracy(message, extracted_message)
# print(f'Bit Error Rate (BER): {ber:.2%}')
# print(f'Message Accuracy: {"Correct" if accuracy else "Incorrect"}')
#
# from IPython.display import Audio, display
# display(Audio(filename=input_filename, autoplay=False))
# display(Audio(filename=output_filename, autoplay=False))
#
# plot_audio_spectrums(input_filename, output_filename, message)