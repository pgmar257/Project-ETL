# Con este bucle conseguí hacer clicks dentro de la web de Honda, y esos clicks abrian los enlaces de cada modelo de moto y a su vez desplegaban el precio y las especificaciones... ¡¡¡de forma COMPLETAMENTE AUTOMÁTICA!!! Mientras el bucle recorria cada URL distinta en la cual se encontraban todos los tipos de motos disponibles en la web de Honda, a su vez se guardaban en un dataframe que finalmente uní con el método concat y donde los nombres de las columnas son los nombres de las especificaciones dentro de la ficha técnica y sus valores aparecen reflejados en filas; Tuve un problema con la ejecución de este código (bueno, uno no, muchísimos.) Y es que no entendía el por qué no se añadian los nombres, las gamas y los precios de cada moto de manera automática pero si se guardaban en la memoria al pasar los clicks, lo solucioné de manera sencilla añadiendo esos valores al datraframe final.


dfs = []
for link in final_links:
    gama = link.split('/')[5]
    name = link.split('/')[6]
    driver.get(link)
    try:
        price = driver.find_elements(By.XPATH, '//*[@id="page"]/div[1]/div[2]/div[1]/div/div/div[1]/div[2]/dl[1]/dd/span')[0].text
    except:
        price = driver.find_elements(By.XPATH, '//*[@id="page"]/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/dl[1]/dd')[0].text
    
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find_all('td', class_="title")
    titles_clean = [e.text for e in title]
    results = soup.find_all('td', class_="result")
    results_clean = [e.text for e in results]
    list_of_tuples = list(zip(titles_clean, results_clean))
    df = pd.DataFrame.from_records(list_of_tuples)
    df_transpose = df.T
    new_header = df_transpose.iloc[0]
    df_final = df_transpose[1:] 
    df_final.columns = new_header
    df_final[columns_filtering]
    df_final["Gama"] = gama
    df_final["Nombre"] = name
    df_final["Precio"] = price
    dfs.append(df_final)
    