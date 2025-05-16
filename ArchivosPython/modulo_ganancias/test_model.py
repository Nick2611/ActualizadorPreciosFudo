import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot as plt

# Cargar datos

"""
    Utilizo la libreria de analisis de datos pandas para cargar el archivo CSV que contiene la cantidad de ventas
    y el ticket promedio de un restaurante en los ultimos 4 meses.
"""
df = pd.read_csv("../restaurant_sales_4_months.csv")
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

# Parámetro: cuántos días vas a usar como input
"""
    Defino la variable DAYS_INPUT que contiene la cantidad de días que voy a usar como input para el modelo, para
    que sea capaz de predecir el mes entero con solo una porcion de los datos.
"""

DAYS_INPUT = 11

# Crear X e y por mes, siendo X los datos de ventas y ticket promedio de los días e Y el total de ventas del mes
samples = []
targets = []

for month in df["month"].unique(): #Recorro todos los meses únicos en el dataframe
    month_data = df[df["month"] == month].reset_index(drop=True) #Creo el dataframe del mes, sin resetear el índice por cada iteracion
    if len(month_data) >= DAYS_INPUT: #Si el mes tiene más días que DAYS_INPUT
        row = []
        for i in range(DAYS_INPUT):
            row.extend([
                month_data.loc[i, "sales"],
                month_data.loc[i, "avg_ticket"],
            ]) #Agrego los datos de ventas y ticket promedio de los días a la fila
        samples.append(row) #añado la fila a la lista de muestras
        targets.append(month_data["revenue"].sum()) #Suma el total de ventas del mes y lo añado a la lista de targets

X = pd.DataFrame(samples) #Creo el dataframe de las muestras (la tabla)
y = pd.Series(targets) #Creo la serie de los targets (la columna)

# Entrenar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #Divido los datos de entrenamiento y prueba
model = RandomForestRegressor(random_state=42) #Utilizamos el modelo de ML RandomForestRegressor
model.fit(X_train, y_train) #Entrenamos al modelo con la data

# Evaluar
y_pred = model.predict(X_test) #Predecimos los datos de prueba

print(y_pred) #Prediccion del mes
print(targets[0]) #Valor actual del total de ventas del mes
mae = mean_absolute_error(y_test, y_pred) #Error absoluto medio para evaluar el modelo
print(mae)



"""
    Plot del grafico de ventas reales usando matplotlib, utilizando la informacion del dataframe previamente generado
    para visualizar la informacion y porcentaje de error real del modelo.
"""

# Ejemplo: enero 2024
enero = df[df["month"] == "2024-01"].sort_values("date").reset_index(drop=True)

subset = enero.iloc[:DAYS_INPUT]

plt.plot(subset["date"], subset["sales"], marker="o")
plt.title("Ventas - Enero (primeros días)")
plt.xticks(rotation=20)
plt.show()

total_enero = enero["revenue"].sum()
print("MAE:", mae)
print("Total enero:", total_enero)
print("Error relativo (%):", (mae / total_enero) * 100)



