import numpy as np
import scipy.io.wavfile as wav


def saw(x):
    return (x + np.pi) / np.pi % 2 - 1


def square(x):
    return np.sign(np.sin(x)) * 0.5


def triangle(x):
    return np.arcsin(np.sin(x)) * 0.5


def create_wavetable(waveform: str = 'sine',
                     length: int = 64) -> np.ndarray:
    wavetable = np.zeros((length,))

    match waveform:
        case 'sine' | 'sin':
            wave = np.sin
        case 'sawtooth' | 'saw':
            wave = saw
        case 'square':
            wave = square
        case 'triangle':
            wave = triangle
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


def interpolate_linearly(wavetable, index):
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wavetable.shape[0]
    next_index_weight = index - truncated_index
    truncated_index_weight = 1 - next_index_weight

    return truncated_index_weight * wavetable[truncated_index] + \
        next_index_weight * wavetable[next_index]


def wavetable_synthesis(wavetable: np.ndarray,
                        sample_rate: int = 44100,
                        frequency: int = 440,
                        duration: float = 3,
                        interpolate: bool = False) -> np.ndarray:
    output = np.zeros((duration * sample_rate,))
    index = 0
    increment = frequency * wavetable.shape[0] / sample_rate

    for n in range(output.shape[0]):
        if interpolate:
            output[n] = interpolate_linearly(wavetable, index)
        else:
            output[n] = wavetable[int(np.floor(index))]
        index += increment
        index %= wavetable.shape[0]

    return output


def fade_in_out(signal, fade_length=1000):
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    fade_out = np.flip(fade_in)

    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])

    return signal


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

    interpolated_output = wavetable_synthesis(wavetable,
                                              sample_rate,
                                              interpolate=True)

    interpolated_scaled_output = scale_signal(interpolated_output)

    wav.write('sine440HzScaledInterpolated.wav',
              sample_rate,
              interpolated_scaled_output.astype(np.float32))

    faded_interpolated_scaled_output = fade_in_out(interpolated_scaled_output)

    wav.write('sine440HzScaledInterpolatedFaded.wav',
              sample_rate,
              faded_interpolated_scaled_output.astype(np.float32))

    for waveform in ['sawtooth', 'square', 'triangle']:
        wavetable = create_wavetable(waveform,
                                     wavetable_length)
        output = wavetable_synthesis(wavetable,
                                     sample_rate,
                                     frequency=220,
                                     interpolate=True)
        output = scale_signal(output)
        output = fade_in_out(output)

        wav.write(f'{waveform}220HzScaledInterpolatedFaded.wav',
                  sample_rate,
                  output.astype(np.float32))
