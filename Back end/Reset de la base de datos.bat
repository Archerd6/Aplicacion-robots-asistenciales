REM Borrado y Creacion de la base de datos

cd instance

del test.db

cd ..

python3 Creacion_de_la_base_de_datos.py %*

start "" "Reset de la base de datos.html"

cls

python app.py

cmd /k