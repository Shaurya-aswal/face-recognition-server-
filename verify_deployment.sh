#!/bin/bash
# Final deployment verification script

echo "🚀 Final Deployment Verification"
echo "================================="

# Check Python version consistency
echo "🐍 Python Version Check:"
echo "  .python-version: $(cat .python-version)"
echo "  runtime.txt: $(cat runtime.txt)"
echo "  railway.toml: $(grep pythonVersion railway.toml)"

# Check required files
echo -e "\n📁 Required Files:"
required_files=(
    "server.py"
    "util.py" 
    "wavelet.py"
    "requirements.txt"
    "railway.toml"
    "nixpacks.toml"
    "Procfile"
    "runtime.txt"
    ".python-version"
    "artifacts/class_dictionary.json"
    "artifacts/saved_model_.pkl"
)

all_present=true
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING!"
        all_present=false
    fi
done

# Check for unnecessary files
echo -e "\n🗑️ Cleanup Check:"
unnecessary_files=("__pycache__" "*.pyc" "test_*.py" "wsgi.py" "start.py" "deploy_checklist.sh")
for pattern in "${unnecessary_files[@]}"; do
    if ls $pattern 2>/dev/null; then
        echo "  ⚠️ Found unnecessary files: $pattern"
    else
        echo "  ✅ No $pattern files found"
    fi
done

if $all_present; then
    echo -e "\n🎉 ALL CHECKS PASSED! Ready for Railway deployment!"
    echo -e "\n📋 Next Steps:"
    echo "  1. git add ."
    echo "  2. git commit -m 'Final deployment configuration - Python 3.10.12'"
    echo "  3. git push origin main"
    echo "  4. Check Railway deployment logs"
else
    echo -e "\n❌ Some files are missing. Please fix before deployment."
fi
