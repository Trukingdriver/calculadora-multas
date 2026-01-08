from datetime import datetime
from flask import Flask, render_template, request
import os

app = Flask(__name__)

def calcular_multa(limite, velocidad, tipo_radar):
    # Aplicar margen de error legal de la DGT
    if velocidad <= 100:
        # Margen fijo: 5km/h para fijo, 7km/h para móvil
        margen = 5 if tipo_radar == "fijo" else 7
    else:
        # Margen porcentual: 5% para fijo, 7% para móvil
        margen = velocidad * (0.05 if tipo_radar == "fijo" else 0.07)
    
    velocidad_final = velocidad - margen
    exceso = velocidad_final - limite

    if exceso <= 0:
        return 0, 0, "Sin sanción (dentro del margen)", 0, velocidad_final

    # Lógica de sanciones
    if exceso <= 20:
        multa, puntos, desc = 100, 0, "Infracción Leve"
    elif exceso <= 30:
        multa, puntos, desc = 300, 2, "Infracción Grave"
    elif exceso <= 40:
        multa, puntos, desc = 400, 4, "Infracción Grave"
    elif exceso <= 50:
        multa, puntos, desc = 500, 6, "Infracción Muy Grave"
    else:
        multa, puntos, desc = 600, 6, "Muy Grave (Posible Delito)"

    return multa, puntos, desc, multa * 0.5, velocidad_final

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        try:
            limite = int(request.form["limite"])
            velocidad = int(request.form["velocidad"])
            tipo_radar = request.form["tipo_radar"]
            
            multa, puntos, desc, pronto, vel_real = calcular_multa(limite, velocidad, tipo_radar)
            
            resultado = {
                "limite": limite,
                "velocidad": velocidad,
                "vel_real": round(vel_real, 2),
                "multa": multa,
                "puntos": puntos,
                "descripcion": desc,
                "pronto_pago": pronto
            }

            # Registro de uso en uso.txt
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            con_datos = f"[{ahora}] Radar: {tipo_radar} | Limite: {limite} | Medido: {velocidad} | Real: {round(vel_real, 2)} | Multa: {multa}€\n"
            with open("uso.txt", "a", encoding="utf-8") as f:
                f.write(con_datos)
        except Exception as e:
            print(f"Error: {e}")

    return render_template("index.html", resultado=resultado)

@app.route("/normativa")
def normativa():
    return render_template("normativa.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
