import re


class PersonalExtractor:

    EMAIL_REGEX = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    PHONE_REGEX = re.compile(
        r"(\+?\d[\d\s\-\(\)]{7,}\d)"
    )

    LINKEDIN_REGEX = re.compile(
        r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9\-_]+",
        re.IGNORECASE
    )

    GITHUB_REGEX = re.compile(
        r"(https?://)?(www\.)?github\.com/[A-Za-z0-9\-_]+",
        re.IGNORECASE
    )

    PORTFOLIO_REGEX = re.compile(
        r"(https?://)?([A-Za-z0-9\-]+\.)+[A-Za-z]{2,}",
        re.IGNORECASE
    )

    def extraer(self, texto):

        resultado = {
            "nombre": "",
            "email": "",
            "telefono": "",
            "linkedin": "",
            "github": "",
            "portafolio": ""
        }

        lineas = [
            linea.strip()
            for linea in texto.splitlines()
            if linea.strip()
        ]

        # -------- Nombre (heurística simple) --------
        for linea in lineas[:5]:

            if len(linea.split()) in (2, 3):

                if not any(
                    c.isdigit()
                    for c in linea
                ):

                    if "@" not in linea:

                        resultado["nombre"] = linea
                        break

        # -------- Email --------
        match = self.EMAIL_REGEX.search(texto)

        if match:
            resultado["email"] = match.group()

        # -------- Teléfono --------
        match = self.PHONE_REGEX.search(texto)

        if match:
            resultado["telefono"] = match.group().strip()

        # -------- LinkedIn --------
        match = self.LINKEDIN_REGEX.search(texto)

        if match:
            resultado["linkedin"] = match.group()

        # -------- GitHub --------
        match = self.GITHUB_REGEX.search(texto)

        if match:
            resultado["github"] = match.group()

        # -------- Portafolio --------
        dominios_excluir = [
            "linkedin.com",
            "github.com",
            "gmail.com",
            "hotmail.com",
            "outlook.com"
        ]

        for match in self.PORTFOLIO_REGEX.finditer(texto):

            url = match.group()

            if not any(
                dominio in url.lower()
                for dominio in dominios_excluir
            ):
                resultado["portafolio"] = url
                break

        return resultado