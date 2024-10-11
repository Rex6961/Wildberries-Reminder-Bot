import re

class EventNotice:
    """
    Класс для обработки и расчета времени и интервалов напоминаний.
    """

    def __init__(self, time_list) -> None:
        """
        Инициализация экземпляра класса EventNotice.

        :param time_list: Список строк, содержащих информацию о времени и интервалах.
        """
        self.time_list = time_list          # Список строк с временем и интервалами
        self.resultTime = 0                 # Итоговое время в секундах
        self.resultInterval = 0             # Итоговый интервал повторений

    def __call__(self):
        """
        Метод, который вызывается при вызове экземпляра класса как функции.
        Обрабатывает каждый элемент в time_list, преобразуя его в секунды или устанавливая интервал.
        """
        for time_str in self.time_list:
            unit = time_str[-1].lower()    # Получение последнего символа строки как единицы измерения и приведение к нижнему регистру

            try:
                value = int(time_str[:-1]) # Преобразование части строки без последнего символа в целое число
            except ValueError:
                # Выбрасывание исключения, если преобразование не удалось
                raise ValueError(f"Некорректное значение времени: {time_str}")

            # Проверка единицы измерения и расчет соответствующего количества секунд
            if unit == "m" and time_str[-1] == "m":  # 'm' для минут
                self.resultTime += value * 60
            elif unit == "m" and time_str[-1] == "M":  # 'M' для месяцев
                self.resultTime += value * 30 * 24 * 60 * 60  # Примерное количество секунд в месяце (30 дней)
            elif unit == "h":  # 'h' для часов
                self.resultTime += value * 60 * 60
            elif unit == "d":  # 'd' для дней
                self.resultTime += value * 24 * 60 * 60
            elif unit == "w":  # 'w' для недель
                self.resultTime += value * 7 * 24 * 60 * 60
            elif unit == "s":  # 's' для секунд
                self.resultTime += value
            elif unit == "i":  # 'i' для интервалов
                self.resultInterval = value
            else:
                # Выбрасывание исключения для неизвестных единиц измерения
                raise ValueError(f"Неизвестная единица измерения: {unit}")

def get_count(data):
    """
    Функция для извлечения времени и интервалов из входной строки.

    :param data: Строка, содержащая информацию о времени и интервалах.
    :return: Список найденных совпадений времени и интервалов.
    """
    # Компиляция регулярных выражений для поиска времени и интервалов
    pattern_time = re.compile(r"\d+[Mwdhms]+")  # Ищет числа, за которыми следуют единицы времени (M, w, d, h, m, s)
    pattern_interval = re.compile(r"\d+i")     # Ищет числа, за которыми следует 'i' для интервалов

    # Поиск всех совпадений времени и интервалов в строке
    time_matches = re.findall(pattern_time, data)
    interval_matches = re.findall(pattern_interval, data)

    # Объединение найденных совпадений в один список
    count = time_matches + interval_matches

    return count
