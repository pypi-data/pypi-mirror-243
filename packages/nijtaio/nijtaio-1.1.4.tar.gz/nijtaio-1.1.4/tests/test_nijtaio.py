"""Unit tests for nijtaio."""
import json
import os
import nijtaio
import datasets


def test_serializer():
    """TODO: document this."""
    batch = [os.path.join(os.path.dirname(__file__), "data", 'e0003.wav')]
    audio_dataset = datasets.load_dataset('audiofolder',
                                          data_files=batch)
    s = nijtaio._nijta_serializer(audio_dataset)
    assert isinstance(s, dict)
    s2 = json.dumps(audio_dataset.cast_column("audio",
                                              datasets.Audio(decode=True)),
                    default=nijtaio._nijta_serializer)
    assert isinstance(s2, str)
