cask "raycast@1" do
  version "1.104.35"
  sha256 "feb3006f9ef4cf2b3271468517505d4df7d523008880920b11c6dd2c35ae5f32"

  url "https://releases.raycast.com/releases/1.104.35/download?build=x86_64"
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
