import numpy as np
import sounddevice as sd


def amplitude_modulation(carrier_frequency: float,
                         modulator_wave: np.ndarray,
                         modulation_index: float = 0.5,
                         amplitude: float = 0.5,
                         sample_rate: int = 44100) -> np.ndarray:
    total_samples = len(modulator_wave)
    time_points = np.arange(total_samples) / sample_rate
    carrier_wave = np.sin(2 * np.pi * carrier_frequency * time_points)
    am_wave = (1 + modulation_index * modulator_wave) * carrier_wave
    max_amplitude = np.max(np.abs(am_wave))
    am_wave = amplitude * (am_wave / max_amplitude)

    return am_wave


def apply_envelope(sound: np.ndarray,
                   adsr: dict,
                   sample_rate: int = 44100) -> np.ndarray:
    sound = sound.copy()
    a_s = int(adsr['attack'] * sample_rate)
    d_s = int(adsr['decay'] * sample_rate)
    r_s = int(adsr['release'] * sample_rate)
    s_s = len(sound) - (a_s + d_s + r_s)

    sound[:a_s] *= np.linspace(0, 1, a_s)
    sound[a_s:a_s + d_s] *= np.linspace(1, adsr['sustain'], d_s)
    sound[a_s + d_s:a_s + d_s + s_s] *= adsr['sustain']
    sound[a_s + d_s + s_s:] *= np.linspace(adsr['sustain'], 0, r_s)

    return sound


def white_noise(duration: float = 1.0,
                amplitude: float = 0.5,
                sample_rate: int = 44100) -> np.ndarray:
    n_s = int(duration * sample_rate)
    noise = np.random.uniform(-1, 1, n_s)
    noise *= amplitude

    return noise


def sine_tone(frequency: int = 440,
              duration: float = 1.0,
              amplitude: float = 0.5,
              sample_rate: int = 44100) -> np.ndarray:
    n_s = int(duration * sample_rate)
    time_points = np.linspace(0, duration, n_s, False)
    sine = np.sin(2 * np.pi * frequency * time_points)
    sine *= amplitude

    return sine


if __name__ == '__main__':
    # my_sound = white_noise()
    # my_sound = sine_tone(duration=3.0)

    # sine_1 = sine_tone(frequency=200, amplitude=0.6)
    # sine_2 = sine_tone(frequency=400, amplitude=0.3)
    # sine_3 = sine_tone(frequency=800, amplitude=0.2)
    # my_sound = sum([sine_1, sine_2, sine_3])

    # sines = [sine_tone(frequency=200 * i + 50, duration=3.0, amplitude=0.7/i) for i in range(1, 31, 2)]
    # my_sound = sum(sines)

    # sines = [sine_tone(frequency=200, duration=3.0, amplitude=0.6),
    #          sine_tone(frequency=205, duration=3.0, amplitude=0.6)]
    # my_sound = sum(sines)

    # adsr = {
    #     'attack': 0.5,
    #     'decay': 0.2,
    #     'sustain': 0.6,
    #     'release': 0.5,
    # }

    # my_sound = apply_envelope(my_sound, adsr)

    my_modulator = sine_tone(frequency=217, duration=3.0)

    my_sound = amplitude_modulation(220, my_modulator)
    my_sound = amplitude_modulation(30, my_sound)
    my_sound = amplitude_modulation(60, my_sound)

    sd.play(my_sound)
    sd.wait()
