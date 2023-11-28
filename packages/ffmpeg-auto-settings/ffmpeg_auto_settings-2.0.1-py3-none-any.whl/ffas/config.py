import collections
import copy
import sys
from pathlib import Path
import tomlkit
from .db import Video
from .misc import singleton
from .videostore import VideoStore


@singleton
class Config(collections.UserDict):
    default_config = {
        'presets': ['faster', 'fast', 'medium', 'slow'],
        'vmaf_delta': 0.5,
        'use_harmonic_mean': True,
        'encoder': 'libx265',
        'crf_limits': {
            'libx264': {
                'lower': 12.0,
                'upper': 35.0
            },
            'libx265': {
                'lower': 12.0,
                'upper': 35.0
            }
        }
    }
    _config_path = Path('.ffas/config.toml')

    def __init__(self):
        super().__init__()
        if self._config_path.is_file():
            self.read_config()
            if 'presets' not in self.data:
                self.data['presets'] = []
        else:
            self.data = copy.deepcopy(self.default_config)
            self.write_config()

    def read_config(self):
        self.data = tomlkit.loads(self._config_path.read_text())

    def write_config(self):
        self._config_path.write_text(tomlkit.dumps(self.data))


def get_configured_sample() -> Video:
    """
    Returns an Encode of the configured sample
    :return: Encode
    :raises LookupError: if no sample_variant is configured
    :raises NoResultFound: if the configured sample_variant is invalid
    """
    config = Config()
    try:
        sample_variant = config['sample_variant']
    except KeyError:
        # switch exception to something more meaningful
        raise LookupError('no sample variant configured')
    sample = VideoStore().get_video(type='sample', variant=sample_variant)  # may raise NoResultFound
    return sample


def ensure_configured_sample() -> None:
    try:
        _ = get_configured_sample()
    except LookupError:
        sys.exit('You need to create or configure a sample first!')
