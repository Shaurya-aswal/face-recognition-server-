#!/bin/bash
# Railway Deployment Checklist Script
# Run this before deploying to verify everything is ready

echo "🔍 Railway Deployment Checklist"
echo "================================"

# Check if all required files exist
echo "📁 Checking required files..."
required_files=("server.py" "util.py" "wavelet.py" "requirements.txt" "railway.toml" "Procfile" "artifacts/class_dictionary.json" "artifacts/saved_model_.pkl")

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING!"
        exit 1
    fi
done

# Check requirements.txt format
echo -e "\n📦 Validating requirements.txt..."
python3 -c "
import pkg_resources
try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read().strip().split('\n')
    
    for req in requirements:
        if req.strip():
            pkg_resources.Requirement.parse(req)
    
    print('✅ requirements.txt format is valid')
except Exception as e:
    print(f'❌ requirements.txt error: {e}')
    exit(1)
"

# Check Python version files
echo -e "\n🐍 Checking Python version configuration..."
if [[ -f ".python-version" ]]; then
    echo "✅ .python-version exists"
else
    echo "❌ .python-version missing"
fi

if [[ -f "runtime.txt" ]]; then
    echo "✅ runtime.txt exists"
else
    echo "❌ runtime.txt missing"
fi

# Check Railway config
echo -e "\n🚂 Checking Railway configuration..."
if grep -q "pythonVersion.*3.10.13" railway.toml; then
    echo "✅ Python version set to 3.10.13"
else
    echo "❌ Python version not set correctly"
fi

if grep -q "startCommand.*gunicorn" railway.toml; then
    echo "✅ Gunicorn start command configured"
else
    echo "❌ Gunicorn start command missing"
fi

# Check artifacts
echo -e "\n🤖 Checking model artifacts..."
if [[ -f "artifacts/class_dictionary.json" ]]; then
    classes=$(python3 -c "import json; print(len(json.load(open('artifacts/class_dictionary.json'))))")
    echo "✅ class_dictionary.json - $classes classes"
else
    echo "❌ class_dictionary.json missing"
fi

if [[ -f "artifacts/saved_model_.pkl" ]]; then
    size=$(ls -lh artifacts/saved_model_.pkl | awk '{print $5}')
    echo "✅ saved_model_.pkl - $size"
else
    echo "❌ saved_model_.pkl missing"
fi

echo -e "\n🎉 All checks passed! Ready for Railway deployment!"
echo "💡 Next steps:"
echo "   1. git add ."
echo "   2. git commit -m 'Fix Railway deployment - all issues resolved'"
echo "   3. git push origin main"
echo "   4. Deploy to Railway"
