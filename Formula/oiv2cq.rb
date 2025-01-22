class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.2/oiv2cq-v1.0.2.tar.gz"
  sha256 "9350c8cc242e67fc58c539e0e8b7a29bf10835333d25382e59d5fbe086cfb32e"
  license "MIT"

  depends_on "python"  # Use the latest Python version

  def install
    libexec.install "oiv2cq", "requirements.txt", "setup.py"

    # Dynamically resolve Python path
    python_path = "#{Formula["python"].opt_bin}/python3"

    # Create a wrapper script for the CLI
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
