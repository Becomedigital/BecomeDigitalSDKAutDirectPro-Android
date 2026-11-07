#!/usr/bin/env python3
"""Verifica que el APK conserve las versiones de Compose utilizadas al compilar la SDK."""
import argparse
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[2]


def inspect(path, versions):
    checked, errors = {}, []
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if not name.startswith('META-INF/androidx.compose.') or not name.endswith('.version'):
                continue
            coordinate = name.removeprefix('META-INF/').removesuffix('.version').replace('_', ':', 1)
            if coordinate not in versions:
                continue
            actual = archive.read(name).decode().strip()
            expected = versions[coordinate]
            checked[coordinate] = actual
            if actual != expected:
                errors.append(f'{coordinate}: se resolvió {actual}; la SDK se compiló con {expected}')
    if not checked:
        errors.append('No se encontraron metadatos de Compose para comprobar la compatibilidad.')
    return {'file': str(path), 'versions': checked, 'errors': errors, 'passed': not errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path, help='APK consumidores debug y release')
    parser.add_argument('--output', type=Path, help='Archivo JSON opcional con los resultados')
    args = parser.parse_args()
    bom = json.loads((ROOT / 'scripts/compose-bom-versions.json').read_text())
    results = [inspect(path, bom['versions']) for path in args.files]
    if args.output:
        args.output.write_text(json.dumps({'bom': bom['coordinate'], 'artifacts': results}, indent=2) + '\n')
    for result in results:
        print(('PASS' if result['passed'] else 'FAIL') + ' ' + result['file'])
        for error in result['errors']:
            print('  ' + error)
    return 0 if all(result['passed'] for result in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
