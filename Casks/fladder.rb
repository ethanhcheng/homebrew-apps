cask "fladder" do
  version "0.12.0"
  sha256 "983a411c9e9e961d9c97dee9f432e01145492b8b604d2c3bacfbf5277eb0cdc9"

  url "https://github.com/DonutWare/Fladder/releases/download/v#{version}/Fladder-macOS-#{version}.dmg"
  name "Fladder"
  desc "Jellyfin client"
  homepage "https://github.com/DonutWare/Fladder"

  app "Fladder.app"
end
