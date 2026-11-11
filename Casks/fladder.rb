cask "fladder" do
  version "0.11.1"
  sha256 "db7f93e833a14afabb71032a0664c831c567128d5b60c6accc402775065efe51"

  url "https://github.com/DonutWare/Fladder/releases/download/v#{version}/Fladder-macOS-#{version}.dmg"
  name "Fladder"
  desc "Jellyfin client"
  homepage "https://github.com/DonutWare/Fladder"

  app "Fladder.app"
end
