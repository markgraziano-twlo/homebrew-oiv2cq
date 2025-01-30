class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "3a3f2d68cfda64094d6eeca8dde56aa77d97929e697196d177a4c22503c07b72" # Ensure the existing tarball's checksum is used
  license "MIT"

  depends_on "python"

  def install
    # Install the CLI files
    libexec.install "oiv2cq", "requirements.txt", "setup.py"

    # Install Python dependencies in the libexec environment
    system Formula["python"].opt_bin/"pip3", "install", "-r", libexec/"requirements.txt", "--target", libexec

    # Create a wrapper script
    (bin/"oiv2cq").write <<~EOS
      #!/bin/bash
      export PYTHONPATH=#{libexec}
      #{Formula["python"].opt_bin}/python3 #{libexec}/oiv2cq/cli.py "$@"
    EOS
    chmod "+x", bin/"oiv2cq"
  end

  test do
    system "#{bin}/oiv2cq", "--help"
  end
end
