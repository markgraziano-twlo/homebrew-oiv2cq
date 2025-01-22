class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/oiv2cq"
  url "https://github.com/markgraziano-twlo/oiv2cq/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "e4ab9465f554c1a24698ee87677112efbd9c5c61832736428b962d6e86f13384"
  license "MIT"

  depends_on "python@3.9"

  def install
    bin.install "oiv2cq"
  end

  test do
    system "#{bin}/oiv2cq", "--help"
  end
end
