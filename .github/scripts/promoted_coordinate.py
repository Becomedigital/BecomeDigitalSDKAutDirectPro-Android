"""Reconoce la RC AutDirectPro publicada sin modificar la etiqueta de origen."""
import base64
import hashlib
import importlib.util
import json
import urllib.request


REPOSITORY = 'Becomedigital/BecomeDigitalSDKAutDirectPro-Android'
PUBLICATION_COMMIT = '32c87e5809c7a8096414f9bd158eb01941cdb14f'
PUBLICATION_RUN = 42659446540
ADDITIONS = ['.github/scripts/promoted_coordinate.py', '.github/scripts/maven_coordinate.py',
             '.github/maven-coordinate.json']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    spec = importlib.util.spec_from_file_location('promoted_coordinate_contract', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def download(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def verify(distribution, config, value, source_inputs, root):
    require(config['repository'] == REPOSITORY and config['platform'] == 'android'
            and value == '3.5.1-rc.1', 'La excepción solo reconoce la RC AutDirectPro 3.5.1-rc.1.')
    require(source_inputs == distribution.release_inputs(config, root),
            'Los archivos actuales no corresponden al registro de promoción.')

    def original(path):
        data = distribution.gh_json(f'repos/{REPOSITORY}/contents/{path}?ref={PUBLICATION_COMMIT}')
        return base64.b64decode(data['content'])

    baseline = json.loads(original('.github/distribution.json'))
    expected = dict(baseline, integration=baseline['integration'] + ADDITIONS)
    require(config == expected, 'Cambió la configuración de integración de la RC publicada.')
    for path in baseline['integration'] + ADDITIONS[1:]:
        if path in ('.github/scripts/distribution.py', '.github/distribution.json'):
            continue
        require((root / path).read_bytes() == original(path),
                'Cambió un archivo de la RC publicada: ' + path)

    record = json.loads((root / '.github/maven-coordinate.json').read_text())
    require(record['version'] == value, 'La coordenada publicada no corresponde a la RC validada.')
    run = distribution.gh_json(f'repos/{REPOSITORY}/actions/runs/{PUBLICATION_RUN}')
    require(run['status'] == 'completed' and run['conclusion'] == 'success'
            and run['head_sha'] == PUBLICATION_COMMIT
            and run['path'] == '.github/workflows/publicar-coordenada-maven.yml',
            'No existe una publicación exitosa del commit revisado de la coordenada Maven.')

    coordinate = load(root / '.github/scripts/maven_coordinate.py')
    module = distribution.platform_module(config, root)
    coordinate.validate_contract(record, module, (root / record['license_file']).read_bytes())
    coordinate.validate_source(record, distribution, config)

    base = ('https://repo.maven.apache.org/maven2/' + record['group_id'].replace('.', '/')
            + '/' + record['artifact_id'] + '/' + value + '/' + record['artifact_id'] + '-' + value)
    for extension, key in [('aar', 'aar_sha256'), ('pom', 'pom_sha256')]:
        require(sha(download(base + '.' + extension)) == record[key],
                'El archivo Maven público difiere de la RC revisada: ' + extension)
