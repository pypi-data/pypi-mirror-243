import re

class SlugifyClass:
    def __init__(self):
        self.caracteres_speciaux = [chr(i) for i in range(32, 127) if not chr(i).isalnum()]
        self.to_replace = list(self.caracteres_speciaux)

    def slugify(self, chenn, separator="-"):
        for i in chenn:
            if i in self.to_replace:
                chenn = chenn.replace(i, separator)
                if chenn[-1] in self.to_replace:
                    chenn = chenn[:-1]

        return chenn.strip().lower()

    def clean_tiret(self, txt):
        un_tiret = re.sub(r'-+', '-', txt)
        return un_tiret 

    def sans_accent(self, txt):
        accents = {'é': 'e', 'è': 'e', 'à': 'a', 'ê': 'e', 'ô': 'o', 'û': 'u', 'ç': 'c', 'î': 'i', 'â': 'a'}
        convert = ''.join(accents.get(char, char) for char in txt)
        return convert

    def fusion_fonct(self, chenn):
        k = self.slugify(chenn)
        k = self.clean_tiret(k)
        k = self.sans_accent(k)

        return k

if __name__ == "__main__":
    slugifier = SlugifyClass()
    chenn_input = input("Saisissez un texte : ")
    resultat_fusion = slugifier.fusion_fonct(chenn_input)

    index_non_tiret = 0
    while index_non_tiret < len(resultat_fusion) and resultat_fusion[index_non_tiret] == "-":
        index_non_tiret += 1

    resultat_fusion = resultat_fusion[index_non_tiret:]
    print(resultat_fusion)
