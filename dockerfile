# Use an official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package repository and install common utilities
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    software-properties-common \
    libgtk-3-dev \
    libwebkit2gtk-4.0-dev \
    upx \
    nsis \
    && apt-get clean

# Install Go 1.20+
RUN wget https://go.dev/dl/go1.20.7.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.20.7.linux-amd64.tar.gz && \
    rm go1.20.7.linux-amd64.tar.gz

# Add Go to the PATH
ENV PATH="/usr/local/go/bin:${PATH}"

# Install Node.js 16+ and NPM
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

# Verify installations
RUN go version && node -v && npm -v && upx --version && makensis -VERSION

# Set the working directory
WORKDIR /app

# Entry point (optional) – this can be changed as per your application needs
CMD ["/bin/bash"]
