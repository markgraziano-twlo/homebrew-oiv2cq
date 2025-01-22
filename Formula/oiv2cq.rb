class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "389342d3351b621c2e529c9449c0f354f63734a8fd2fb57d05e10a676bf33619"
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
