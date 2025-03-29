import numpy as np
import scipy.io.wavfile as wav


def interpolate_linearly(wavetable, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wavetable.shape[0]
    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight

    return truncated_index_weight * wavetable[truncated_index] + \
        next_index_weight * wavetable[next_index]


def fade_in_out(signal, fade_length=1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])

    return signal


def sawtooth(x):
    return (x + np.pi) / np.pi % 2 - 1


if __name__ == '__main__':
    sample_rate = 44100
    f = 220
    t = 3
    waveform = sawtooth
    wavetable_length = 64
    wavetable = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wavetable[n] = waveform(2 * np.pi * n / wavetable_length)

    output = np.zeros((t * sample_rate,))

    index = 0
    increment = f * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        output[n] = interpolate_linearly(wavetable, index)
        index += increment
        index %= wavetable_length

    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    output = fade_in_out(output)

    wav.write('saw220HzScaledInterpolatedFaded.wav',
              sample_rate,
              output.astype(np.float32))
