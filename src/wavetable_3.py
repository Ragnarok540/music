import numpy as np
import scipy.io.wavfile as wav


def interpolate_linearly(wavetable, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wavetable.shape[0]
    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight

    return truncated_index_weight * wavetable[truncated_index] + \
        next_index_weight * wavetable[next_index]


if __name__ == '__main__':
    sample_rate = 44100
    f = 440
    t = 3
    waveform = np.sin
    wavetable_length = 64
    wavetable = np.zeros((wavetable_length,))

    for n in range(wavetable_length):
        wavetable[n] = waveform(2 * np.pi * n / wavetable_length)

    output = np.zeros((t * sample_rate,))

    index = 0
    increment = f * wavetable_length / sample_rate

    for n in range(output.shape[0]):
        # output[n] = wavetable[int(np.floor(index))]
        output[n] = interpolate_linearly(wavetable, index)
        index += increment
        index %= wavetable_length

    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    wav.write('sine440HzScaledInterpolated.wav',
              sample_rate,
              output.astype(np.float32))
