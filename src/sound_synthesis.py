import numpy as np
import sounddevice as sd


def white_noise(duration: float = 1.0,
                amplitude: float = 0.5,
                sample_rate: int = 44100) -> np.ndarray:
    n_samples = int(duration * sample_rate)
    noise = np.random.uniform(-1, 1, n_samples)
    noise *= amplitude

    return noise


def sine_tone(frequency: int = 440,
              duration: float = 1.0,
              amplitude: float = 0.5,
              sample_rate: int = 44100) -> np.ndarray:
    n_samples = int(duration * sample_rate)
    time_points = np.linspace(0, duration, n_samples, False)
    sine = np.sin(2 * np.pi * frequency * time_points)
    sine *= amplitude

    return sine


if __name__ == '__main__':
    # my_sound = white_noise()
    # my_sound = sine_tone()

    # sine_1 = sine_tone(frequency=200, amplitude=0.6)
    # sine_2 = sine_tone(frequency=400, amplitude=0.3)
    # sine_3 = sine_tone(frequency=800, amplitude=0.2)
    # my_sound = sum([sine_1, sine_2, sine_3])

    # sines = [sine_tone(frequency=200 * i + 50, amplitude=0.7/i) for i in range(1, 31, 2)]
    # my_sound = sum(sines)

    sines = [sine_tone(frequency=200, duration=3.0, amplitude=0.6),
             sine_tone(frequency=205, duration=3.0, amplitude=0.6)]
    my_sound = sum(sines)

    sd.play(my_sound)
    sd.wait()
