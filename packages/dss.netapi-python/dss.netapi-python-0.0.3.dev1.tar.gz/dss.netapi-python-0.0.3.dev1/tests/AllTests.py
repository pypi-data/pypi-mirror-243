import unittest

from GraphTestCase import GraphTestCase
from SimpleTestGraphTestCase import SimpleTestGraphTestCase
from MiniGraphTestCase import MiniGraphTestCase

# TestSuite um alle Testfälle laufen zu lassen
suite = unittest.TestSuite()

# Basistestfälle
suite.addTest(GraphTestCase())
suite.addTest(SimpleTestGraphTestCase())

# ...und ab jetzt mit mehr Semantik
suite.addTest(MiniGraphTestCase())