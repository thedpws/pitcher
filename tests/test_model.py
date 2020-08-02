
import unittest
from pitchr import harmony_maker
import importlib
import shutil
from pitchr import *

import os

class TestModel(unittest.TestCase):

    def setUp(self):
        os.environ['HOME'] = os.getcwd()


    def test_when_path_unset_uses_default(self):
        # Arrange
        del os.environ['PITCHR_PATH']


        # Act
        importlib.reload(harmony_maker)

        # Assert
        self.assertEqual(harmony_maker.PITCHR_PATH, os.environ['HOME'] + '/.pitchr')

    def test_when_path_set_uses_path(self):
        # Arrange
        os.environ['PITCHR_PATH'] = os.environ['HOME'] + '/.newpitchr'


        # Act
        importlib.reload(harmony_maker)


        # Assert
        self.assertEqual(harmony_maker.PITCHR_PATH, os.environ['HOME'] + '/.newpitchr')

    def test_when_model_does_not_exist_is_downloaded(self):

        # Arrange
        os.environ['PITCHR_PATH'] = os.environ['HOME'] + '/.newpitchr'

        if os.path.exists(os.environ['HOME'] + '/.newpitchr'):
            shutil.rmtree(os.environ['HOME'] + '/.newpitchr')

        importlib.reload(harmony_maker)

        # Preconditions Assertions
        self.assertFalse(os.path.exists(os.environ['HOME'] + '/.newpitchr/saved_model'))


        # Act
        h = harmony_maker.build_harmony(Staff([Measure([Note('C', 1.0)])]))

        path = os.environ['HOME'] + '/.newpitchr/saved_model/my_model/saved_model.pb'
        # Assert
        self.assertTrue(os.path.exists(path))
