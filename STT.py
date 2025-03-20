import sounddevice as sd
import soundfile as sf
import whisper
import noisereduce as nr # Импортируем noisereduce
import torch

class SpeechToTextModule:
    def __init__(self, model_name="small", samplerate=16000, channels=2):
        """
        Инициализирует модуль распознавания речи.

        Args:
            model_name (str): Название модели Whisper для использования (например, "tiny", "base", "small", "medium", "large").
            samplerate (int): Частота дискретизации аудио (по умолчанию 16000 Гц).
            channels (int): Количество каналов записи (по умолчанию 1, моно).
        """
        self.model_name = model_name
        self.samplerate = samplerate
        self.channels = channels
        self.model = None # Модель загрузится при первом использовании

    def _load_model(self):
        """Загружает модель Whisper, если она еще не загружена."""
        if self.model is None:
            print(f"⚙️ Загружаю модель Whisper: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
            print("✅ Модель Whisper загружена.")

    def record_audio(self, duration=5):
        """
        Записывает аудио с микрофона.

        Args:
            duration (int): Длительность записи в секундах (по умолчанию 5 секунд).

        Returns:
            numpy.ndarray: Записанное аудио в виде numpy массива.
        """
        print("🎙️ Начинаю запись голоса...")
        recording = sd.rec(int(self.samplerate * duration), samplerate=self.samplerate, channels=self.channels)
        sd.wait()  # Ожидание завершения записи
        print("⏹️ Запись завершена.")
        return recording

    def transcribe_audio(self,  filename='last_input.mp3', audio_data="",):
        """
        Распознает речь из аудиоданных с шумоподавлением с помощью Whisper.

        Args:
            audio_data (numpy.ndarray): Аудио данные для распознавания.
            filename (str): Имя файла для временного сохранения аудио (по умолчанию "recording.wav").

        Returns:
            str: Распознанный текст или None в случае ошибки.
        """
        try:
            # 1. Шумоподавление
            #reduced_noise = nr.reduce_noise(y=audio_data, sr=self.samplerate, prop_decrease=0.95)
            #sf.write(filename, reduced_noise, self.samplerate)  # Сохраняем аудио после шумоподавления

            self._load_model()
            print("🧠 Запускаю распознавание речи с помощью Whisper...")
            result = self.model.transcribe(filename)
            transcription_text = result["text"]
            print("✅ Распознавание завершено.")
            torch.cuda.empty_cache()
            return transcription_text

        except Exception as e:
            print(f"❌ Произошла ошибка при распознавании: {e}")
            return None

    def process_voice(self, duration=5):
        """
        Записывает голос и распознает его.

        Args:
            duration (int): Длительность записи в секундах (по умолчанию 5 секунд).

        Returns:
            str: Распознанный текст или None в случае ошибки.
        """
        audio = self.record_audio(duration)
        self.save_audio_recording(audio)
        if audio is not None:
            return self.transcribe_audio("last_input.mp3")
        return None

    def play_recorded_audio(self, audio_data):
        """
        Воспроизводит аудио данные, полученные как sounddevice массив.

        Args:
            audio_data (numpy.ndarray): Аудио данные для воспроизведения (sounddevice массив).
        """
        try:
            sd.play(audio_data, self.samplerate, blocking=True)
            sd.wait()  # Убеждаемся, что воспроизведение завершено
            print("▶️  Воспроизведение записи завершено.")
        except sd.PortAudioError as e:
            print(f"❌ Ошибка при воспроизведении аудио (sounddevice): {e}")
        except Exception as e:
            print(f"❌ Общая ошибка при воспроизведении аудио: {e}")

    def save_audio_recording(self, audio_data, filename="last_input.mp3"):
        """
        Сохраняет аудио данные в WAV файл.

        Args:
            audio_data (numpy.ndarray): Аудио данные для сохранения.
            filename (str): Имя файла для сохранения аудио (по умолчанию "recording_saved.wav").
        """
        try:
            sf.write(filename, audio_data, self.samplerate, format='mp3')
            print(f"💾 Аудио запись сохранена в файл: {filename}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении аудио: {e}")