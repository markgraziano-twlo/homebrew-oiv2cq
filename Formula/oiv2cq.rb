class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "e7e263380a0dfa44b663baf34c9de937b5fbaa02128babeae2a5495c90de530f"
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
