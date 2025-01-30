class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "22be46263eeec3c5672360fbe3e4ddf9fd1a4233571079040f9e1ea8793390aa"
  license "MIT"

  depends_on "python"

  def install
    # Install CLI files
    libexec.install Dir["*"]

    # Create and set up the virtual environment inside libexec
    system Formula["python"].opt_bin/"python3", "-m", "venv", "#{libexec}/venv"
    system "#{libexec}/venv/bin/pip", "install", "-r", "#{libexec}/requirements.txt"

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
