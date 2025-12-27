from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_multa(limite, velocidad):
    exceso = velocidad - limite
    if exceso <= 0:
        return 0, 0, "No hay multa. ¡Todo correcto!", 0

    if exceso <= 20:
        multa = 100
        puntos = 0
        descripcion = "Infracción leve"
    elif exceso <= 30:
        multa = 300
        puntos = 2
        descripcion = "Infracción grave"
    elif exceso <= 40:
        multa = 400
        puntos = 4
        descripcion = "Infracción grave"
    elif exceso <= 50:
        multa = 500
        puntos = 6
        descripcion = "Infracción muy grave"
    else:
        multa = 600
        puntos = 6
        descripcion = "Muy grave (posible delito)"

    pronto_pago = multa * 0.5
    return multa, puntos, descripcion, pronto_pago

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        limite = int(request.form["limite"])
        velocidad = int(request.form["velocidad"])
        multa, puntos, descripcion, pronto_pago = calcular_multa(limite, velocidad)
        
        resultado = {
            "limite": limite,
            "velocidad": velocidad,
            "exceso": velocidad - limite,
            "multa": multa,
            "puntos": puntos,
            "descripcion": descripcion,
            "pronto_pago": pronto_pago
        }
        
        try:
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            con_datos = f"[{ahora}] Limite: {limite} | Medido: {velocidad} | Multa: {multa}€\n"
            with open("uso.txt", "a", encoding="utf-8") as f:
                f.write(con_datos)
        except Exception as e:
            print(f"Error al escribir en el registro: {e}"

                  
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)
