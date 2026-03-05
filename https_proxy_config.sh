#!/bin/bash
# HTTPS Proxy configuration for market data sources
export http_proxy="http://106.13.244.171:7890"
export https_proxy="http://106.13.244.171:7890"
export HTTP_PROXY="http://106.13.244.171:7890"
export HTTPS_PROXY="http://106.13.244.171:7890"

# Configure curl to use proxy with HTTPS
alias curl='curl --proxy http://106.13.244.171:7890 --proxy-ssl'

# Test HTTPS connectivity
echo "Testing HTTPS proxy connectivity..."
curl -s "https://www.google.com" > /dev/null && echo "✅ HTTPS Proxy working" || echo "❌ HTTPS Proxy not working"