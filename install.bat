@echo off
echo 🚀 Installing EduSat AI Dependencies...
echo.

echo 1. Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo 2. Installing core packages...
pip install numpy pandas scikit-learn matplotlib seaborn

echo.
echo 3. Installing web packages...
pip install streamlit plotly openpyxl pillow joblib

echo.
echo 4. Installing optional packages...
pip install fastapi uvicorn xlsxwriter

echo.
echo ✅ Installation complete!
pause
