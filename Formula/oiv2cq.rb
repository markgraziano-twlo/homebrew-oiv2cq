class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "9d91582b8d03a496a1f2af48d0bd66cdd755fd55969b3d3ba4c7a6f380454b5e" # Ensure the existing tarball's checksum is used
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
