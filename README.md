# Personal Homebrew apps

Fladder cask, downloaded directly from DonutWare/Fladder. Initial version and checksum come from the upstream v0.11.1 release metadata.

## Publish once

Create an empty public repository named `homebrew-apps` at https://github.com/new under `ethanhcheng`. Do not initialize it with a README, license, or gitignore. Then run in Terminal:

```sh
cd ~/homebrew-apps
git init -b main
git add Casks scripts .github README.md
git -c user.name=ethanhcheng -c user.email=157773553+ethanhcheng@users.noreply.github.com commit -m "Add Fladder cask and automatic release updates"
git remote add origin https://github.com/ethanhcheng/homebrew-apps.git
git push -u origin main
```

Git will require GitHub authentication (a token or credential helper; account passwords do not work). Alternatively upload the files through GitHub, preserving the `.github/workflows/` directory.

In the repository's Actions tab, enable Actions if prompted. Select **Update Fladder → Run workflow**. Wait for a successful run before installing. This first run downloads the DMG and verifies the initial checksum and Intel executable. Subsequent runs occur daily and commit version/checksum changes directly to main. No separate secret or PR approval is needed; the repository's GITHUB_TOKEN is used. Branch protection requiring PRs will prevent direct updates. Scheduled workflows in inactive public repositories may be disabled after 60 days; re-enable them in Actions if GitHub notifies you.

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
