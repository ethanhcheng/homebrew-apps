# Personal Homebrew apps

Fladder cask, downloaded directly from DonutWare/Fladder. Initial version and checksum come from the upstream v0.11.1 release metadata.

## Repository setup

The repository has already been published. Fladder's first validation workflow passed. Its updater checks daily.

## Install on this Mac

Quit Fladder. Keep a backup of the existing app before replacement:

```sh
mkdir -p ~/homebrew-migration/backups
 ditto /Applications/Fladder.app ~/homebrew-migration/backups/Fladder-before-homebrew.app
brew install --cask --adopt ethanhcheng/apps/fladder
```

If adoption reports a different existing bundle, the backup is complete and you can replace the bundle using:

```sh
brew install --cask --force ethanhcheng/apps/fladder
```

The cask contains only an app artifact: no settings deletion, uninstall hooks, or quarantine bypasses. macOS may require you to approve opening the upstream app. Existing app data stays in place.

## Normal updates

```sh
brew update
brew upgrade --cask ethanhcheng/apps/fladder
```

The daily workflow checks stable releases, exact asset name and source, SHA-256 (also compared with GitHub's digest when available), bundle identifier, bundle version, and x86_64 in the main executable. It never launches the app or downloaded code. It stops on downgrades, missing Intel support, unexpected packaging, or replacement of an existing version's artifact. Ruby syntax must pass before a commit. Failures appear in Actions; enable GitHub workflow-failure notifications.

These checks do not test playback, plugin frameworks, signing/notarization, or the minimum supported macOS version. A successful workflow cannot guarantee the app will run on every Intel Mac. The workflow validates the DMG daily even when the version is unchanged. A checksum detects changed bytes; it is not an independent guarantee of upstream trustworthiness.

To check manually, run `python3 scripts/update-fladder.py` on a Mac with internet access. Review and commit any cask change. To pause automation, disable the Update Fladder workflow in Actions.

## Local validation status

Python and Ruby syntax checked. Live DMG validation and the hosted workflow have not been run from the restricted Codex session. Run the workflow once after publishing before adopting the app.

## Raycast v1 for Intel

The **Prepare fixed Raycast v1 cask** workflow downloads the official legacy DMG, requires version 1.104.35, verifies Intel support and the Raycast signing team, computes SHA-256, and publishes Casks/raycast@1.rb. It runs when its setup files change or through Actions → Run workflow. It does not automatically track newer releases. Once the cask exists, reruns leave it unchanged.

After that workflow succeeds, quit Raycast and run:

```sh
brew update
brew install --cask --adopt ethanhcheng/apps/raycast@1
```

If adoption refuses a different bundle, keep the existing app until you have backed it up before any replacement. There are no zap or uninstall hooks. Homebrew will not upgrade this cask to Raycast v2. The cask does not disable Raycast's own in-app updater.

The cask uses the vendor's version-specific Intel download URL. Its fixed checksum ensures that a changed download fails rather than silently installs a different version. If the vendor stops serving these bytes, a reviewed URL/checksum update is required. The workflow checks Intel support in the main executable, not every framework or app feature.
