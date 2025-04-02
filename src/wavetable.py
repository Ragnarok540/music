import numpy as np
import scipy.io.wavfile as wav


def create_wavetable(waveform: str = 'sine',
                     length: int = 64) -> np.ndarray:
    wavetable = np.zeros((length,))

    match waveform:
        case 'sine' | 'sin':
            wave = np.sin
        case 'sawtooth' | 'saw':
            def wave(x):
                (x + np.pi) / np.pi % 2 - 1
        case 'square':
            def wave(x):
                np.sign(np.sin(x)) * 0.5
        case 'triangle':
            def wave(x):
                np.arcsin(np.sin(x)) * 0.5
        case _:
            raise Exception(f'waveform "{waveform}" not implemented')

    for n in range(length):
        wavetable[n] = wave(2 * np.pi * n / length)

    return wavetable


def scale_signal(signal: np.ndarray,
                 gain: int = -20) -> np.ndarray:
    output = signal.copy()
    amplitude = 10 ** (gain / 20)
    output *= amplitude

    return output


def wavetable_synthesis(wavetable: np.ndarray,
                        sample_rate: int = 44100,
                        frequency: int = 440,
                        duration: float = 3) -> np.ndarray:
    output = np.zeros((duration * sample_rate,))
    index = 0
    increment = frequency * wavetable.shape[0] / sample_rate

    for n in range(output.shape[0]):
        output[n] = wavetable[int(np.floor(index))]
        index += increment
        index %= wavetable.shape[0]

    return output


if __name__ == '__main__':
    sample_rate = 44100
    waveform = 'sin'
    wavetable_length = 64

    wavetable = create_wavetable(waveform, wavetable_length)
    output = wavetable_synthesis(wavetable, sample_rate)

    wav.write('sine440Hz.wav', sample_rate, output.astype(np.float32))

    scaled_output = scale_signal(output)

    wav.write('sine440HzScaled.wav',
              sample_rate,
              scaled_output.astype(np.float32))
