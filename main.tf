# main.tf - FIXED VERSION
provider "aws" {
  region = "us-east-1"
}

# Create a more specific security group
resource "aws_security_group" "scanner_sg" {
  name        = "verit-scanner-sg"
  description = "Security group for Verit scam scanner app"

  ingress {
    description = "HTTP for Flask app"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP for future web server"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "verit-scanner"
  }
}

# Get the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}

# Create the EC2 instance with SIMPLIFIED setup
resource "aws_instance" "verit_app" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = "t2.micro"  # Use micro for testing (free tier)
  vpc_security_group_ids = [aws_security_group.scanner_sg.id]
  
  # REMOVED: key_name (we'll add it back later)
  # REMOVED: iam_instance_profile (not needed for basic deployment)
  
  # Simple storage configuration
  root_block_device {
    volume_size = 8  # GB - smaller for testing
    volume_type = "gp2"
  }

  # SIMPLIFIED user_data - just get a basic app running first
  user_data = <<-EOF
              #!/bin/bash
              # Update system
              yum update -y
              
              # Install dependencies
              yum install -y python3 python3-pip git

              # Create application directory
              mkdir -p /opt/verit
              cd /opt/verit

              # Create a SIMPLE test app.py first
              cat > app.py << 'PYTHON_EOF'
from flask import Flask, render_template
import requests
import base64
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head><title>Verit - Scam Scanner</title></head>
        <body>
            <h1>🚀 Verit is Deployed on AWS!</h1>
            <p>Your Flask application is successfully running on EC2</p>
            <p>Next: Deploy the full scam detection functionality</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
              PYTHON_EOF

              # Create templates directory
              mkdir -p templates
              
              # Create simple index.html
              cat > templates/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Verit - Test Page</title>
</head>
<body>
    <h1>✅ Verit Template Works!</h1>
    <p>Flask templates are loading correctly</p>
</body>
</html>
              HTML_EOF

              # Install only Flask for now
              pip3 install flask

              # Start the application
              cd /opt/verit
              nohup python3 app.py > /var/log/verit.log 2>&1 &

              echo "Verit basic deployment complete!"
              echo "App running on http://localhost:5000"
              EOF

  tags = {
    Name = "Verit-Scanner-Test"
    Project = "Verit"
  }
}

# Output the public URL
output "application_url" {
  description = "Public URL of your Verit application"
  value       = "http://${aws_instance.verit_app.public_ip}:5000"
}

output "instance_ip" {
  description = "Public IP address"
  value       = aws_instance.verit_app.public_ip
}

output "ssh_connection" {
  description = "SSH connection command"
  value       = "ssh ec2-user@${aws_instance.verit_app.public_ip}"
}