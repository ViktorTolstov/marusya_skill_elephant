import pytest
import json
from skill_buy_elephant.skill import skill
from pathlib import Path


base_req_file_name = Path(__file__).parent / 'base_request.json'


@pytest.mark.parametrize('phrase_text, new_session, answer_text', [
    ('где купить слона', True, 'Привет! Купи слона!'),
    ('не понял', False, 'Все говорят'),
    ('куплю', False, 'Слона можно найти на Яндекс.Маркете!'),
])
def test_skill(phrase_text, new_session, answer_text):
    req = {}
    resp = {}
    with open(base_req_file_name) as f:
        req = json.load(f)

    req['request']['original_utterance'] = phrase_text
    req['session']['new'] = new_session

    skill.handle_dialog(req, resp)

    assert answer_text in resp['response']['text']