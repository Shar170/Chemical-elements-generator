
import streamlit as st
import chem
import widgets
import random

st.set_page_config(page_title='ChemGen', page_icon='⚗', layout='wide')
st.title("👨‍🔬Generate your own chemistry!")

if 'uniq_id' not in st.session_state.keys():
    st.session_state['uniq_id'] = str(int(random.random()*1000000000))
    st.write(f"Session ID: ```{st.session_state['uniq_id']}```")
else:
    st.write(f"Session ID: ```{st.session_state['uniq_id']}```")

number_of_elements = st.slider("Number of elements", min_value=1, max_value=100, value=50)

all_reactions = st.checkbox('Generate all posible reactions', True)
if not all_reactions:
    number_of_compounds = st.slider("Number of compounds", min_value=1, max_value=1200, value=50)
else:
    number_of_compounds = -1

condition_count = st.slider("Number of conditions", min_value=1, max_value=10, value=[1,3])

generate = st.button("Generate")

if(generate):
    #condition_count = chem.random.randint(condition_count[0], condition_count[1])
    generated_elements = chem.generate_elements(number_of_elements)
    generated_compounds = chem.generate_reactions(generated_elements, number_of_compounds, condition_count)
    with st.expander(f'## Elements({len(generated_elements)})'):
        for element in generated_elements:
            widgets.show_element(element)
    with st.expander(f'## Compounds({len(generated_compounds)})'):
        for compound in generated_compounds.values():
            widgets.show_reaction(compound)
    show_new_elements = st.checkbox("Show new elements on graph?", True)
    st.markdown('## Chemistry')
    widgets.plot_chem(generated_elements, generated_compounds, show_new_elements)
    st.markdown('## Table')
    st.markdown('### Elements')
    widgets.dataframe_of_elements(generated_elements)
    st.markdown('### Reactions')
    widgets.dataframe_of_compounds(generated_compounds)