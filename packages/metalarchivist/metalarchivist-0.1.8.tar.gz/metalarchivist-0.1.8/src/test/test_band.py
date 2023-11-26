
import os
import sys
import json
import unittest
import importlib.util
from types import ModuleType
from enum import Enum

from configparser import ConfigParser

import pandas as pd


class Submodule(Enum):
    MODULE = 'metalarchivist', './src/metalarchivist/__init__.py'
    EXPORT = 'metalarchivist.export', './src/metalarchivist/export/__init__.py'
    IFACE = 'metalarchivist.interface', './src/metalarchivist/interface/__init__.py'


def run_test_cases():
    unittest.main(argv=[''], verbosity=2)


def prepare_submodule(submodule: Submodule) -> ModuleType:
    submodule_name, submodule_path = submodule.value
    spec = importlib.util.spec_from_file_location(submodule_name, submodule_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[submodule_name] = module
    spec.loader.exec_module(module)

    return module

class TestBands(unittest.TestCase):
    def test_band_report(self):
        config = ConfigParser({'unittests': {'OUTPUTDIR': './'}})
        config.read('metallum.cfg')

        metalarchivist = prepare_submodule(Submodule.MODULE)
        self.assertIsNotNone(metalarchivist)

        interface = prepare_submodule(Submodule.IFACE)
        self.assertIsNotNone(interface)

        export = prepare_submodule(Submodule.EXPORT)
        self.assertIsNotNone(export)

        bands = metalarchivist.get_bands(['https://www.metal-archives.com/bands/Furia/23765',
                                          'https://www.metal-archives.com/bands/Cult_of_Fire/3540334368',
                                          'https://www.metal-archives.com/bands/Urfaust/19596',
                                          'https://www.metal-archives.com/bands/A_Forest_of_Stars/115504',
                                          'https://www.metal-archives.com/bands/Burzum/88',
                                          'https://www.metal-archives.com/bands/Mayhem/67',
                                          'https://www.metal-archives.com/bands/Satanic_Warmaster/989'])

        self.assertIsInstance(bands, list)
        
        output_path = os.path.join(config['unittests']['OUTPUTDIR'], 'test-bands.json')
        json.dump(bands, open(output_path, 'w'))

    def test_genres(self):
        interface = prepare_submodule(Submodule.IFACE)
        self.assertIsNotNone(interface)

        export = prepare_submodule(Submodule.EXPORT)
        self.assertIsNotNone(export)

        genres = interface.Genres('Drone/Doom Metal (early); Psychedelic/Post-Rock (later)')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 4)
        self.assertEqual(genres.clean_genre, 'Doom, Drone, Post-Rock, Psychedelic')

        genres = interface.Genres('Progressive Doom/Post-Metal')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 3)
        self.assertEqual(genres.clean_genre, 'Doom, Post-Metal, Progressive')

        genres = interface.Genres('Blackened Death Metal/Grindcore')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 3)
        self.assertEqual(genres.clean_genre, 'Blackened, Death, Grindcore')

        genres = interface.Genres('Black Metal')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 1)
        self.assertEqual(genres.clean_genre, 'Black')

        genres = interface.Genres('Progressive Death/Black Metal')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 3)
        self.assertEqual(genres.clean_genre, 'Black, Death, Progressive')

        genres = interface.Genres('Epic Black Metal')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 2)
        self.assertEqual(genres.clean_genre, 'Black, Epic')

        genres = interface.Genres('Various (early); Atmospheric Black Metal, Ambient (later)')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 4)
        self.assertEqual(genres.clean_genre, 'Various, Ambient, Atmospheric, Black')

        genres = interface.Genres('Symphonic Gothic Metal with Folk influences')
        self.assertIsNotNone(genres)
        self.assertEqual(len(genres.phases), 3)
        self.assertEqual(genres.clean_genre, 'Folk, Gothic, Symphonic')

    def test_band_profile(self):
        interface = prepare_submodule(Submodule.IFACE)
        self.assertIsNotNone(interface)

        export = prepare_submodule(Submodule.EXPORT)
        self.assertIsNotNone(export)

        self.assertIn('Band', dir(export))

        band = export.Band.get_profile('https://www.metal-archives.com/bands/Furia/23765')
        self.assertEqual(band.name, 'Furia')
        self.assertEqual(band.metallum_id, 23765)

        self.assertIsNotNone(band.themes)
        self.assertIsInstance(band.themes, interface.Themes)
        self.assertIsInstance(band.genres, interface.Genres)

    def test_band_profiles(self):
        interface = prepare_submodule(Submodule.IFACE)
        self.assertIsNotNone(interface)

        export = prepare_submodule(Submodule.EXPORT)
        self.assertIsNotNone(export)

        self.assertIn('Band', dir(export))

        bands = export.Band.get_profiles(['https://www.metal-archives.com/bands/Furia/23765',
                                          'https://www.metal-archives.com/bands/Cult_of_Fire/3540334368',
                                          'https://www.metal-archives.com/bands/Urfaust/19596',
                                          'https://www.metal-archives.com/bands/A_Forest_of_Stars/115504',
                                          'https://www.metal-archives.com/bands/Burzum/88',
                                          'https://www.metal-archives.com/bands/Mayhem/67',
                                          'https://www.metal-archives.com/bands/Satanic_Warmaster/989'])

        self.assertEqual(len(bands), 7)

    def test_band_themes(self):
        ...

if __name__ == '__main__':
    run_test_cases()
