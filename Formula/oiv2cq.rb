class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "0a792fe5120e8bc2b29a8eab8a25762ea27f3cf2a5e359bba65aeb393bbc5528"
  license "MIT"

  depends_on "python"

  def install
    # Install CLI files
    libexec.install "oiv2cq", "requirements.txt", "setup.py", "prereqs.py", "template_create.py", "cli.py"

    # Create and set up the virtual environment inside libexec
    system Formula["python"].opt_bin/"python3", "-m", "venv", "#{libexec}/venv"
    system "#{libexec}/venv/bin/pip", "install", "-r", "#{libexec}/requirements.txt"

    # Create a wrapper script to activate the virtual environment and run the CLI
    (bin/"oiv2cq").write <<~EOS
      #!/bin/bash
      source "#{libexec}/venv/bin/activate"
      python3 #{libexec}/cli.py "$@"
    EOS
    chmod "+x", bin/"oiv2cq"
  end

  test do
    system "#{bin}/oiv2cq", "--help"
  end
end
