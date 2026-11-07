"""Evita validar un APK con módulos Compose desalineados respecto a la compilación de la SDK."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile


SPEC = importlib.util.spec_from_file_location('android_dependency_versions',
    Path(__file__).resolve().parents[1] / 'scripts/verify_android_dependencies.py')
versions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(versions)


class ComposeAlignment(unittest.TestCase):
    def inspect(self, entries):
        with tempfile.TemporaryDirectory() as temporary:
            apk = Path(temporary) / 'consumer.apk'
            with zipfile.ZipFile(apk, 'w') as archive:
                for name, value in entries.items():
                    archive.writestr(name, value)
            return versions.inspect(apk, {'androidx.compose.foundation:foundation': '1.11.3',
                                          'androidx.compose.material3:material3': '1.4.0'})

    def test_rejects_the_observed_older_foundation_runtime(self):
        result = self.inspect({'META-INF/androidx.compose.foundation_foundation.version': '1.10.0'})
        self.assertFalse(result['passed'])
        self.assertIn('1.10.0', result['errors'][0])

    def test_accepts_each_module_at_its_own_bom_version(self):
        result = self.inspect({'META-INF/androidx.compose.foundation_foundation.version': '1.11.3',
                               'META-INF/androidx.compose.material3_material3.version': '1.4.0'})
        self.assertTrue(result['passed'])

    def test_missing_version_evidence_is_not_treated_as_success(self):
        self.assertFalse(self.inspect({})['passed'])
