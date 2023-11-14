
import streamlit as st

import chem
import widgets
st.set_page_config(page_title='ChemGen', page_icon='⚗', layout='wide')
st.title("Your custom, uniq chemistry!")
number_of_elements = st.slider("Number of elements", min_value=1, max_value=100, value=50)

all_reactions = st.checkbox('Generate all posible reactions', True)
if not all_reactions:
    number_of_compounds = st.slider("Number of compounds", min_value=1, max_value=1200, value=50)
else:
    number_of_compounds = -1

generate = st.button("Generate")

if(generate):
    condition_count = chem.random.randint(1,3)
    generated_elements = chem.generate_elements(number_of_elements)
    generated_compounds = chem.generate_reactions(generated_elements, number_of_compounds)
    with st.expander(f'## Elements({len(generated_elements)})'):
        for element in generated_elements:
            widgets.show_element(element) 
    with st.expander(f'## Compounds({len(generated_compounds)})'):
        for compound in generated_compounds.values():
            widgets.show_element(compound)
    show_new_elements = st.checkbox("Show new elements on graph?", True)
    st.markdown('## Chemistry')
    widgets.plot_chem(generated_elements, generated_compounds, show_new_elements)