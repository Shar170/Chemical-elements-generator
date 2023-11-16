import streamlit as st
import chem
import nx_altair as nxa
import altair as alt
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


def rgbToHex(rgb):
    x = ''
    for i in rgb:
        x += format(i,'02x').upper()
        try:
            if x[0] == x[1] and x[2] == x[3] and x[4] == x[5]:
                x = x[0] + x[2] + x[4]
        except:
            pass
    return '#'+x

def show_element(element : chem.FictionalElement):
    with st.form(element.name):
        st.markdown(f"### {element.name} ({element.short_name})")
        for prop in element.properties.keys():
            if prop == "Color":
                st.color_picker('Color of element:', rgbToHex(element.properties[prop]), disabled=True)
            else:
                st.write(f"{prop}: ```{element.properties[prop]}```")
        
        st.form_submit_button(f'{element.short_name}', disabled=True)

def show_reaction(reaction : chem.FictionalReaction):
    with st.form(reaction.name):
        st.markdown(f"### {reaction.name}")
        st.markdown(f"#### {reaction.reactants[0].name} + {reaction.reactants[1].name} → {reaction.product.name}")
        for prop in reaction.product.properties.keys():
            if prop == "Color":
                st.color_picker('Color of element', rgbToHex(reaction.product.properties[prop]), disabled=True)
            else:
                st.write(f"{prop}: ```{reaction.product.properties[prop]}```")
        
        st.form_submit_button()


def plot_chem(generated_elements : list[chem.FictionalElement], compounds : dict[str, chem.FictionalReaction], draw_notpure: bool = False):
    
    # Сгенерируем реакции и добавим результаты в граф
    G = nx.Graph()

    for element in generated_elements:
        element.properties['Name'] = element.name
        G.add_nodes_from([(element.name, element.properties)])
    
    if draw_notpure:
        for key, reaction in compounds.items():
                          
            reaction.product.properties['Name'] = reaction.product.name
            G.add_nodes_from([(reaction.product.name, reaction.product.properties)])
        
            G.add_edge(reaction.product.name, 
                reaction.reactants[0].name,
                reaction=reaction.name)
            G.add_edge(reaction.product.name, 
                reaction.reactants[1].name,
                reaction=reaction.name)
    else:
        for key, new_compound in compounds.items():
            # Добавляем элементы и результаты реакций в граф
            G.add_edge(new_compound.reactants[0].name, 
                    new_compound.reactants[0].name, 
                    reaction=new_compound.name)

    # Рисуем граф
    plt.figure(figsize=(25, 12))
    pos = nx.spring_layout(G, dim=2)

    # Draw the graph using Altair

    viz = nxa.draw_networkx(G, pos=pos,
                            node_color='Pure',
                            node_tooltip=[
                                "Name",
                                "Pure",
                                "Phase",
                                "Electroactivity",
                                "Radiation",
                                "Mass_Number",
                                "Atomic_Number",
                                "Toxicity_Safety",
                                "Detoxification",
                            ],
                            width=3,
                            edge_tooltip='reaction',
                            node_label='Name',
                            #cmap='viridis',
                            linewidths=5,
                            node_size=500,
                            edge_color='reaction')

    # Show it as an interactive plot!
    viz = viz.interactive()
    _, col, _ = st.columns([1, 5, 1])
    col.altair_chart(viz, use_container_width=True)

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def dataframe_of_elements(generated_elements : list[chem.FictionalElement]):
    elements = []
    for element in generated_elements:
        element.properties["Name"] = element.name
        element.properties["Short_Name"] = element.short_name
        elements.append(element.properties)
    df = pd.DataFrame.from_dict([e.properties for e in generated_elements])
    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols]
    st.dataframe(df)
    st.download_button(
        "Download CSV",
        convert_df(df),
        "elements.csv",
        "text/csv",
        key='download-elements-csv'
        )

def dataframe_of_compounds(generated_compounds : dict[str, chem.FictionalReaction]):
    compounds = []
    for key, reaction in generated_compounds.items():
        reaction.product.properties["Name"] = reaction.product.name
        reaction.product.properties["Formula"] = f"{reaction.reactants[0].name} + {reaction.reactants[1].name} → {reaction.product.name}"
        reaction.product.properties["Condition"] = reaction.conditions
        compounds.append(reaction.product.properties)
    df = pd.DataFrame.from_dict(compounds)
    cols = df.columns.tolist()
    cols = cols[-3:] + cols[:-3]
    df = df[cols]
    st.dataframe(df)
    st.download_button(
        "Download CSV",
        convert_df(df),
        "reactions.csv",
        "text/csv",
        key='download-reactions-csv'
        )