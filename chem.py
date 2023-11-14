import markovify
import pandas as pd
import random

text_model = markovify.Text([' '.join(str(x)) for x in pd.read_csv('Elements.csv')['Element'].apply(str)], state_size=2)


class FictionalElement:
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties

def generate_new_name(existsing_names: list[str] = []):
    generated_name = text_model.make_sentence().replace(' ', '')
    while (generated_name == None or generated_name in existsing_names):
        generated_name = text_model.make_sentence().replace(' ', '')

    return generated_name
    


def generate_elements(num_elements : int):
    elements = []
    exist_names = []
    for i in range(num_elements):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Генерация случайных значений поверхностной энергии и плотности
        molecular_mass = 50 + i  # Пример значения молекулярной массы
        crystal_lattice = 5 + i  # Пример значения кристаллической решётки
        surface_energy = random.uniform(0.5, 2.0) * molecular_mass / crystal_lattice
        phase = random.choice(['liquid', 'gas', 'solid'])
        density = random.uniform(0.8, 1.5) * molecular_mass / (crystal_lattice ** 3) 
        
        if phase == 'solid':
            density *= 2
        if phase == 'gas':
            density *= 0.5

        element = FictionalElement(
            generate_new_name(exist_names),
            {
                "Electroactivity": "High" if i % 2 == 0 else "Low",
                "Magnetic_Properties": "Present" if i % 3 == 0 else "Absent",
                "Thermal_Stability": "Stable" if i % 4 == 0 else "Unstable",
                "Chemical_Reactivity": "Reactive" if i % 5 == 0 else "Non-reactive",
                "Crystal_Structure": "Cubic" if i % 6 == 0 else "Amorphous",
                "Radiation": "Emits" if i % 7 == 0 else "None",
                "Mass_Number": 100 + i,
                "Atomic_Number": 40 + i,
                "Elasticity_Strength": "Flexible" if i % 8 == 0 else "Rigid",
                "Color_Properties": "Changes color" if i % 9 == 0 else "Stable color",
                "Color":color,
                "Surface_Energy": surface_energy,
                "Density": density,
                "Toxicity_Safety": "Toxic" if i % 10 == 0 else "Non-toxic",
                "Phase" : phase,
                "Metall" : random.choice([True, False]),
                "Detoxification" : False if i % 10 == 0 else random.choice([True, False]),
                "Pure" : True
                # Добавьте другие свойства по вашему выбору
            }
        )
        exist_names.append(element.name)
        elements.append(element)
    return elements


# Пример генерации новой химической реакции с обязательными условиями
def generate_chemical_reaction(elements : list[FictionalElement], conditions_count:int = 2):
    # Выбираем два случайных элемента для реакции
    if len(elements) > 2:
        reactant = random.sample(elements, 2)
    elif len(elements) == 2:
        reactant = elements
    else:
        return None
    # Условия для протекания реакции
    required_conditions = [
        "Electroactivity",
        "Magnetic_Properties",
        "Thermal_Stability",
        "Chemical_Reactivity",
        "Crystal_Structure",
        "Radiation",
        "Elasticity_Strength",
        "Toxicity_Safety",
        "Phase",
        "Metall",
        "Detoxification",
        "Pure"
    ]  # Пример обязательных свойств для реакции
    conditions_count = min(conditions_count, len(required_conditions))
    required_conditions = random.sample(required_conditions, conditions_count)
    # Проверяем, удовлетворяют ли элементы условиям реакции
    if all(reactant[0].properties.get(cond) == reactant[1].properties.get(cond) for cond in required_conditions):
        new_properties = {}
        for prop in reactant[0].properties:
            if type(reactant[0].properties[prop]) is str:
                if random.random() < 0.5:
                    new_properties[prop] = reactant[0].properties[prop]
                else:
                    new_properties[prop] = reactant[1].properties[prop]
            elif type(reactant[0].properties[prop]) is bool:
                new_properties[prop] = random.choice([reactant[0].properties[prop], reactant[1].properties[prop]])
            elif type(reactant[0].properties[prop]) is float:
                new_properties[prop] = random.uniform(reactant[0].properties[prop], reactant[1].properties[prop])
            else:
                if random.random() < 0.5:
                    new_properties[prop] = reactant[0].properties[prop]
                else:
                    new_properties[prop] = reactant[1].properties[prop]

        new_properties["Pure"] = False
        new_element = FictionalElement(f"{reactant[0].name} + {reactant[1].name}", new_properties)
        return new_element
    else:
        return None  # Если реакция не может протекать

# Генерируем новые химические реакции с обязательными условиями
def generate_reactions(generated_elements : list[FictionalElement], number_of_reactions:int = 0, condition_count : int =2):
    compounds = {}
    if number_of_reactions < 0:
        for element1 in generated_elements:
            for element2 in generated_elements:
                new_compound = generate_chemical_reaction([element1, element2], condition_count)
                if new_compound and (element1.name + " + " + element2.name) not in compounds.keys() and (element2.name + " + " + element1.name) not in compounds.keys():
                    compounds[new_compound.name] = new_compound
                    print(f"New Compound: {new_compound.name}")
    else:
        while len(compounds.keys()) < number_of_reactions:
            new_compound = generate_chemical_reaction(generated_elements)
            if new_compound and new_compound.name not in compounds.keys():
                compounds[new_compound.name] = new_compound
                print(f"New Compound: {new_compound.name}")
    return compounds

def print_elements(elements: list[FictionalElement]):
    for element in elements:
        print(f"Compound: {element}")
        for prop, val in element.properties.items():
            print(f"{prop}: {val}")
        print()