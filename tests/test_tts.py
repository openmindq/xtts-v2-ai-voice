import pytest
import torch
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.xtts_voice.tts_engine import TTSEngine
from src.xtts_voice.exceptions import ModelLoadError, SpeakerFileError, SynthesisError
from src.xtts_voice.settings import get_settings

@pytest.fixture
def mock_tts():
    mock = MagicMock()
    mock.tts_to_file.return_value = None
    return mock

@pytest.fixture
def temp_output(tmp_path):
    return tmp_path / "test.wav"

def test_engine_init_gpu(mock_tts):
    with patch('torch.cuda.is_available', return_value=True):
        engine = TTSEngine()
        assert engine.device == 'cuda'
        mock_tts.assert_called_once_with(get_settings().model_name, gpu=True)

def test_engine_init_cpu(mock_tts):
    with patch('torch.cuda.is_available', return_value=False):
        engine = TTSEngine()
        assert engine.device == 'cpu'
        mock_tts.assert_called_once_with(get_settings().model_name, gpu=False)

def test_synthesize_basic(mock_tts, temp_output):
    engine = TTSEngine()
    output = engine.synthesize("Test metin", output_path=temp_output)
    assert output == temp_output
    mock_tts.tts_to_file.assert_called_once()

def test_synthesize_speaker(mock_tts, tmp_path):
    speaker = tmp_path / "speaker.wav"
    speaker.touch()
    engine = TTSEngine()
    output = engine.synthesize("Test", speaker_wav=speaker)
    assert 'speaker_wav' in mock_tts.tts_to_file.call_args.kwargs

def test_speaker_not_exists(mock_tts):
    engine = TTSEngine()
    with pytest.raises(SpeakerFileError):
        engine.synthesize("Test", speaker_wav=Path("nonexistent.wav"))

def test_model_load_error():
    with patch('TTS.api.TTS') as mock_tts:
        mock_tts.side_effect = Exception("Load failed")
        with pytest.raises(ModelLoadError):
            TTSEngine()
