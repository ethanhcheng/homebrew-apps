cask "fladder" do
  version "0.12.1"
  sha256 "468f095d5e12c0950766f478df789207cade4ab62db3f005b2bcd448a7920f8e"

  url "https://github.com/DonutWare/Fladder/releases/download/v#{version}/Fladder-macOS-#{version}.dmg"
  name "Fladder"
  desc "Jellyfin client"
  homepage "https://github.com/DonutWare/Fladder"

  app "Fladder.app"
end
