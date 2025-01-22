class Oiv2cq < Formula
  desc "CLI to automate onboarding and plugin setup for Twilio's CloudQuery projects"
  homepage "https://github.com/markgraziano-twlo/homebrew-oiv2cq"
  url "https://github.com/markgraziano-twlo/homebrew-oiv2cq/releases/download/v1.0.0/oiv2cq-v1.0.0.tar.gz"
  sha256 "eb86caf46aec48747da028465d61f79a20ededbb39d19831f41b3bf36f15ab14"
  license "MIT"

  depends_on "python"

  def install
    # Install the oiv2cq directory and supporting files
    libexec.install "oiv2cq", "requirements.txt", "setup.py"

    # Install Python dependencies into libexec
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
