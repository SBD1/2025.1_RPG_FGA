# Tabela de eficácia
eficacias = {
    'M': {'P': 1.5, 'H': 0.75},
    'P': {'E': 1.5, 'M': 0.75},
    'H': {'M': 1.5, 'G': 0.75},
    'E': {'G': 1.5, 'P': 0.75},
    'G': {'H': 1.5, 'E': 0.75}
}

def eficacia(elemento1, elemento2):
    return eficacias.get(elemento1, {}).get(elemento2, 1)

# TESTE
elemento1, elemento2 = 'M', 'P'
temp = 100
resultado = eficacia(elemento1, elemento2)
temp *= resultado
print(f'O valor obtido é {temp}')