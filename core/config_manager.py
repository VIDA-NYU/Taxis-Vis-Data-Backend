from decouple import config
import os
import json
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as django_settings

CONFIG_DIR = os.path.join(django_settings.BASE_DIR, 'config')

DEFAULT_CONFIG_TAXIS_DATASET = config('DEFAULT_CONFIG_TAXIS_DATASET', default='nyc_taxis_2015_dataset')


def load_config():
    config_path = os.path.join(CONFIG_DIR, f"{DEFAULT_CONFIG_TAXIS_DATASET}.json")
    if not os.path.exists(config_path):
        raise ImproperlyConfigured(
            f"Configuration file '{DEFAULT_CONFIG_TAXIS_DATASET}.json' not found in the config directory.")

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            raise ImproperlyConfigured(
                f"Configuration file '{DEFAULT_CONFIG_TAXIS_DATASET}.json' contains invalid JSON: {e}")

    required_keys = ['datetime_columns', 'location_columns', 'required_columns']
    for key in required_keys:
        if key not in config:
            raise ImproperlyConfigured(
                f"Configuration file '{DEFAULT_CONFIG_TAXIS_DATASET}.json' is missing required key: '{key}'")

    return config
