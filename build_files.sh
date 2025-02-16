# build_files.sh

# Install pip if not available
if ! command -v pip &> /dev/null; then
    echo "Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
fi

echo "INSTALLING REQUIREMENTS....."

pip install -r requirements.txt

echo "Done..."

python3.12 manage.py collectstatic --noinput
