#!/bin/bash

package_name="flask"

# Comprobar si el paquete está instalado
pip show $package_name 2>/dev/null
if [ $? -eq 0 ]; then
    echo "$package_name is already installed."
else
    echo "Installing $package_name..."
    pip install $package_name
fi


package_name="flask_sqlalchemy"

# Comprobar si el paquete está instalado

pip show $package_name 2>/dev/null
if [ $? -eq 0 ]; then
    echo "$package_name is already installed."
else
    echo "Installing $package_name..."
    pip install $package_name
fi



# Inicio del servidor en sí

cd .env/Scripts

source activate

cd ../..

xdg-open "URL del servidor (localhost).html"

clear

python3.10 app.py
