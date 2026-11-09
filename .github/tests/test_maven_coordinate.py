"""Protege el nombre publicado y la reutilización del binario de la RC aprobada."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


c = load('coordinate_contract', ROOT / '.github/scripts/maven_coordinate.py')
m = load('coordinate_pom', ROOT / 'scripts/prepare_maven_release.py')


class MavenCoordinate(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / '.github/maven-coordinate.json').read_text())
        self.license = (ROOT / self.record['license_file']).read_bytes()
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        sdk = Path(temporary.name) / 'sdk.aar'
        sdk.write_bytes(b'RC revisada para la prueba del contrato')
        self.module = SimpleNamespace(GROUP=m.GROUP, ARTIFACT=m.ARTIFACT, SDK=sdk,
                                      DEPENDENCIES=m.DEPENDENCIES, make_pom=m.make_pom)
        self.record['aar_sha256'] = c.sha(sdk.read_bytes())
        self.record['dependencies_sha256'] = c.dependencies_sha(self.module)
        self.record['pom_sha256'] = c.sha(m.make_pom(self.record['version'], self.record['license_name'], self.record['license_url']))

    def test_reviewed_coordinate_accepts_the_existing_rc_binary(self):
        c.validate_contract(self.record, self.module, self.license)

    def test_cannot_publish_over_the_other_distribution_coordinate(self):
        self.record['artifact_id'] = 'identity-verification'
        with self.assertRaisesRegex(ValueError, 'coordenada AutDirectPro'):
            c.validate_contract(self.record, self.module, self.license)

    def test_cannot_substitute_another_binary_for_the_existing_rc(self):
        self.record['aar_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'AAR difiere'):
            c.validate_contract(self.record, self.module, self.license)

    def test_dependency_changes_require_another_rc(self):
        module = SimpleNamespace(GROUP=m.GROUP, ARTIFACT=m.ARTIFACT, SDK=self.module.SDK,
                                 DEPENDENCIES=m.DEPENDENCIES + (('example', 'unreviewed', '1.0'),))
        with self.assertRaisesRegex(ValueError, 'dependencias'):
            c.validate_contract(self.record, module, self.license)

    def test_cannot_change_license_metadata_after_pom_review(self):
        self.record['license_name'] += ' modificado'
        with self.assertRaisesRegex(ValueError, 'POM difiere'):
            c.validate_contract(self.record, self.module, self.license)

    def test_cannot_use_a_mutable_license_url(self):
        self.record['license_url'] = self.record['license_url'].replace(self.record['license_commit'], 'main')
        with self.assertRaisesRegex(ValueError, 'URL pública inmutable'):
            c.validate_contract(self.record, self.module, self.license)

    def test_rejects_a_source_tag_moved_to_another_commit(self):
        distribution = SimpleNamespace(gh_json=Mock(side_effect=[
            {'draft': False, 'prerelease': True}, {'object': {'type': 'commit', 'sha': '0' * 40}},
        ]))
        with self.assertRaisesRegex(ValueError, 'etiqueta de origen'):
            c.validate_source(self.record, distribution, {'repository': 'Becomedigital/BecomeDigitalSDKAutDirectPro-Android'})
