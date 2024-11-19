import pandas as pd
from pathlib import Path
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb

## Criando o Data frame apartir do excel
data = pd.read_excel('/home/homenick/Projetos/dashboard_jbo/vias do municipio jabaotão.xlsx', sheet_name='vias do municipio jabaotão')
## manipulando dados
total_pavimentadas = data.loc[data['PAVIMENTO'] == 1, 'PAVIMENTO'].sum()
total_naoPavimentadas = data.loc[data['PAVIMENTO'] == 5, 'PAVIMENTO'].sum()

data ["PAVIMENTO"] = data ["PAVIMENTO"].replace({1:"não_pavimentada" ,5: "pavimentada"})

print(data)

contagem_pavimento = data.groupby(['BAIRRO', 'PAVIMENTO']).size().unstack(fill_value=0).reset_index()

print(contagem_pavimento)



## Adicionando filtros

bairro= list(data["BAIRRO"].unique())
pavimento=list(data["PAVIMENTO"].unique())

def on_filter (state):
    if(
        len(state.bairro) == 0
    ):
        notify(state, "Error", "No results found. Check the filters.")
        return
    state.contagem_pavimento = filter(state.bairro)

    def filter(bairro):
        data_filtered = contagem_pavimento[data ["BAIRRO"].isin(bairro)]
        

##print(df.head())
##Criando a Pagina
with tgb.Page() as page:
    ## adicionando os itens da pagina
    tgb.text("🗺️ Vias Jaboatão dos Guarapes", class_name="h1")
    ##layout da pagina
    with tgb.layout('1 1 1'):
            ##tgb.table("{df}")
        with tgb.part():
            tgb.text("## Total de vias em metro linear", mode="md")
            ##tgb.text("{data['COMPRIMENT'].sum()}", class_name="h4")
            ##tgb.text("{:,.2f}".format(data['COMPRIMENT'].sum()), class_name="h4")
            tgb.text("{:,.2f} m".format(data['COMPRIMENT'].sum()).replace(',', ' ').replace('.', ','), class_name="h4")
        with tgb.part():
            tgb.text("## Total de vias Pavimentadas", mode="md")
            tgb.text("{:,.0f}".format(total_pavimentadas).replace(',', ' ').replace('.', ','), class_name="h4")
        with tgb.part():
            tgb.text("## Total de vias Não Pavimentadas", mode="md")
            tgb.text("{:,.0f}".format(total_naoPavimentadas).replace(',', ' ').replace('.', ','), class_name="h4")
    
    with tgb.layout('1 1 '):
    ## SELETOR
        tgb.selector(
            value="{bairro}",
            lov=bairro,
            dropdown=True,
            multiple=True,
            label="Escolha o Bairro",
            class_name="fullwidth",
            on_change=on_filter,
        )
        tgb.selector(
            value="{pavimento}",
            lov=pavimento,
            dropdown=True,
            multiple=True,
            label="Escolha o tipo de pavimento",
            class_name="fullwidth",
        )

    with tgb.layout('1'):
      

        tgb.chart(
            "{contagem_pavimento}", 
            type="bar", 
            x="BAIRRO", 
            y__1="pavimentada", 
            y__2="não_pavimentada"
        )

##lançando o webapp
if __name__== "__main__" :
    Gui(page).run(
        titel="Vias Dashboard",
        use_reloader=True,
        degu=True,
    )

