import elevenlabs
import configparser
import sounddevice as sd  # Импортируем sounddevice
import soundfile as sf    # Импортируем soundfile


class TextToSpeechModule:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            self.client = elevenlabs.ElevenLabs(api_key=config.get('elevenlabs', 'api_key'))
            self.voice_id = config.get('elevenlabs', 'voice_id')
            self.model_id = config.get('elevenlabs', 'model_id')
            self.output_format = config.get('elevenlabs', 'output_format')

        except (configparser.NoSectionError, configparser.NoOptionError):
            print("⚠️ Секция или параметры не найдены в config.ini")
            return
        except FileNotFoundError:
            print("⚠️ Файл config.ini не найден. Пожалуйста, создайте его.")
            return

    def text_to_speech_and_save(self, text, filename="audio.mp3"): # Изменим расширение по умолчанию на .wav для лучшей совместимости с sounddevice/soundfile
        """
        Преобразует текст в речь с помощью ElevenLabs и сохраняет аудио в файл.

        Args:
            text (str): Текст для озвучивания.
            filename (str, optional): Имя файла для сохранения аудио. Defaults to "audio.wav".
        """
        try:
            audio = self.client.text_to_speech.convert(text=text, voice_id=self.voice_id,
                                                        model_id=self.model_id,
                                                        output_format=self.output_format)
            elevenlabs.save(audio, filename)
            print(f"🔈 Аудио сохранено в файл: {filename}")

        except Exception as e:
            print(f"❌ Ошибка при генерации и сохранении речи: {e}")

    def play_audio_file(self, filename="audio.mp3"): # Изменим расширение по умолчанию на .wav
        """
        Воспроизводит аудиофайл, используя библиотеки sounddevice и soundfile.

        Args:
            filename (str, optional): Имя аудиофайла для воспроизведения. Defaults to "audio.wav".
        """
        try:
            data, fs = sf.read(filename) # Читаем аудиофайл с помощью soundfile
            sd.play(data, fs, blocking=True) # Воспроизводим аудиоданные с помощью sounddevice, blocking=True для ожидания окончания воспроизведения
            sd.wait() # Убедимся, что воспроизведение завершено (лишнее, так как blocking=True уже ждет, но для ясности оставим)
            print(f"▶️  Воспроизведение аудио из файла (sounddevice/soundfile): {filename}")

        except FileNotFoundError:
            print(f"❌ Аудиофайл не найден: {filename}")
        except sf.LibsndfileError as e:
            print(f"❌ Ошибка при чтении аудиофайла (soundfile): {e}")
        except sd.PortAudioError as e:
            print(f"❌ Ошибка при воспроизведении аудио (sounddevice): {e}")
        except Exception as e:
            print(f"❌ Общая ошибка при воспроизведении аудиофайла (sounddevice/soundfile): {e}")

    def text_to_speech_and_play(self, text):
        """
        Преобразует текст в речь с помощью ElevenLabs, сохраняет аудио и воспроизводит его.

        Args:
            text (str): Текст для озвучивания.
        """
        filename = "audio.mp3"  # Имя файла по умолчанию, изменим на .wav
        self.text_to_speech_and_save(text, filename) # Сначала сохраняем аудио
        self.play_audio_file(filename) # Затем воспроизводим сохраненный файл







