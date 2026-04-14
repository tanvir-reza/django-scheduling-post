#!/bin/bash

set -e

echo "🔄 Updating system..."
sudo apt update

echo "📦 Installing prerequisites..."
sudo apt install -y ca-certificates curl gnupg lsb-release

echo "🔑 Adding Docker GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "📚 Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "🔄 Updating package list..."
sudo apt update

echo "🐳 Installing Docker Engine and Compose plugin..."
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "👤 Adding current user to docker group..."
sudo usermod -aG docker $USER

echo "🚀 Enabling and starting Docker..."
sudo systemctl enable docker
sudo systemctl start docker

echo "✅ Installation complete!"

echo ""
echo "⚠️ IMPORTANT: Log out and log back in (or run 'newgrp docker') to use Docker without sudo."
echo ""
echo "👉 Test with:"
echo "docker --version"
echo "docker compose version"

