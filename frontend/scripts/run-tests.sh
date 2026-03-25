#!/bin/bash

# Frontend test runner script
# Usage: bash run-tests.sh [unit|integration|e2e|coverage|watch|ui]

set -e

TEST_TYPE=${1:-unit}

echo "🧪 Running frontend tests..."

# Install dependencies if not already installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    pnpm install
fi

case $TEST_TYPE in
    "unit")
        echo "🔬 Running unit tests only..."
        pnpm test tests/components/ tests/lib/ --reporter=verbose
        ;;
    "integration")
        echo "🔗 Running integration tests only..."
        pnpm test tests/integration/ --reporter=verbose
        ;;
    "e2e")
        echo "🌐 Running E2E tests..."
        pnpm test:e2e
        ;;
    "coverage")
        echo "📊 Running tests with coverage report..."
        pnpm test:coverage
        echo "📈 Coverage report generated in coverage/index.html"
        ;;
    "watch")
        echo "👀 Running tests in watch mode..."
        pnpm test:watch
        ;;
    "ui")
        echo "🎨 Running tests with UI..."
        pnpm test:ui
        ;;
    "all")
        echo "🚀 Running all tests..."
        echo "Unit tests..."
        pnpm test tests/components/ tests/lib/
        echo "Integration tests..."
        pnpm test tests/integration/
        echo "E2E tests..."
        pnpm test:e2e
        ;;
    "fast")
        echo "⚡ Running fast unit tests only..."
        pnpm test tests/components/ tests/lib/ --run --reporter=basic
        ;;
    *)
        echo "❌ Invalid test type. Use: unit, integration, e2e, coverage, watch, ui, all, fast"
        exit 1
        ;;
esac

echo "✅ Tests completed!"
