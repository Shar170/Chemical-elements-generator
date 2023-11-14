import streamlit as st
import chem
import nx_altair as nxa
import altair as alt
import networkx as nx
import matplotlib.pyplot as plt

def show_element(element : chem.FictionalElement):
    with st.form(element.name):
        st.markdown(f"### {element.name}")
        for prop in element.properties.keys():
            st.write(f"{prop}: ```{element.properties[prop]}```")
        
        st.form_submit_button()

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

def plot_chem(generated_elements : list[chem.FictionalElement], compounds : dict[str, chem.FictionalElement], draw_notpure: bool = False):
    
    # Сгенерируем реакции и добавим результаты в граф
    G = nx.Graph()

    for element in generated_elements:
        element.properties['Name'] = element.name
        G.add_nodes_from([(element.name, element.properties)])
    if draw_notpure:
        for new_element in compounds.values():
            new_element.properties['Name'] = new_element.name
            G.add_nodes_from([(new_element.name, new_element.properties)])


    for new_compound in compounds.values():
        if draw_notpure:
            # Добавляем элементы и результаты реакций в граф
            G.add_edge(new_compound.name, 
                    new_compound.name.split(" + ")[1], 
                    reaction=new_compound.name, 
                    properties= '\n'.join([f'{key}: {value}\n' for key, value in element.properties.items()]))
            # Добавляем элементы и результаты реакций в граф
            G.add_edge(new_compound.name.split(" + ")[0], 
                    new_compound.name, 
                    reaction=new_compound.name, 
                    properties= '\n'.join([f'{key}: {value}\n' for key, value in element.properties.items()]))
        else:
            # Добавляем элементы и результаты реакций в граф
            G.add_edge(new_compound.name.split(" + ")[0], 
                    new_compound.name.split(" + ")[1], 
                    reaction=new_compound.name, 
                    properties= '\n'.join([f'{key}: {value}\n' for key, value in element.properties.items()]))

    # Рисуем граф
    plt.figure(figsize=(25, 12))
    pos = nx.spring_layout(G, dim=2)


    #node_labels = {node: f"{node}" for node, props in nx.get_node_attributes(G, 'name').items()}
    #node_colors = [props for node, props in nx.get_node_attributes(G, 'color').items()]
    #edge_labels = nx.get_edge_attributes(G, 'reaction')
    #nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=150, font_size=10, font_weight='bold', node_color=node_colors)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels

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
    st.altair_chart(viz)