#!/bin/bash
# Proxy configuration for market data sources
export http_proxy="http://106.13.244.171:7890"
export https_proxy="http://106.13.244.171:7890"
export HTTP_PROXY="http://106.13.244.171:7890"
export HTTPS_PROXY="http://106.13.244.171:7890"

# Test proxy connectivity
echo "Testing proxy connectivity..."
curl -s --proxy $http_proxy "https://www.google.com" > /dev/null && echo "✅ Proxy working" || echo "❌ Proxy not working"