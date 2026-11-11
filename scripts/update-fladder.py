#!/usr/bin/env python3
"""Validate the latest stable upstream DMG before updating the cask."""
import hashlib
import json
import os
from pathlib import Path
import plistlib
import re
import subprocess
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CASK = ROOT / 'Casks/fladder.rb'

def version_tuple(value):
    if not re.fullmatch(r'\d+\.\d+\.\d+', value):
        raise ValueError(f'Unexpected stable version: {value!r}')
    return tuple(map(int, value.split('.')))

def run(*args):
    return subprocess.check_output(args, text=True).strip()

def main():
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'fladder-personal-tap'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    req = urllib.request.Request('https://api.github.com/repos/DonutWare/Fladder/releases/latest', headers=headers)
    with urllib.request.urlopen(req, timeout=60) as response:
        release = json.load(response)
    if release['draft'] or release['prerelease']:
        raise ValueError('Expected a published stable release')
    tag = release['tag_name']
    version = tag.removeprefix('v')
    new_version = version_tuple(version)
    if tag != 'v' + version:
        raise ValueError('Upstream tag format changed')
    text = CASK.read_text()
    old_version = re.search(r'^  version "([^"]+)"$', text, re.M).group(1)
    if new_version < version_tuple(old_version):
        raise ValueError('Refusing a downgrade')
    expected_name = f'Fladder-macOS-{version}.dmg'
    assets = [a for a in release['assets'] if a['name'] == expected_name]
    if len(assets) != 1:
        raise ValueError('macOS asset missing or renamed; manual review required')
    asset = assets[0]
    expected_url = f'https://github.com/DonutWare/Fladder/releases/download/{tag}/{expected_name}'
    if asset['browser_download_url'] != expected_url:
        raise ValueError('Unexpected download URL')
    with tempfile.TemporaryDirectory() as temp:
        dmg = Path(temp) / expected_name
        digest = hashlib.sha256()
        with urllib.request.urlopen(expected_url, timeout=120) as response, dmg.open('wb') as target:
            while chunk := response.read(1024 * 1024):
                digest.update(chunk)
                target.write(chunk)
        sha = digest.hexdigest()
        upstream_digest = asset.get('digest')
        if upstream_digest and upstream_digest != 'sha256:' + sha:
            raise ValueError('Download does not match GitHub asset digest')
        current_sha = re.search(r'^  sha256 "([a-f0-9]{64})"$', text, re.M).group(1)
        if version == old_version and sha != current_sha:
            raise ValueError('Existing release asset changed; manual review required')
        mount = Path(temp) / 'mount'
        mount.mkdir()
        run('hdiutil', 'attach', '-readonly', '-nobrowse', '-mountpoint', str(mount), str(dmg))
        try:
            app = mount / 'Fladder.app'
            with (app / 'Contents/Info.plist').open('rb') as info:
                plist = plistlib.load(info)
            if plist['CFBundleIdentifier'] != 'nl.jknaapen.fladder':
                raise ValueError('Unexpected app bundle identifier')
            if plist['CFBundleShortVersionString'] != version:
                raise ValueError('App version does not match release')
            executable = plist['CFBundleExecutable']
            if Path(executable).name != executable:
                raise ValueError('Unexpected executable path')
            architectures = run('lipo', '-archs', str(app / 'Contents/MacOS' / executable)).split()
            if 'x86_64' not in architectures:
                raise ValueError('Intel support missing; manual review required')
        finally:
            run('hdiutil', 'detach', str(mount))
    text = re.sub(r'^  version "[^"]+"$', f'  version "{version}"', text, flags=re.M)
    text = re.sub(r'^  sha256 "[a-f0-9]{64}"$', f'  sha256 "{sha}"', text, flags=re.M)
    CASK.write_text(text)
    print(f'Validated Fladder {version}; Intel executable present')

if __name__ == '__main__':
    main()
