from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 barras porque es un path relativo. Si fuera absoluto, serían 4 barras
with app.app_context():
    db = SQLAlchemy(app)

class Todo(db.Model): #Tabla para tareas creadas
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(200))        # prioridad
    descripcion = db.Column(db.String(200))             # Descripcion
    atributos = db.Column(db.String(800))               # Atributos

class Robo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)

class InstanciaTarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    priority = db.Column(db.String(200))       # prioridad
    atributos_asignados = db.Column(db.String(800))



@app.route('/test', methods=['POST', 'GET']) ## Indica qué hacer cuando un usuario llega a la pagina principal
def test():
    task_content = "Test"
    new_task = Todo(content=task_content)

    try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
    except:
            return "Problem while insereting in the DB"

    return render_template('index.html') # Renderizar index.html
    

@app.route('/', methods=['POST', 'GET']) ## Indica qué hacer cuando un usuario llega a la pagina principal
def index():
    
    return render_template('index.html') # Renderizar index.html

@app.route('/index.html', methods=['POST', 'GET'])
def index_alt():
    return render_template('index.html') # Renderizar index.html
    # task_content = "Test"
    # new_task = Todo(content=task_content)

    # try:
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/')
        
    # except:
    #         return "Problem while insereting in the DB"

#---------------------------------------------------------------------------------------------------------#

@app.route('/Interfaz_tecnico.html', methods=['POST','GET'])     # Redireccion a Tecnico
def tecnico():
    tasks = Todo.query.order_by(Todo.id).all() # Este método nos devuelve todos los elementos de la tabla de la base de datos
    rob = Robo.query.order_by(Robo.id).all()
    return render_template('Interfaz_tecnico.html', tasks=tasks, rob=rob) # Presentar las tareas
    # if request.method == 'POST':
    #     task_content = "Prueba de texto"
    #     new_task = Todo(content=task_content)

    #     try:
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/Interfaz_tecnico.html')
        
    #     except:
    #         return "Problem while insereting in the DB"
    # else:
    #     tasks = Todo.query.order_by(Todo.id).all() # Este método nos devuelve todos los elementos de la tabla de la base de datos
    #     return render_template('Interfaz_tecnico.html', tasks=tasks) # Presentar las tareas


@app.route('/delete')
def delete():
    tasks = Todo.query.order_by(Todo.id).all() # Todas las tareas
    id= tasks[-1].id                           # La ultima tarea

    if(id > 1):
        task_to_delete = Todo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/Interfaz_tecnico.html')
        except:
            return "Error while deleting the task" + id
    return redirect('/Interfaz_tecnico.html')

@app.route('/reset')
def reset():
    tasks = Todo.query.order_by(Todo.id).all() # Todas las tareas
    id= tasks[-1].id                           # La ultima tarea

    rob = Robo.query.order_by(Robo.id).all() # Todos los robots
    idr = rob[-1].id 

    if(id > 1):
        for idx in range(2,id+1):
            task_to_delete = Todo.query.get_or_404(idx)
            try:
                db.session.delete(task_to_delete)
                db.session.commit()
            except:
                return "Error while deleting the task" + idx
    
    for idx in range(2,idr+1):
        task_to_delete = Robo.query.get_or_404(idx)
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
        except:
            return "Error while deleting the task" + idx

    return redirect('/Interfaz_tecnico.html')


@app.route('/resetEncargado')
def resetEncargado():
    tasks = Todo.query.order_by(Todo.id).all() # Todas las tareas
    id= tasks[-1].id                           # La ultima tarea

    it = InstanciaTarea.query.order_by(InstanciaTarea.id).all() # Todos los robots
    idr = it[-1].id 

    if(id > 1):
        for idx in range(2,id+1):
            task_to_delete = Todo.query.get_or_404(idx)
            try:
                db.session.delete(task_to_delete)
                db.session.commit()
            except:
                return "Error while deleting the task" + idx
    
    for idx in range(2,idr+1):
        task_to_delete = InstanciaTarea.query.get_or_404(idx)
        try:
            db.session.delete(task_to_delete)
            db.session.commit()
        except:
            return "Error while deleting the task" + idx

    return redirect('/interfaz_encargado.html')


@app.route('/update/<int:id>', methods=['POST','GET'])      # Redireccion a formulario tareas
def update_tarea(id):
        
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            task.content = request.form['nombre']
            task.descripcion = request.form['descripcion']
            task.priority=request.form['prioridad']
            task.atributos = request.form['atributos']
            db.session.commit()
            return redirect('/Interfaz_tecnico.html')
        except:
            return "There was an issue when updating the task " + id
    else:
        return render_template('interfaz_tareas.html', task=task)

