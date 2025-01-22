class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "ef4279fd167cb0609dd8c36a2bbc8a11e20eba66f4370e8473d1d298a4373c81"
  license "MIT"

  depends_on "python"  # Use the latest Python version

  def install
    libexec.install "oiv2cq", "requirements.txt", "setup.py"

    # Dynamically resolve Python path
    python_path = "#{Formula["python"].opt_bin}/python3"

    # Create a wrapper script for the CLI
    (bin/"oiv2cq").write <<~EOS
      #!/bin/bash
      #{python_path} #{libexec}/oiv2cq/cli.py "$@"
    EOS
    chmod "+x", bin/"oiv2cq"
  end

  test do
    system "#{bin}/oiv2cq", "--help"
  end
end
