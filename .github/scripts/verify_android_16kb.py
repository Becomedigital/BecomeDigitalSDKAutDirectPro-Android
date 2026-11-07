#!/usr/bin/env python3
"""Verifica los segmentos LOAD ELF de 64 bits y las bibliotecas nativas sin comprimir del APK."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zipfile

PAGE = 16_384


def inspect(path):
    path = Path(path)
    libraries = []
    errors = []
    with zipfile.ZipFile(path) as archive, path.open('rb') as raw:
        for info in archive.infolist():
            if not info.filename.endswith('.so'):
                continue
            data = archive.read(info)
            if data[:4] != b'\x7fELF':
                errors.append(f'{info.filename}: ELF inválido')
                continue
            if data[4] != 2:
                continue  # El requisito de páginas de 16 KB aplica a las arquitecturas de 64 bits.
            endian = '<' if data[5] == 1 else '>'
            offset = struct.unpack_from(endian + 'Q', data, 32)[0]
            size, count = struct.unpack_from(endian + 'HH', data, 54)
            segments = [struct.unpack_from(endian + 'IIQQQQQQ', data, offset + i * size)
                        for i in range(count)]
            loads = [s for s in segments if s[0] == 1]
            aligned = bool(loads) and all(s[7] >= PAGE and s[2] % PAGE == s[3] % PAGE for s in loads)
            zip_aligned = None
            if path.suffix == '.apk' and info.compress_type == zipfile.ZIP_STORED:
                raw.seek(info.header_offset)
                header = raw.read(30)
                name_len, extra_len = struct.unpack_from('<HH', header, 26)
                zip_aligned = (info.header_offset + 30 + name_len + extra_len) % PAGE == 0
            entry = {'name': info.filename, 'sha256': hashlib.sha256(data).hexdigest(),
                     'load_alignment_bytes': sorted({s[7] for s in loads}),
                     'elf_16kb': aligned, 'apk_zip_16kb': zip_aligned}
            libraries.append(entry)
            if not aligned or zip_aligned is False:
                errors.append(f'{info.filename}: alineación ELF o APK incompatible')
    if not libraries:
        errors.append('No se encontraron bibliotecas nativas de 64 bits; no se pudo verificar la compatibilidad')
    return {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'libraries': libraries, 'errors': errors, 'passed': not errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', help='Archivos AAR, APK o AAB')
    parser.add_argument('--output', type=Path, help='Archivo JSON opcional con los resultados de verificación')
    args = parser.parse_args()
    results = [inspect(p) for p in args.files]
    report = {'page_size': PAGE, 'functional_camera_test_performed': False, 'artifacts': results}
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    for result in results:
        print(('PASS' if result['passed'] else 'FAIL') + ' ' + result['file'])
        for entry in result['libraries']:
            print('  ' + entry['name'] + ': ELF=' + str(entry['load_alignment_bytes']) +
                  ', APK ZIP=' + str(entry['apk_zip_16kb']))
        for error in result['errors']:
            print('  ' + error)
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
