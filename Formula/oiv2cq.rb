class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.1/oiv2cq-v1.0.1.tar.gz"
  sha256 "e67710c4aedecf8e2b64278c1db4b0c1c7f9af6757e93116bf7d2af3d20b0eea"
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
