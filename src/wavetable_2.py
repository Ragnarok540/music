import numpy as np
import scipy.io.wavfile as wav


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
        output[n] = wavetable[int(np.floor(index))]
        index += increment
        index %= wavetable_length

    gain = -20
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    wav.write('sine440HzScaled.wav', sample_rate, output.astype(np.float32))
