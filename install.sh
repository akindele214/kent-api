echo "Creating a virtual environment"
python -m venv env
echo

echo "Activating virtual environment"
source env/Scripts/activate
./env/Scripts/activate

echo "Installing dependencies"
pip install -r requirements.txt

echo "Setting Up Database"
python manage.py migrate

echo "Press ANY KEY to end"
read