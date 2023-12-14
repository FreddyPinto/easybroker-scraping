from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

# Lee las variables de entorno
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# Inicializa el navegador
driver = webdriver.Chrome()

# Abre la página de inicio de sesión
driver.get('https://www.easybroker.com/mx/account/authentication/new')

# Espera a que se cargue la página
time.sleep(2)

# Haz clic en el botón de iniciar sesión con email
boton_email = driver.find_element(By.XPATH, '//a[@data-email-button]')
boton_email.click()

# Espera a que se muestre el formulario
time.sleep(2)

# Ingresa el email
campo_email = driver.find_element(By.XPATH, '//input[@id="authentication_email"]')
campo_email.send_keys(email)

# Haz clic en continuar
boton_continuar = driver.find_element(By.XPATH, '//input[@value="Continuar"]')
boton_continuar.click()

# Espera a que se muestre el siguiente formulario
time.sleep(2)

# Ingresa la contraseña
campo_password = driver.find_element(By.XPATH, '//input[@id="session_password"]')
campo_password.send_keys(password)

# Haz clic en iniciar sesión
boton_iniciar_sesion = driver.find_element(By.XPATH, '//input[@value="Iniciar sesión"]')
boton_iniciar_sesion.click()

# Inicializa listas para almacenar los datos
nombres = []
ciudades = []
telefonos = []
sitios_web = []

# Itera sobre las páginas
for i in range(1, 342):  # Ajusta el rango según sea necesario
    # Navega a la página
    driver.get(f'https://www.easybroker.com/agent/agencies/search?page={i}&reset_page=true')

    # Espera a que se cargue la página
    time.sleep(2)

    # Obtiene el HTML de la página
    html = driver.page_source

    # Analiza el HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Encuentra los elementos necesarios
    elements = soup.find_all('div', class_='col-md-4')

    # Itera sobre los elementos y extrae los datos
    for element in elements:
        nombre = element.find('h6', class_="organization-title m-0").text.strip()
        ciudad = element.find('p', class_="m-0").text.strip()
        telefono = element.find('a', href=lambda href: href and "tel:" in href).text.strip()
        enlace = element.find('a', href=lambda href: href and href.startswith('https://'))
        sitio_web = enlace.get('href') if enlace else None

        # Agrega los datos a las listas correspondientes
        nombres.append(nombre)
        ciudades.append(ciudad)
        telefonos.append(telefono)
        sitios_web.append(sitio_web)

# Crea un DataFrame
df = pd.DataFrame({
    'Nombre': nombres,
    'Ciudad': ciudades,
    'Telefono': telefonos,
    'Sitio web': sitios_web,
})

# Reemplaza las filas vacías con None
df['Ciudad'] = df['Ciudad'].replace("", None)

# Guarda el DataFrame en un archivo CSV
df.to_csv('data/raw/datos2.csv', index=False)

# Cierra el navegador
driver.quit()

# Imprime un mensaje de éxito
print("Datos guardados en data/raw/datos.csv")
