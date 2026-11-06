"""Regresiones del contrato Maven de la distribución Legacy."""
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET


SPEC = importlib.util.spec_from_file_location(
    'legacy_maven', Path(__file__).resolve().parents[2] / 'scripts/prepare_maven_release.py')
maven = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(maven)


class LegacyMaven(unittest.TestCase):
    def test_pom_keeps_legacy_coordinate_and_capture_dependencies(self):
        pom = ET.fromstring(maven.make_pom('3.5.1-rc.1', 'Términos de prueba', 'https://example.test/license'))
        ns = {'m': maven.POM_NS}
        self.assertEqual(pom.findtext('m:groupId', namespaces=ns), 'ai.becomedigital')
        self.assertEqual(pom.findtext('m:artifactId', namespaces=ns), 'identity-verification-legacy')
        self.assertEqual(pom.findtext('m:version', namespaces=ns), '3.5.1-rc.1')
        deps = {d.findtext('m:artifactId', namespaces=ns): d.findtext('m:version', namespaces=ns)
                for d in pom.findall('m:dependencies/m:dependency', ns)}
        self.assertEqual(deps['capture-core'], '1.4.1')
        self.assertEqual(deps['capture-ux'], '1.4.1')
        self.assertFalse(any('blinkid' in name.lower() for name in deps))
        self.assertEqual(deps['ui'], '1.11.3')
        self.assertEqual(deps['runtime'], '1.11.3')

    def test_rc_check_validates_the_binary_base_version(self):
        with patch.object(sys, 'argv', ['prepare_maven_release.py', '--version', '3.5.1-rc.1', '--check']), \
             patch.object(maven, 'validate_artifacts') as validate:
            maven.main()
        validate.assert_called_once_with('3.5.1')
