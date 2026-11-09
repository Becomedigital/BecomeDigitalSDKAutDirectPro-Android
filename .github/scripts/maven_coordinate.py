#!/usr/bin/env python3
"""Publica una nueva coordenada Maven con el binario de una RC ya publicada."""
from pathlib import Path
import argparse
import ast
import base64
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dependencies_sha(module):
    return sha(json.dumps(module.DEPENDENCIES, separators=(',', ':')).encode())


def validate_contract(record, module, license_bytes):
    if record['group_id'] != 'ai.becomedigital' or record['artifact_id'] != 'identity-verification-aut-direct-pro':
        raise ValueError('La publicación debe usar la coordenada AutDirectPro aprobada.')
    if module.GROUP != record['group_id'] or module.ARTIFACT != record['artifact_id']:
        raise ValueError('La coordenada del POM difiere de la revisada.')
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+-rc\.[1-9][0-9]*', record['version']):
        raise ValueError('Este flujo solo admite una RC revisada.')
    if record['version'] != record['source_tag']:
        raise ValueError('Debe conservarse la versión de la RC de origen.')
    if sha(module.SDK.read_bytes()) != record['aar_sha256']:
        raise ValueError('El AAR difiere de la RC de origen; prepara otra RC.')
    if dependencies_sha(module) != record['dependencies_sha256']:
        raise ValueError('Cambiaron las dependencias de la RC de origen.')
    if sha(license_bytes) != record['license_sha256']:
        raise ValueError('Cambió el texto de licencia revisado.')
    coordinate = record['group_id'] + ':' + record['artifact_id'] + ':' + record['version']
    if coordinate not in license_bytes.decode('utf-8'):
        raise ValueError('La licencia no identifica la coordenada y versión revisadas.')
    expected_url = ('https://raw.githubusercontent.com/Becomedigital/BecomeDigitalSDKAutDirectPro-Android/'
                    + record['license_commit'] + '/' + record['license_file'])
    if not re.fullmatch(r'[0-9a-f]{40}', record['license_commit']) or record['license_url'] != expected_url:
        raise ValueError('La licencia debe tener una URL pública inmutable del repositorio.')
    if record['license_file'] != 'legal/LICENSE-AutDirectPro-3.5.1-rc.1.txt':
        raise ValueError('El archivo de licencia no corresponde a esta publicación.')
    pom = module.make_pom(record['version'], record['license_name'], record['license_url'])
    if sha(pom) != record['pom_sha256']:
        raise ValueError('El POM difiere del revisado.')


def validate_source(record, distribution, config):
    repo = config['repository']
    release = distribution.gh_json(f"repos/{repo}/releases/tags/{record['source_tag']}")
    if release['draft'] or not release['prerelease']:
        raise ValueError('La RC de origen debe estar publicada.')
    ref = distribution.gh_json(f"repos/{repo}/git/ref/tags/{record['source_tag']}")['object']
    while ref['type'] == 'tag':
        ref = distribution.gh_json(f"repos/{repo}/git/tags/{ref['sha']}")['object']
    if ref['type'] != 'commit' or ref['sha'] != record['source_commit']:
        raise ValueError('La etiqueta de origen no corresponde al commit revisado.')
    data = distribution.gh_json(f"repos/{repo}/contents/.github/release.json?ref={record['source_tag']}")
    source = json.loads(base64.b64decode(data['content']))
    if source['version'] != record['version'] or source['inputs']['becomedigitalsdk.aar'] != record['aar_sha256']:
        raise ValueError('La RC publicada no contiene el AAR revisado.')
    actual = distribution.inputs(config)
    if actual != {k: v for k, v in source['inputs'].items() if k != 'integration_sha256'}:
        raise ValueError('Los binarios cambiaron respecto de la RC publicada.')
    data = distribution.gh_json(f"repos/{repo}/contents/scripts/prepare_maven_release.py?ref={record['source_tag']}")
    source_tree = ast.parse(base64.b64decode(data['content']).decode('utf-8'))
    dependencies = next(ast.literal_eval(node.value) for node in source_tree.body
                        if isinstance(node, ast.Assign)
                        and any(isinstance(target, ast.Name) and target.id == 'DEPENDENCIES' for target in node.targets))
    if sha(json.dumps(dependencies, separators=(',', ':')).encode()) != record['dependencies_sha256']:
        raise ValueError('Las dependencias difieren de la RC publicada.')
    data = distribution.gh_json(f"repos/{repo}/contents/{record['license_file']}?ref={record['license_commit']}")
    if sha(base64.b64decode(data['content'])) != record['license_sha256']:
        raise ValueError('La licencia pública difiere de la revisada.')


def check():
    record = json.loads((ROOT / '.github/maven-coordinate.json').read_text())
    distribution = load_module('coordinate_distribution', ROOT / '.github/scripts/distribution.py')
    module = load_module('coordinate_maven', ROOT / 'scripts/prepare_maven_release.py')
    config = json.loads((ROOT / '.github/distribution.json').read_text())
    validate_contract(record, module, (ROOT / record['license_file']).read_bytes())
    module.validate_artifacts(record['version'].split('-')[0])
    return record, distribution, module, config


def assemble(record, module, output):
    folder = module.stage(record['version'], record['license_name'], record['license_url'], False, None)
    pom = next(folder.glob('*.pom'))
    if sha(pom.read_bytes()) != record['pom_sha256']:
        raise ValueError('El POM generado difiere del revisado.')
    relative = Path(*module.GROUP.split('.')) / module.ARTIFACT / record['version']
    shutil.copytree(folder, output / 'maven' / relative)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'coordinate-publication.json').write_text(json.dumps(record, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['check', 'preflight', 'assemble', 'publish'])
    parser.add_argument('--output', type=Path, default=Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'become-maven-coordinate')
    args = parser.parse_args()
    record, distribution, module, config = check()
    if args.command == 'preflight':
        if os.environ.get('GITHUB_REF') != 'refs/heads/main':
            raise ValueError('Esta publicación requiere el commit revisado en main.')
        distribution.publication_gate(config)
        validate_source(record, distribution, config)
    elif args.command == 'assemble':
        assemble(record, module, args.output)
    elif args.command == 'publish':
        pom = next((args.output / 'maven').rglob('*.pom'))
        aar = pom.with_suffix('.aar')
        if sha(pom.read_bytes()) != record['pom_sha256'] or sha(aar.read_bytes()) != record['aar_sha256']:
            raise ValueError('El paquete preparado difiere del revisado.')
        distribution.publish_central(args.output)
    print('Coordenada Maven validada: ' + record['group_id'] + ':' + record['artifact_id'] + ':' + record['version'])


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration) as error:
        print('Error: ' + str(error), file=sys.stderr)
        sys.exit(1)
