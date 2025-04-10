import STT
import TTS
import Gemeni
import torch

if __name__ == '__main__':

    # stt_module = STT.SpeechToTextModule("small") # Можно указать модель: SpeechToTextModule(model_name="small")
    # recognized_text = stt_module.process_voice()
    # if recognized_text:
    #     print("\n📝 Распознанный текст:")
    #     print(recognized_text)

    # tts_module = TTS.TextToSpeechModule()  # Использует API ключ из переменной окружения, голос "Adam", модель "eleven_monolingual_v1"
    # text_to_say =recognized_text
    # tts_module.text_to_speech_and_play(text_to_say)
    #
    # # Инициализация модуля Gemini (API ключ нужно получить и передать!)
    gemini_module = Gemeni.GeminiIntegrationModule()  # !!! Замени на свой реальный API ключ
    report_text = """
    # **Отчет о результатах исследования уровня шума в жилых районах города N**
    #
    # **Введение**
    #
    # Настоящий отчет подготовлен с целью оценки текущего уровня шумового загрязнения в жилых районах города N.  Повышенный уровень шума является значительным фактором, негативно влияющим на качество жизни населения, вызывая стресс, нарушения сна и другие проблемы со здоровьем.  Данное исследование направлено на выявление районов с наиболее высоким уровнем шума и предоставление рекомендаций для улучшения акустической обстановки.
    #
    # **Методология исследования**
    #
    # Исследование проводилось в период с 15 по 22 октября 2023 года.  Для сбора данных были выбраны 5 случайно отобранных жилых районов города N:  Центральный, Заречный, Прибрежный, Северный и Южный.  В каждом районе были выбраны по 3 точки измерения, представляющие собой типичные жилые зоны (дворы, детские площадки, улицы с умеренным движением).
    #
    # Измерения уровня шума проводились с использованием шумомера "Октава-110А-Эко" в соответствии с ГОСТ 51616-2000 "Шум. Общие требования безопасности".  Измерения проводились в дневное (с 10:00 до 12:00) и вечернее (с 19:00 до 21:00) время в будние дни.  Для каждой точки измерения было проведено 3 замера продолжительностью 5 минут каждый, после чего вычислялось среднее значение уровня звукового давления в дБА.
    #
    # **Результаты исследования**
    #
    # Средние значения уровня шума в различных районах города N представлены в таблице ниже:
    #
    # | Район        | Средний уровень шума (дБА) - Дневное время | Средний уровень шума (дБА) - Вечернее время |
    # |--------------|--------------------------------------------|---------------------------------------------|
    # | Центральный  | 65                                         | 68                                          |
    # | Заречный    | 58                                         | 62                                          |
    # | Прибрежный  | 55                                         | 58                                          |
    # | Северный    | 60                                         | 64                                          |
    # | Южный       | 52                                         | 55                                          |
    #
    # Анализ полученных данных показывает, что наиболее высокий уровень шума наблюдается в Центральном районе города как в дневное, так и в вечернее время.  Это может быть связано с высокой плотностью застройки, интенсивным транспортным потоком и наличием большого количества коммерческих объектов.  Наименьший уровень шума зафиксирован в Южном и Прибрежном районах, что может быть обусловлено удаленностью от основных транспортных магистралей и наличием зеленых зон.
    #
    # Во всех районах уровень шума в вечернее время несколько выше, чем в дневное, что вероятно связано с увеличением активности населения и транспортного движения в вечерние часы.
    #
    # **Выводы и рекомендации**
    #
    # Проведенное исследование выявило значительные различия в уровне шумового загрязнения между различными жилыми районами города N.  Центральный район характеризуется наиболее неблагоприятной акустической обстановкой, приближающейся к пороговым значениям, установленным санитарными нормами.
    #
    # Для улучшения акустической ситуации в городе N рекомендуется:
    #
    # 1. **В Центральном районе:**  Рассмотреть возможность внедрения шумозащитных мероприятий вдоль основных транспортных магистралей (установка шумозащитных экранов, использование малошумного асфальта).  Усилить контроль за соблюдением правил благоустройства, касающихся уровня шума от коммерческих объектов и строительных площадок.
    #
    # 2. **В Северном районе:**  Провести дополнительный анализ источников шума и разработать локальные меры по их снижению, например, ограничение скорости движения на отдельных участках дорог.
    #
    # 3. **Для всех районов:**  Увеличить площадь зеленых насаждений, которые способствуют снижению уровня шума.  Проводить информационно-просветительскую работу среди населения о негативном влиянии шума и способах его снижения.  Регулярно проводить мониторинг уровня шума для отслеживания динамики и эффективности принимаемых мер.
    #
    # **Дата:** 26 октября 2023 г.
    # **Подготовлено:** Аналитический отдел Городской Администрации г. N
    # """
    summarized_report = gemini_module.summarize_text(report_text)
    #
    if summarized_report:
        print("📝 Суммированный отчет от Gemini:\n", summarized_report)
        # Далее можно использовать TTS модуль для озвучивания summarized_report
        tts_module = TTS.TextToSpeechModule()  # Предполагаем, что TTS модуль уже инициализирован
        tts_module.text_to_speech_and_play(summarized_report)
    else:
        print("Не удалось получить summary от Gemini.")