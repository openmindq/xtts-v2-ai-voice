import pytest
from unittest.mock import patch, MagicMock
from tts_engine import TTSEngine
from pathlib import Path

@patch('TTS.api.TTS')
def test_tts_engine_init(mock_tts):
    engine = TTSEngine()
    assert engine.device in ['cuda', 'cpu']
    mock_tts.assert_called_once()

@patch.object(TTSEngine, 'tts')
def test_synthesize_basic(mock_tts, tmp_path):
    engine = TTSEngine()
    output = engine.synthesize('Test', output_path=tmp_path / 'test.wav')
    assert output.exists()
