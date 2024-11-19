import geopandas as gpd
import matplotlib.pyplot as plt

# Carregar os shapefiles
gdf1 = gpd.read_file('/home/homenick/Projetos/dashboard_jbo/vias_jbo/vias_nao_pavimentadas/vias não pavimentadas.shp')
gdf2 = gpd.read_file('/home/homenick/Projetos/dashboard_jbo/vias_jbo/vias_pavimentadas/vias pavimentadas.shp')

# Criar o gráfico com fundo transparente
fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')  # Define o fundo da figura como transparente

# Plotar os dados
gdf1.plot(ax=ax, color='orange', label='Vias não pavimentadas')
gdf2.plot(ax=ax, color='blue', label='Vias Pavimentadas')

# Configurações do gráfico
plt.legend()
plt.title('Mapa jbo')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Remover a cor de fundo do eixo
ax.set_facecolor('none')  # Define o fundo do eixo como transparente
ax.set_xticks([])  # Remove os ticks do eixo x
ax.set_yticks([])  # Remove os ticks do eixo y

# Mostrar o gráfico
plt.show()
