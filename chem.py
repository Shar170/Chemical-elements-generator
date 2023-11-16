import markovify
import pandas as pd
import random

text_model = markovify.Text([' '.join(str(x)) for x in pd.read_csv('Elements.csv')['Element'].apply(str)], state_size=2)
exists_short_names = []

def gcd(a, b):
    """
    Calculate the greatest common divisor (GCD) using Euclid's algorithm.
    """
    while b:
        a, b = b, a % b
    return a

def convert_to_subscript(number):
    """
    Convert the symbol of a number to a subscript.
    """
    subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    subscript_number = str(number).translate(subscript_digits)
    return subscript_number

def calculate_formula(element1, valency1, element2, valency2):
    """
    Calculate the chemical formula of a compound formed by two elements with different valencies.
    """
    # Find the least common multiple (LCM) of valencies
    lcm = abs(valency1 * valency2) // gcd(valency1, valency2)

    # Determine the ratio of atoms in the compound
    ratio1 = lcm // abs(valency1)
    ratio2 = lcm // abs(valency2)

    # Construct the chemical formula
    formula = f"{element1}{convert_to_subscript(ratio1)}{element2}{convert_to_subscript(ratio2)}"

    return formula


def do_short(long_name):
    """Make chemical element name is short. Extract first consonant letters or first two letters
    Nikecle => Nk"""
    result = ''
    result = long_name[0]
    #try generate single letter name
    if result not in exists_short_names:
        exists_short_names.append(result)
        return result
    #try generate two letter name
    if long_name[0:2] not in exists_short_names:
        result = long_name[0:2]
        exists_short_names.append(long_name[0:2])
        return result
    
    #try generate two symbols name with consonants letters
    for letter in long_name[1:]:
        if letter not in 'aeiouAEIOU':
            result += letter
        if len(result) > 2:
            if result in exists_short_names:
                result = long_name[0]
            else:
                break

    return result


class FictionalElement:
    def __init__(self, name, properties, valency = -1):
        self.name = name
        self.short_name = do_short(name)
        self.properties = properties
        self.valency = random.randint(1,5) if valency == -1 else valency

class Condition:
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties



class FictionalReaction:
    def __init__(self, name, reactants : list[FictionalElement], product:FictionalElement, conditions:list):
        self.name = name
        self.reactants = reactants
        self.product = product
        self.conditions = conditions

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
                "Thermal_Stability": "Unstable" if i % 4 == 0 else "Stable",
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
def generate_chemical_reaction(elements : list[FictionalElement], conditions_count: list[int] = [1,2]):
    # Выбираем два случайных элемента для реакции
    if len(elements) > 2:
        reactant = random.sample(elements, 2)
    elif len(elements) == 2:
        reactant = elements
    else:
        return None
    
    if reactant[0].name == reactant[1].name:
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
    conditions_count = random.randint(conditions_count[0], conditions_count[1])
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
        formula = calculate_formula(reactant[0].short_name, reactant[0].valency, reactant[1].short_name, reactant[1].valency)
        new_element = FictionalElement(formula, new_properties)
        reaction = FictionalReaction(name=formula,
                                     reactants=[reactant[0], reactant[1]], 
                                     product=new_element, 
                                     conditions=required_conditions)
        return reaction
    else:
        return None  #Если реакция не может протекать

# Генерируем новые химические реакции с обязательными условиями
def generate_reactions(generated_elements : list[FictionalElement], number_of_reactions:int = 0, condition_count : list[int] =[1,2]):
    compounds = {}
    if number_of_reactions < 0:
        for element1 in generated_elements:
            for element2 in generated_elements:
                if element1 == element2:
                    continue
                new_compound = generate_chemical_reaction([element1, element2], condition_count)
                if new_compound != None and (element1.name + " + " + element2.name) not in compounds.keys() and (element2.name + " + " + element1.name) not in compounds.keys():
                    compounds[new_compound.name] = new_compound
                    print(f"New Compound: {new_compound.name}")
    else:
        while len(compounds.keys()) < number_of_reactions:
            new_compound = generate_chemical_reaction(generated_elements)
            
            if new_compound != None and new_compound.name not in compounds.keys():
                compounds[new_compound.name] = new_compound
                print(f"New Compound: {new_compound.name}")
    return compounds

def print_elements(elements: list[FictionalElement]):
    for element in elements:
        print(f"Compound: {element}")
        for prop, val in element.properties.items():
            print(f"{prop}: {val}")
        print()