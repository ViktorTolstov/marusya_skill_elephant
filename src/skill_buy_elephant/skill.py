from typing import Dict, List


class Skill:
    def __init__(self) -> None:
        self._sessionStorage: Dict = dict()  # Хранилище данных о сессиях.

    # Функция для непосредственной обработки диалога.
    def handle_dialog(self, req, res) -> None:
        res['version'] = req['version']
        res['session'] = req['session']
        res['response'] = {
            'end_session': False
        }

        user_id = req['session']['user_id']

        if req['session']['new']:
            # Это новый пользователь.
            # Инициализируем сессию и поприветствуем его.

            self._sessionStorage[user_id] = {
                'suggests': [
                    "Не хочу.",
                    "Не буду.",
                    "Отстань!",
                ]
            }

            res['response']['text'] = 'Привет! Купи слона!'
            res['response']['tts'] = \
                '<speaker audio="alarmclock/Будильник отключён"> ' \
                'У вас получилось!'
            res['response']['buttons'] = self.get_suggests(user_id)
            return

        # Обрабатываем ответ пользователя.
        if req['request']['original_utterance'].lower() in [
            'ладно',
            'куплю',
            'покупаю',
            'хорошо',
        ]:
            # Пользователь согласился, прощаемся.
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
            return

        # Если нет, то убеждаем его купить слона!
        res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
            req['request']['original_utterance']
        )
        res['response']['tts'] = \
            '<speaker audio="alarmclock/Будильник отключён"> У вас получилось!'
        res['response']['buttons'] = self.get_suggests(user_id)

    # Функция возвращает две подсказки для ответа.
    def get_suggests(self, user_id: str) -> List:
        session = self._sessionStorage.get(user_id) or {'suggests': []}

        # Выбираем две первые подсказки из массива.
        suggests: List = [
            {'title': suggest, 'hide': True}
            for suggest in session['suggests'][:2]
        ]

        # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
        session['suggests'] = session['suggests'][1:]
        self._sessionStorage[user_id] = session

        # Если осталась только одна подсказка, предлагаем подсказку
        # со ссылкой на Яндекс.Маркет.
        if len(suggests) < 2:
            suggests.append({
                "title": "Ладно",
                "url": "https://market.yandex.ru/search?text=слон",
                "hide": True
            })

        return suggests


skill: Skill = Skill()
