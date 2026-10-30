#!/usr/bin/env python3
"""Valida el AAR Legacy y prepara una publicación Maven local."""

from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CHECKSUMS = ROOT / "CHECKSUMS.sha256"
SDK = ROOT / "becomedigitalsdk.aar"
CAPTURE_CORE = ROOT / "libs/capture-core-1.4.1.aar"
CAPTURE_UX = ROOT / "libs/capture-ux-1.4.1.aar"
GROUP = "net.becomedigital"
ARTIFACT = "identity-verification-legacy"
POM_NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", POM_NS)

# Las versiones corresponden al artefacto y a la guía de integración actuales.
DEPENDENCIES = (
    ("com.microblink", "capture-core", "1.4.1"),
    ("com.microblink", "capture-ux", "1.4.1"),
    ("androidx.appcompat", "appcompat", "1.7.1"),
    ("androidx.constraintlayout", "constraintlayout", "2.1.4"),
    ("androidx.core", "core-ktx", "1.15.0"),
    ("androidx.activity", "activity-ktx", "1.12.4"),
    ("androidx.activity", "activity-compose", "1.12.4"),
    ("androidx.fragment", "fragment-ktx", "1.6.2"),
    ("androidx.navigation", "navigation-fragment", "2.5.3"),
    ("androidx.navigation", "navigation-ui", "2.5.3"),
    ("androidx.compose.material3", "material3", "1.4.0"),
    ("androidx.camera", "camera-core", "1.5.3"),
    ("androidx.camera", "camera-camera2", "1.5.3"),
    ("androidx.camera", "camera-view", "1.5.3"),
    ("androidx.camera", "camera-lifecycle", "1.5.3"),
    ("com.google.guava", "guava", "33.3.1-android"),
    ("com.amplifyframework.ui", "liveness", "1.10.0"),
    ("com.amplifyframework", "aws-auth-cognito", "2.33.0"),
    ("com.google.code.gson", "gson", "2.10.1"),
    ("com.squareup.okhttp3", "okhttp", "4.9.3"),
    ("com.android.volley", "volley", "1.2.1"),
    ("com.github.bumptech.glide", "glide", "4.10.0"),
    ("androidx.room", "room-runtime", "2.6.1"),
    ("androidx.lifecycle", "lifecycle-livedata", "2.8.7"),
    ("androidx.lifecycle", "lifecycle-viewmodel", "2.8.7"),
)


def digest(path: Path, algorithm: str) -> str:
    checksum = hashlib.new(algorithm)
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def verify_checksums() -> None:
    checked: set[Path] = set()
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        expected, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        if path not in (SDK, CAPTURE_CORE, CAPTURE_UX) or path in checked:
            raise ValueError(f"Ruta de checksum inesperada: {relative}")
        checked.add(path)
        if digest(path, "sha256") != expected:
            raise ValueError(f"El checksum no coincide: {relative}")
    if checked != {SDK, CAPTURE_CORE, CAPTURE_UX}:
        raise ValueError("Faltan checksums de los tres AAR")


def inspect_aar(path: Path) -> zipfile.ZipFile:
    archive = zipfile.ZipFile(path)
    bad_file = archive.testzip()
    if bad_file:
        archive.close()
        raise ValueError(f"AAR dañado: {path.name}: {bad_file}")
    if "classes.jar" not in archive.namelist():
        archive.close()
        raise ValueError(f"Falta classes.jar: {path.name}")
    return archive


def validate_artifacts(version: str) -> None:
    verify_checksums()
    issues: list[str] = []
    with inspect_aar(SDK) as sdk:
        manifest = sdk.read("AndroidManifest.xml").decode("utf-8")
        if 'android:minSdkVersion="24"' not in manifest:
            raise ValueError("La SDK no declara Android API 24 como mínimo")
        if "proguard.txt" not in sdk.namelist():
            raise ValueError("Faltan las reglas R8 del AAR")
        with zipfile.ZipFile(BytesIO(sdk.read("classes.jar"))) as classes:
            config = classes.read("com/becomedigital/sdk/identity/becomedigitalsdk/BuildConfig.class")
            if b"https://api.svi.becomedigital.net" not in config or b"prod" not in config:
                raise ValueError("El AAR no corresponde al ambiente de producción")
        values = sdk.read("res/values/values.xml").decode("utf-8")
        match = re.search(r'<string name="sdk_version"[^>]*>(.*?)</string>', values)
        if not match or version not in match.group(1):
            issues.append("La versión interna del AAR no coincide con la versión Maven")
    with inspect_aar(CAPTURE_CORE) as core, inspect_aar(CAPTURE_UX):
        native_abis = {
            name.split("/")[1]
            for name in core.namelist()
            if name.startswith("jni/") and name.endswith(".so")
        }
        required_abis = {"arm64-v8a", "x86_64"}
        if not required_abis.issubset(native_abis):
            missing = ", ".join(sorted(required_abis - native_abis))
            issues.append(f"Capture Core 1.4.1 carece de ABI requerida: {missing}")
    if issues:
        raise ValueError("; ".join(issues))


def add(parent: ET.Element, name: str, value: str | None = None) -> ET.Element:
    child = ET.SubElement(parent, f"{{{POM_NS}}}{name}")
    if value is not None:
        child.text = value
    return child


