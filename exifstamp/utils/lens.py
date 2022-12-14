import csv
import os

lens_bindings = {}


def get_binding_of(lens: str, options: dict) -> str | None:
    """Returns a lens models from a csv of lens bindings"""
    global lens_bindings

    if len(lens_bindings) == 0:
        with open(os.path.join(os.path.dirname(__file__), '..', 'themes', options['theme'], 'lens_bindings.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lens_bindings[row['lens_binding']] = row['lens_real']

    return lens_bindings.get(lens, lens)
