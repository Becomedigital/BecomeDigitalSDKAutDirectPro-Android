"""La promoción conserva el contrato de la RC Maven bajo la nueva coordenada."""
import base64
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('promoted_coordinate_tests', ROOT / '.github/scripts/promoted_coordinate.py')
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


class PromotedCoordinate(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.record = {'version': '3.5.1-rc.1', 'group_id': 'ai.becomedigital',
                       'artifact_id': 'identity-verification-aut-direct-pro',
                       'license_file': 'legal/rc.txt', 'aar_sha256': p.sha(b'aar'),
                       'pom_sha256': p.sha(b'pom')}
        baseline = {'repository': p.REPOSITORY, 'platform': 'android',
                    'integration': ['scripts/prepare_maven_release.py', '.github/scripts/distribution.py',
                                    '.github/distribution.json', 'legal/rc.txt']}
        self.config = dict(baseline, integration=baseline['integration'] + p.ADDITIONS)
        self.originals = {
            '.github/distribution.json': json.dumps(baseline).encode(),
            'scripts/prepare_maven_release.py': b'POM revisado',
            '.github/scripts/maven_coordinate.py': b'Contrato revisado',
            '.github/maven-coordinate.json': json.dumps(self.record).encode(),
            'legal/rc.txt': b'Licencia RC aprobada',
        }
        for name, data in self.originals.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.run = {'status': 'completed', 'conclusion': 'success', 'head_sha': p.PUBLICATION_COMMIT,
                    'path': '.github/workflows/publicar-coordenada-maven.yml'}
        self.inputs = {'sdk.aar': 'binary', 'integration_sha256': 'reviewed'}
        self.api = SimpleNamespace(gh_json=Mock(side_effect=self.remote),
                                   release_inputs=Mock(return_value=self.inputs),
                                   platform_module=Mock(return_value=object()))
        self.contract = SimpleNamespace(validate_contract=Mock(), validate_source=Mock())
        self.loading = patch.object(p, 'load', return_value=self.contract)
        self.loading.start()
        self.addCleanup(self.loading.stop)
        self.download = patch.object(p, 'download', side_effect=lambda url: b'aar' if url.endswith('.aar') else b'pom')
        self.download_mock = self.download.start()
        self.addCleanup(self.download.stop)

    def remote(self, path):
        if '/actions/runs/' in path:
            self.assertTrue(path.endswith('/' + str(p.PUBLICATION_RUN)))
            return self.run
        prefix = f'repos/{p.REPOSITORY}/contents/'
        name, ref = path.removeprefix(prefix).split('?ref=')
        self.assertEqual(ref, p.PUBLICATION_COMMIT)
        return {'content': base64.b64encode(self.originals[name]).decode()}

    def verify(self):
        p.verify(self.api, self.config, '3.5.1-rc.1', self.inputs, self.root)

    def test_recognizes_the_successfully_published_coordinate(self):
        self.verify()
        self.contract.validate_contract.assert_called_once()
        self.contract.validate_source.assert_called_once()
        self.assertEqual(self.download_mock.call_count, 2)

    def test_exception_does_not_apply_to_another_repo_or_version(self):
        for repository, value in [('other/repository', '3.5.1-rc.1'), (p.REPOSITORY, '3.5.1-rc.2')]:
            config = dict(self.config, repository=repository)
            with self.subTest(repository=repository, version=value), self.assertRaisesRegex(ValueError, 'solo reconoce'):
                p.verify(self.api, config, value, self.inputs, self.root)

    def test_rejects_stale_prepared_inputs(self):
        self.api.release_inputs.return_value = {'sdk.aar': 'changed'}
        with self.assertRaisesRegex(ValueError, 'registro de promoción'):
            self.verify()

    def test_does_not_allow_arbitrary_changes_to_the_configuration(self):
        self.config['required_abis'] = ['arm64-v8a']
        with self.assertRaisesRegex(ValueError, 'configuración de integración'):
            self.verify()

    def test_requires_identical_runtime_pom_contract_and_rc_license(self):
        for name in ['scripts/prepare_maven_release.py', '.github/scripts/maven_coordinate.py',
                     '.github/maven-coordinate.json', 'legal/rc.txt']:
            path = self.root / name
            previous = path.read_bytes()
            path.write_bytes(b'changed')
            with self.subTest(path=name), self.assertRaisesRegex(ValueError, 'Cambió un archivo'):
                self.verify()
            path.write_bytes(previous)

    def test_rejects_an_unpublished_or_different_commit(self):
        for key, value in [('status', 'in_progress'), ('conclusion', 'failure'),
                           ('head_sha', '0' * 40), ('path', '.github/workflows/other.yml')]:
            before = copy.copy(self.run)
            self.run[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'publicación exitosa'):
                self.verify()
            self.run = before

    def test_retains_source_tag_binary_and_dependency_validation(self):
        for message in ['La etiqueta de origen cambió', 'Los binarios cambiaron', 'Cambiaron las dependencias']:
            self.contract.validate_source.side_effect = ValueError(message)
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                self.verify()

    def test_requires_the_reviewed_public_pom_and_aar(self):
        for extension in ['aar', 'pom']:
            self.download_mock.side_effect = lambda url: b'changed' if url.endswith('.' + extension) else (b'aar' if url.endswith('.aar') else b'pom')
            with self.subTest(extension=extension), self.assertRaisesRegex(ValueError, 'Maven público.*' + extension):
                self.verify()

    def test_public_artifact_unavailability_cannot_be_ignored(self):
        self.download_mock.side_effect = OSError('No disponible')
        with self.assertRaises(OSError):
            self.verify()
