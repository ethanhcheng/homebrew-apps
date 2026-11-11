#!/usr/bin/env python3
"""Publish a fixed v1 cask only after checking the vendor's actual DMG."""
import hashlib
from pathlib import Path
import plistlib
import subprocess
import tempfile
import urllib.request

VERSION = '1.104.35'
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'Casks/raycast@1.rb'

def run(*args):
    return subprocess.check_output(args, text=True).strip()

def main():
    if TARGET.exists():
        print('Fixed cask already exists; leaving version and checksum unchanged.')
        return
    # Official legacy download page links to this endpoint. The checksum locks
    # the resulting cask to these bytes even if the vendor later changes it.
    url = 'https://releases.raycast.com/download'
    with tempfile.TemporaryDirectory() as temp:
        dmg = Path(temp) / 'Raycast.dmg'
        digest = hashlib.sha256()
        with urllib.request.urlopen(url, timeout=120) as response, dmg.open('wb') as output:
            while chunk := response.read(1024 * 1024):
                digest.update(chunk)
                output.write(chunk)
        mount = Path(temp) / 'mount'
        mount.mkdir()
        run('hdiutil', 'attach', '-readonly', '-nobrowse', '-mountpoint', str(mount), str(dmg))
        try:
            app = mount / 'Raycast.app'
            with (app / 'Contents/Info.plist').open('rb') as source:
                info = plistlib.load(source)
            if info.get('CFBundleIdentifier') != 'com.raycast.macos':
                raise ValueError('Unexpected app identifier')
            if info.get('CFBundleShortVersionString') != VERSION:
                raise ValueError(f'Expected {VERSION}, received {info.get("CFBundleShortVersionString")}; refusing update')
            executable = info['CFBundleExecutable']
            if Path(executable).name != executable:
                raise ValueError('Unexpected executable path')
            if 'x86_64' not in run('lipo', '-archs', str(app / 'Contents/MacOS' / executable)).split():
                raise ValueError('Intel executable missing')
            # Check the mounted bundle without launching it.
            run('codesign', '--verify', '--deep', '--strict', str(app))
            signing = subprocess.run(['codesign', '-dv', '--verbose=4', str(app)], capture_output=True, text=True, check=True)
            if 'TeamIdentifier=SY64MV22J9' not in signing.stderr:
                raise ValueError('Unexpected Raycast signing team')
        finally:
            run('hdiutil', 'detach', str(mount))
    text = f'''cask "raycast@1" do
  version "{VERSION}"
  sha256 "{digest.hexdigest()}"

  url "{url}"
  name "Raycast v1"
  desc "Legacy Raycast release for Intel Macs"
  homepage "https://www.raycast.com/download/unsupported"

  livecheck do
    skip "Fixed legacy release; update only after reviewing Intel compatibility"
  end

  depends_on macos: ">= :ventura"
  conflicts_with cask: "raycast"

  app "Raycast.app"
end
'''
    TARGET.write_text(text)
    try:
        run('ruby', '-c', str(TARGET))
    except Exception:
        TARGET.unlink()
        raise
    print(f'Validated Raycast {VERSION}, signature and Intel executable; SHA-256 {digest.hexdigest()}')

if __name__ == '__main__':
    main()
