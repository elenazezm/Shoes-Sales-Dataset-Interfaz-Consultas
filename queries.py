import pandas as pd

CSV_PATH = "data/shoes_sales_dataset.csv"

def cargar_datos():
    df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
    return df

# ── 1. Top 5 marcas por ingreso total ──────────────────────────────────────
def q1_top_marcas_ingreso():
    df = cargar_datos()
    resultado = (
        df.groupby("Brand")["Revenue_USD"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue_USD": "Ingreso_Total_USD"})
        .sort_values("Ingreso_Total_USD", ascending=False)
        .head(5)
        .round(2)
    )
    justificacion = (
        "Identifica las 5 marcas que generan mayor ingreso total. "
        "Permite priorizar inventario y negociación con proveedores clave."
    )
    return resultado, justificacion

# ── 2. Ingreso promedio por canal de ventas ────────────────────────────────
def q2_ingreso_por_canal():
    df = cargar_datos()
    resultado = (
        df.groupby("Sales_Channel")
        .agg(
            Ventas=("Units_Sold", "sum"),
            Ingreso_Promedio_USD=("Revenue_USD", "mean"),
            Ingreso_Total_USD=("Revenue_USD", "sum"),
        )
        .reset_index()
        .round(2)
    )
    justificacion = (
        "Compara canales de venta (Online, Mall, etc.) en volumen e ingreso. "
        "Apoya decisiones de inversión en marketing por canal."
    )
    return resultado, justificacion

# ── 3. Tipo de zapato más vendido por país ─────────────────────────────────
def q3_tipo_por_pais():
    df = cargar_datos()
    idx = df.groupby(["Country", "Shoe_Type"])["Units_Sold"].sum()
    resultado = (
        idx.reset_index()
        .sort_values(["Country", "Units_Sold"], ascending=[True, False])
        .groupby("Country")
        .first()
        .reset_index()
        .rename(columns={"Shoe_Type": "Tipo_Más_Vendido", "Units_Sold": "Unidades"})
    )
    justificacion = (
        "Revela qué tipo de calzado domina en cada mercado geográfico. "
        "Útil para personalizar catálogos por región."
    )
    return resultado, justificacion

# ── 4. Tendencia mensual de ingresos ──────────────────────────────────────
def q4_tendencia_mensual():
    df = cargar_datos()
    df["Mes"] = df["Date"].dt.to_period("M").astype(str)
    resultado = (
        df.groupby("Mes")
        .agg(Ingreso_Total=("Revenue_USD", "sum"), Transacciones=("Sale_ID", "count"))
        .reset_index()
        .sort_values("Mes")
        .round(2)
    )
    justificacion = (
        "Muestra la evolución mensual de ingresos y número de transacciones. "
        "Detecta estacionalidad y picos de demanda para planificar stock."
    )
    return resultado, justificacion

# ── 5. Precio promedio y margen por marca ─────────────────────────────────
def q5_precio_promedio_marca():
    df = cargar_datos()
    resultado = (
        df.groupby("Brand")
        .agg(
            Precio_Promedio=("Price_USD", "mean"),
            Unidades_Totales=("Units_Sold", "sum"),
            Ingreso_Total=("Revenue_USD", "sum"),
        )
        .reset_index()
        .sort_values("Precio_Promedio", ascending=False)
        .round(2)
    )
    justificacion = (
        "Analiza el precio promedio de cada marca y su volumen de ventas. "
        "Detecta si marcas premium realmente generan más ingreso total."
    )
    return resultado, justificacion

# ── 6. Color más popular por tipo de zapato ───────────────────────────────
def q6_color_por_tipo():
    df = cargar_datos()
    resultado = (
        df.groupby(["Shoe_Type", "Color"])["Units_Sold"]
        .sum()
        .reset_index()
        .sort_values(["Shoe_Type", "Units_Sold"], ascending=[True, False])
        .groupby("Shoe_Type")
        .head(3)
        .reset_index(drop=True)
        .rename(columns={"Units_Sold": "Unidades_Vendidas"})
    )
    justificacion = (
        "Top 3 colores más vendidos por categoría de calzado. "
        "Guía decisiones de producción y compra de inventario."
    )
    return resultado, justificacion

# ── 7. País con mayor ticket promedio ─────────────────────────────────────
def q7_ticket_promedio_pais():
    df = cargar_datos()
    resultado = (
        df.groupby("Country")
        .agg(
            Ticket_Promedio=("Revenue_USD", "mean"),
            Total_Ventas=("Sale_ID", "count"),
            Ingreso_Total=("Revenue_USD", "sum"),
        )
        .reset_index()
        .sort_values("Ticket_Promedio", ascending=False)
        .round(2)
    )
    justificacion = (
        "Calcula el gasto promedio por transacción en cada país. "
        "Identifica mercados premium para campañas de alto valor."
    )
    return resultado, justificacion

# ── 8. Ranking de marcas por unidades vendidas en canal Online ─────────────
def q8_marcas_online():
    df = cargar_datos()
    resultado = (
        df[df["Sales_Channel"] == "Online"]
        .groupby("Brand")
        .agg(Unidades=("Units_Sold", "sum"), Ingreso=("Revenue_USD", "sum"))
        .reset_index()
        .sort_values("Unidades", ascending=False)
        .round(2)
    )
    justificacion = (
        "Ranking exclusivo del canal Online por unidades vendidas. "
        "Permite optimizar SEO, publicidad digital y catálogo e-commerce."
    )
    return resultado, justificacion

# ── 9. Ventas por trimestre y canal ───────────────────────────────────────
def q9_ventas_trimestre_canal():
    df = cargar_datos()
    df["Trimestre"] = df["Date"].dt.to_period("Q").astype(str)
    resultado = (
        df.groupby(["Trimestre", "Sales_Channel"])
        .agg(Ingreso=("Revenue_USD", "sum"), Unidades=("Units_Sold", "sum"))
        .reset_index()
        .sort_values(["Trimestre", "Ingreso"], ascending=[True, False])
        .round(2)
    )
    justificacion = (
        "Tabla cruzada trimestre × canal de ventas. "
        "Identifica qué canal domina en cada temporada del año."
    )
    return resultado, justificacion

# ── 10. Top 10 días con mayor ingreso ─────────────────────────────────────
def q10_top_dias():
    df = cargar_datos()
    resultado = (
        df.groupby("Date")
        .agg(Ingreso_Dia=("Revenue_USD", "sum"), Transacciones=("Sale_ID", "count"))
        .reset_index()
        .sort_values("Ingreso_Dia", ascending=False)
        .head(10)
        .reset_index(drop=True)
        .round(2)
    )
    resultado["Date"] = resultado["Date"].dt.strftime("%Y-%m-%d")
    justificacion = (
        "Top 10 días con mayor ingreso de ventas. "
        "Detecta fechas clave (promociones, eventos) para replicar estrategias."
    )
    return resultado, justificacion


CONSULTAS = {
    "1. Top 5 Marcas por Ingreso":       q1_top_marcas_ingreso,
    "2. Ingreso por Canal de Venta":     q2_ingreso_por_canal,
    "3. Tipo de Zapato por País":        q3_tipo_por_pais,
    "4. Tendencia Mensual de Ingresos":  q4_tendencia_mensual,
    "5. Precio Promedio por Marca":      q5_precio_promedio_marca,
    "6. Color Popular por Tipo":         q6_color_por_tipo,
    "7. Ticket Promedio por País":       q7_ticket_promedio_pais,
    "8. Marcas Líderes Online":          q8_marcas_online,
    "9. Ventas Trimestre × Canal":       q9_ventas_trimestre_canal,
    "10. Top 10 Días de Mayor Ingreso":  q10_top_dias,
}
