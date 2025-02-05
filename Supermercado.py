# -*- coding: utf-8 -*-
"""Semana 12

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ag_vmsgKKex3D-C7iuItxYI95Cl5rZct
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, norm

df = pd.read_csv("SuperMarketData.csv")
print(df.head())
print()

sales = np.array(df["Sales"]) * 19.88
print("SALES")
max_sales = max(sales)
min_sales = min(sales)
sales_norm = 1/(max_sales - min_sales) * (sales - min_sales)

a, b, _, _ = beta.fit(sales) #La función beta.fit() regresa 4 valores. Los dos
#guiones bajos son para indicar que el tercer y cuarto valor son basura.
print("Alfa y Beta:")
print(a, b)
print()

mu_xnorm = a / (a+b)
var_xnorm = a * b / ((a+b)**2 * (a+b+1))
sigma_xnorm = np.sqrt(var_xnorm)
print("Promedio, varianza y desviación estándar normal:")
print(mu_xnorm, var_xnorm, sigma_xnorm)
print()

mu = (max_sales - min_sales) * mu_xnorm + min_sales
var = (max_sales - min_sales) ** 2 * var_xnorm
sigma = np.sqrt(var)
print("Promedio, varianza y desviación estándar:")
print(mu, var, sigma)

#---------- Gastos de operación ---------#
#Salarios
dias_t = 24
fact = 1.15

sal_cajeros = 258.25
num_cajeros = 30
total_cajeros = sal_cajeros * num_cajeros * dias_t * fact

sal_conserje = 5000
num_conserjes = 20
total_conserjes = sal_conserje * num_conserjes * fact

total_gerente = 100000

sub_gerente = 45000
num_subgerentes = 4
total_subgerentes = sub_gerente * num_subgerentes

sal_almacenista = 262.13
almacenista = 40
total_almacenista = sal_almacenista * almacenista * dias_t * fact

g_pasillo = 264.65
num_pasillos = 40
total_pasillo = g_pasillo * num_pasillos * dias_t * fact


nomina_total = (total_cajeros + total_conserjes + total_gerente + total_subgerentes + total_almacenista + total_pasillo)
print("Gastos de nómina")
print(nomina_total)
print()

#Gastos de agua
gal_mensuales = 1916500 / 12
gal_am3 = gal_mensuales * 0.00378541
agua_base = 20757.36 + 400.56152 * 102.49
alcantarillado = agua_base * 0.1
tratamiento_agua = agua_base * 0.12
IVA = agua_base * 0.16
gasto_agua = agua_base + alcantarillado + tratamiento_agua +IVA
print("Gastos de agua: ")
print(gasto_agua)
print()


#Gastos de luz
fijo_luz = 362.6
consumo_luz = 2000 * 120 * 12 * 30 #Consumo de luz mensual asumiendo que la duración del mes es de 30 días
cargo_v = consumo_luz * 1.978
demanda_max = 2000 * 120
cargo_d = demanda_max * 383.9
cargo_c = demanda_max * 328.44
gasto_luz = fijo_luz + cargo_v + cargo_d + cargo_c
print("Gastos de luz:")
print(gasto_luz)
print()

#Total
gasto_operacion = nomina_total + gasto_agua + gasto_luz
print("Gastos de operación")
print(gasto_operacion)
print()
ingreso = gasto_operacion + 1500000

omega = norm.ppf(0.01)
a_ = mu ** 2
b_ = -2 * mu * ingreso - omega ** 2 * sigma ** 2
c_ = ingreso ** 2
N1 = (-b_ + np.sqrt(b_ ** 2 - 4 * a_ * c_ )) / (2 * a_)
N2 = (-b_ - np.sqrt(b_ ** 2 - 4 * a_ * c_ )) / (2 * a_)

print(N1, N2)
if (ingreso / N1 - mu > 0):
  N = N1
else:
  N = N2

porc_pob = N / 160000
print(porc_pob)

rating = np.array(df["Rating"])
print("RATINGS:")
max_rat = max(rating)
min_rat = min(rating)
rating_norm = 1/(max_rat - min_rat) * (rating - min_rat)

a_rat, b_rat, _, _ = beta.fit(rating)
print("Alfa y Beta:")
print(a_rat, b_rat)
print()

rat_mu_xnorm = a_rat / (a_rat + b_rat)
rat_var_xnorm = a_rat * b_rat / ((a_rat + b_rat)**2 * (a_rat+b_rat+1))
rat_sigma_xnorm = np.sqrt(rat_var_xnorm)
print("Promedio, varianza y desviación estándar normal:")
print(rat_mu_xnorm, rat_var_xnorm, rat_sigma_xnorm)
print()

rat_mu = (max_rat - min_rat) * rat_mu_xnorm + min_rat
rat_var = (max_rat - min_rat) ** 2 * rat_var_xnorm
rat_sigma = np.sqrt(rat_var)
print("Promedio, varianza y desviación estándar:")
print(rat_mu, rat_var, rat_sigma)

#Para sacar la probabilidad de que en la sucursal que abramos, si los datos que usamos fue en una comunidad semejante a la de Juriquilla, de que en promedio tengan un rating de 8.5 o más
n = 1000
sigma_prom = rat_sigma / np.sqrt(n)
valor_z = (8.5 - rat_mu) / (sigma_prom / np.sqrt(n))
prob = 1 - norm.cdf(valor_z)
print("Probabilidad de que los ratings sean iguales o mayores a 8.5: ")
print(prob)

plt.hist(df["Rating"], bins=10, color = "pink", edgecolor = "black")
plt.title("Distribución de los Ratings")
plt.xlabel("Rating")
plt.ylabel("Frecuencia")
plt.show()
