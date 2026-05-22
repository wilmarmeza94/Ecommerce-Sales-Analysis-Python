import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. CARGA DE DATOS MASIVOS
# ==========================================
try:
    # Leemos el archivo CSV con las 1,500 filas de venta
    df = pd.read_csv('datos_ventas_ecommerce.csv')
    print(f"✅ Archivo cargado con éxito. Total de filas a procesar: {len(df)}")
except FileNotFoundError:
    print("❌ Error: No se encontró el archivo 'datos_ventas_ecommerce.csv' en la misma carpeta.")
    exit()

# Ver una muestra inicial en la consola de VS Code
print("\n👀 Primeras 5 filas del archivo original:")
print(df.head())
print("-" * 60)

# ==========================================
# 2. LIMPIEZA DE DATOS (Data Cleaning)
# ==========================================
print("🧹 Iniciando proceso automatizado de limpieza...")

# A. Limpiar columna de precios: Quitar el símbolo '$' y convertirlo a número decimal
df['Precio_Unitario'] = df['Precio_Unitario'].str.replace('$', '', regex=False).astype(float)

# B. Tratamiento de valores nulos (Filas dañadas o vacías)
# Contamos cuántos nulos hay antes de limpiar
nulos_cantidad = df['Cantidad'].isnull().sum()
nulos_fecha = df['Fecha'].isnull().sum()

# Si faltan cantidades, asumimos por regla de negocio que se compró mínimo 1 producto
df['Cantidad'] = df['Cantidad'].fillna(1)

# Si falta la fecha, eliminamos el registro porque no sirve para análisis temporal
df = df.dropna(subset=['Fecha'])

# C. Convertir la fecha al formato correcto de fechas en Python
df['Fecha'] = pd.to_datetime(df['Fecha'])

# D. Crear la métrica clave de negocio: Total de Ventas por fila
df['Total_Ventas'] = df['Cantidad'] * df['Precio_Unitario']

print(f"   -> Se corrigieron {nulos_cantidad} registros con cantidad vacía.")
print(f"   -> Se eliminaron {nulos_fecha} registros críticos sin fecha.")
print("✅ Limpieza completada.")
print("-" * 60)

# ==========================================
# 3. ANÁLISIS EXPERTOS DE NEGOCIO (Insights)
# ==========================================
print("📊 Generando métricas clave para la gerencia...")

ingreso_total = df['Total_Ventas'].sum()
productos_mas_vendidos = df.groupby('Producto')['Cantidad'].sum().sort_values(ascending=False)
ciudades_top = df.groupby('Ciudad')['Total_Ventas'].sum().sort_values(ascending=False)

print(f"\n💰 INGRESOS TOTALES DEL PERIODO: ${ingreso_total:,.2f}")
print("\n📦 VOLUMEN DE PRODUCTOS VENDIDOS (Top):")
print(productos_mas_vendidos)
print("\n📍 CIUDADES POR VOLUMEN DE FACTURACIÓN:")
print(ciudades_top)
print("-" * 60)

# ==========================================
# 4. VISUALIZACIÓN EJECUTIVA (Gráficos)
# ==========================================
print("📈 Diseñando gráficos ejecutivos...")

# Configuración visual limpia
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Ventas por Ciudad
sns.barplot(ax=axes[0], x=ciudades_top.values, y=ciudades_top.index, palette="Dark2")
axes[0].set_title("Facturación Total por Ciudad ($)", fontsize=13, fontweight='bold')
axes[0].set_xlabel("Ventas ($)")

# Gráfico 2: Productos más vendidos (Volumen)
sns.barplot(ax=axes[1], x=productos_mas_vendidos.values, y=productos_mas_vendidos.index, palette="Blues_r")
axes[1].set_title("Unidades Totales Vendidas por Producto", fontsize=13, fontweight='bold')
axes[1].set_xlabel("Cantidad Vendida")

# Ajustar y Guardar de manera automática para el portafolio
plt.tight_layout()
plt.savefig("reporte_rendimiento_ecommerce.png", dpi=300)
print("💾 ¡Gráfico guardado automáticamente como 'reporte_rendimiento_ecommerce.png'!")

# Mostrar en pantalla
plt.show()