def make_pom(version: str, license_name: str, license_url: str) -> bytes:
    project = ET.Element(f"{{{POM_NS}}}project")
    add(project, "modelVersion", "4.0.0")
    add(project, "groupId", GROUP)
    add(project, "artifactId", ARTIFACT)
    add(project, "version", version)
    add(project, "packaging", "aar")
    add(project, "name", "Become Digital Identity Verification Legacy para Android")
    add(project, "description", "Verificación de identidad para aplicaciones Android.")
    url = "https://github.com/Becomedigital/BecomeDigitalSDKAutDirectPro-Android"
    add(project, "url", url)
    license_node = add(add(project, "licenses"), "license")
    add(license_node, "name", license_name)
    add(license_node, "url", license_url)
    add(license_node, "distribution", "repo")
    developer = add(add(project, "developers"), "developer")
    add(developer, "id", "BecomeDigital")
    add(developer, "name", "Become Digital SAS")
    scm = add(project, "scm")
    add(scm, "url", url)
    add(scm, "connection", f"scm:git:{url}.git")
    add(scm, "developerConnection", f"scm:git:{url}.git")
    dependencies = add(project, "dependencies")
    for group, artifact, dependency_version in DEPENDENCIES:
        dependency = add(dependencies, "dependency")
        add(dependency, "groupId", group)
        add(dependency, "artifactId", artifact)
        add(dependency, "version", dependency_version)
        add(dependency, "scope", "compile")
    ET.indent(project, space="  ")
    return ET.tostring(project, encoding="utf-8", xml_declaration=True) + b"\n"


def make_reference_jar(path: Path, kind: str) -> None:
    note = (
        f"{kind} de Become Digital Identity Verification Legacy.\n"
        "Este paquete se distribuye como binario. Consulte la guía pública de integración:\n"
        "https://github.com/Becomedigital/BecomeDigitalSDKAutDirectPro-Android\n"
    )
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        entry = zipfile.ZipInfo("README.md", (1980, 1, 1, 0, 0, 0))
        archive.writestr(entry, note.encode("utf-8"))


def stage(version: str, license_name: str, license_url: str, sign: bool, gpg_key: str | None) -> Path:
    root = ROOT / "dist" / "maven-repository" / Path(*GROUP.split(".")) / ARTIFACT / version
    if root.exists():
        raise ValueError("La versión ya existe en el repositorio local; no se sobrescribe")
    root.mkdir(parents=True)
    stem = f"{ARTIFACT}-{version}"
    files = [root / f"{stem}.aar", root / f"{stem}.pom",
             root / f"{stem}-sources.jar", root / f"{stem}-javadoc.jar"]
    shutil.copyfile(SDK, files[0])
    files[1].write_bytes(make_pom(version, license_name, license_url))
    make_reference_jar(files[2], "Fuentes")
    make_reference_jar(files[3], "Documentación")
    for path in files:
        if sign:
            command = ["gpg", "--armor", "--detach-sign", "--output", str(path) + ".asc"]
            command += ["--local-user", gpg_key]
            subprocess.run(command + [str(path)], check=True)
            subprocess.run(["gpg", "--verify", str(path) + ".asc", str(path)], check=True,
                           capture_output=True, text=True)
        for algorithm in ("md5", "sha1", "sha256", "sha512"):
            Path(str(path) + "." + algorithm).write_text(digest(path, algorithm), encoding="ascii")
    return root


def make_bundle(version: str) -> Path:
    repository = ROOT / "dist" / "maven-repository"
    version_dir = repository / Path(*GROUP.split(".")) / ARTIFACT / version
    output = ROOT / "dist" / f"central-bundle-{version}.zip"
    if output.exists():
        raise ValueError("El bundle de esta versión ya existe; no se sobrescribe")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(version_dir.rglob("*")):
            if not path.is_file():
                continue
            entry = zipfile.ZipInfo(path.relative_to(repository).as_posix(), (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, path.read_bytes())
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Versión exacta, por ejemplo 1.2.3")
    parser.add_argument("--check", action="store_true", help="Solo validar artefactos")
    parser.add_argument("--license-name", default="Licencia de Become Digital SDK")
    parser.add_argument("--license-url", help="URL pública de los términos de licencia aprobados")
    parser.add_argument("--sign", action="store_true", help="Firmar los archivos con GPG")
    parser.add_argument("--gpg-key", help="Huella de la clave GPG")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-rc\.[0-9]+)?", args.version):
        parser.error("La versión debe cumplir SemVer")
    validate_artifacts(args.version)
    if args.check:
        print("Los AAR cumplen la validación para Maven")
        return
    if not args.license_url or not args.license_url.startswith("https://"):
        parser.error("Se necesita --license-url con una URL HTTPS aprobada")
    if "example.invalid" in args.license_url:
        parser.error("No se permite una URL de licencia de ejemplo")
    if args.sign and not args.gpg_key:
        parser.error("Se necesita --gpg-key para firmar")
    path = stage(args.version, args.license_name, args.license_url, args.sign, args.gpg_key)
    print(f"Repositorio Maven local: {path}")
    if args.sign:
        print(f"Bundle para Central: {make_bundle(args.version)}")
    else:
        print("Faltan las firmas GPG para publicar en Maven Central", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(f"Preparación Maven detenida: {error}", file=sys.stderr)
        sys.exit(1)
