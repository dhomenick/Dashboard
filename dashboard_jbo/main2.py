import pandas as pd
from pathlib import Path
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb

# Criando o DataFrame a partir do Excel
data = pd.read_excel('/home/homenick/Projetos/dashboard_jbo/vias do municipio jabaotão.xlsx', sheet_name='vias do municipio jabaotão')

# Manipulando dados
total_pavimentadas = data.loc[data['PAVIMENTO'] == 1, 'PAVIMENTO'].sum()
total_naoPavimentadas = data.loc[data['PAVIMENTO'] == 5, 'PAVIMENTO'].sum()

data["PAVIMENTO"] = data["PAVIMENTO"].replace({1: "não_pavimentada", 5: "pavimentada"})
contagem_pavimento = data.groupby(['BAIRRO', 'PAVIMENTO']).size().unstack(fill_value=0).reset_index()

# Adicionando filtros
bairro = list(data["BAIRRO"].unique())
pavimento = list(data["PAVIMENTO"].unique())

def on_filter(state):
    if len(state.bairro) == 0:
        notify(state, "Error", "No results found. Check the filters.")
        return
    state.contagem_pavimento = filter(state.bairro)

def filter(bairros):
    data_filtered = contagem_pavimento[contagem_pavimento['BAIRRO'].isin(bairros)]
    return data_filtered

# Criando a Página
with tgb.Page() as page:
    tgb.text("🗺️ Vias Jaboatão dos Guarapes", class_name="h1")
    
    with tgb.layout('1 1 1'):
        with tgb.part():
            tgb.text("## Total de vias em metro linear", mode="md")
            tgb.text("{:,.2f} m".format(data['COMPRIMENT'].sum()).replace(',', ' ').replace('.', ','), class_name="h4")
        with tgb.part():
            tgb.text("## Total de vias Pavimentadas", mode="md")
            tgb.text("{:,.0f}".format(total_pavimentadas).replace(',', ' ').replace('.', ','), class_name="h4")
        with tgb.part():
            tgb.text("## Total de vias Não Pavimentadas", mode="md")
            tgb.text("{:,.0f}".format(total_naoPavimentadas).replace(',', ' ').replace('.', ','), class_name="h4")
    
    with tgb.layout('1 '):
        tgb.selector(
            value="{bairro}",
            lov=bairro,
            dropdown=True,
            multiple=True,
            label="Escolha o Bairro",
            class_name="fullwidth",
            on_change=on_filter,
        )
       
        

    with tgb.layout('2 1'):
        tgb.chart(
            "{contagem_pavimento}", 
            type="bar", 
            x="BAIRRO", 
            y__1="pavimentada", 
            y__2="não_pavimentada"
        )
        tgb.image(
            "{content}", 
            label="This is an image", 
            
            )
        
# Lançando o webapp
if __name__ == "__main__":
    Gui(page).run(
        title="Vias Dashboard",
        use_reloader=True,
        debug=True,
    )
