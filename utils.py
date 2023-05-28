def format_primes(filename : str) -> list[int]:
    with open(filename) as file:
        content = file.read()
        # Formattage du contenu
        content = content.split(" ")
        content = [int(i) for i in content if i != '' and '\n' not in i]
        return content