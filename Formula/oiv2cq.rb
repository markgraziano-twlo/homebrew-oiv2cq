class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/oiv2cq"
  url "https://github.com/markgraziano-twlo/oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "389342d3351b621c2e529c9449c0f354f63734a8fd2fb57d05e10a676bf33619"
  license "MIT"

  depends_on "python@3.9"

  def install
    bin.install "oiv2cq"
  end

  test do
    system "#{bin}/oiv2cq", "--help"
  end
end