@app.route('/new_update/<int:id>', methods=['POST','GET'])      # Redireccion a formulario tareas
def new_tarea(id):
        
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':

        try:
            task_content = request.form['nombre']
            task_descrip = request.form['descripcion']
            task_priority=request.form['prioridad']
            task_atribut = request.form['atributos']
            new_task = Todo(content=task_content, descripcion=task_descrip, priority=task_priority, atributos=task_atribut)
            db.session.add(new_task)
            db.session.commit()
            return redirect('/Interfaz_tecnico.html')
        except:
            return "There was an issue when updating the task " + id
    else:
        return render_template('interfaz_tareas_nueva.html', task=task)
    


@app.route('/interfaz_encargado.html', methods=['POST','GET'])   # Redireccion a Encargado
def encargado():
    tasks = Todo.query.order_by(Todo.id).all() # tareas ordenadas por id
    instancias = InstanciaTarea.query.order_by(InstanciaTarea.priority).all() # instancias de tareas ordenadas por prioridad
    return render_template('interfaz_encargado.html', tasks=tasks, instancias=instancias)

# @app.route('/asignar_tarea.html', methods=['POST','GET'])
# def asignar_tarea():
#      return render_template('asignar_tarea.html')

@app.route('/asignar/<int:id>', methods=['POST','GET'])      # Redireccion a formulario asignar tareas
def asignar(id):
    task = Todo.query.get_or_404(id)

    atributosi = task.atributos

    atributosii = atributosi.split(",")

    if request.method == 'POST':
        # intancias sin los valores de los atributos
        try:
        
            cadena_con_todos_los_atributos = ""

            for i in range(len(atributosii)):
                # Comprobar si el atributo tiene algun valor que sea vacio, para no añadir varios - al final
                if(request.form["atributos"+str(i)]!=""):
                    CampName="atributos"+str(i)
                    if(i!=len(atributosii)-1): # Si no es el ultimo
                        cadena_con_todos_los_atributos = cadena_con_todos_los_atributos + request.form[CampName]  + " - "
                    else: # Si es el ultimo
                        cadena_con_todos_los_atributos = cadena_con_todos_los_atributos + request.form[CampName]
                else:
                    # En este caso tenemos que tocarlo solo si es el ultimo del rango, para que no se quede un - al final borramos
                    if(i==len(atributosii)-1 and cadena_con_todos_los_atributos!=""):# Si es el ultimo y no esta vacio
                        cadena_con_todos_los_atributos = cadena_con_todos_los_atributos[:-2]
                

            task_content = request.form['nombre']
            task_priority=request.form['prioridad']
            
            instancia_tarea = InstanciaTarea(content=task_content, priority=task_priority, atributos_asignados=cadena_con_todos_los_atributos)
            db.session.add(instancia_tarea)
            db.session.commit()
            return redirect('/interfaz_encargado.html')
        except:
            return "Error: no se ha podido asignar la tarea"
    else:
        return render_template('/asignar_tarea.html', task=task, taskinfo=atributosii)



@app.route('/nuevo_robot')
def nuevo_robot():
    rob = Robo.query.order_by(Robo.id).all() # Todos los robots
    
    nombres_de_robots = ["Wally","Radion","NetBot","Roomba","Solac","Roborock"]
    new_rob = Robo(nombre=random.choice(nombres_de_robots))
    try:
        db.session.add(new_rob)
        db.session.commit()
        return redirect('/Interfaz_tecnico.html')
    except:
        return "Problem while insereting in the DB"


@app.route('/delete_robot')
def delete_robot():
    rob = Robo.query.order_by(Robo.id).all() # Todos los robots
    id= rob[-1].id                           # El último robot

    if(id > 1):
        task_to_delete = Robo.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/Interfaz_tecnico.html')
        except:
            return "Error while deleting the task" + id
    return redirect('/Interfaz_tecnico.html')

    # rob_to_delete = Robo.query.get_or_404(id)
    # try:
    #     db.session.delete(id)
    #     db.session.commit()
    #     return redirect('/Interfaz_tecnico.html')
    # except:
    #     return "Error while deleting the task" + id

@app.route('/delete_Asignada/<int:id>') 
def delete_Asignada(id):
    if(id > 0):
        task_to_delete = InstanciaTarea.query.get_or_404(id)

        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            return redirect('/interfaz_encargado.html')
        except:
            return "Error while deleting the task" + id
    return redirect('/interfaz_.html')

if __name__ == "__main__":
    app.run(debug=True)