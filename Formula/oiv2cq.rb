class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "ede8b8dd4b5770c8d8ce49f513be3c7aec16f723ae7914c21421af2e36df8562"
  license "MIT"

  depends_on "python"

  def install
    # Install CLI files
    libexec.install Dir["*"]

    # Install dependencies into the virtual environment
  system Formula["python"].opt_bin/"python3", "-m", "venv", libexec/"venv"
  system "#{libexec}/venv/bin/pip", "install", "-r", libexec/"requirements.txt"

  # Create the wrapper script
  (bin/"oiv2cq").write <<~EOS
    #!/bin/bash
    source #{libexec}/venv/bin/activate
    python3 #{libexec}/oiv2cq/cli.py "$@"
  EOS
  chmod "+x", bin/"oiv2cq"
end

  test do
    system "#{bin}/oiv2cq", "--help"
  end
end
