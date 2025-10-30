import pandas as pd

df = pd.read_csv("PlanilhaDados.csv")

### Coluna nivel senioridade ###
nivel = df["Nivel_Senioridade"]

# Convertendo para junior
df.loc[df["Nivel_Senioridade"].str.lower().str.contains("j"), "Nivel_Senioridade"] = "Júnior"

# Convertendo para pleno
df.loc[df["Nivel_Senioridade"].str.lower().str.contains("p"), "Nivel_Senioridade"] = "Pleno"

# Convertendo para senior
df.loc[df["Nivel_Senioridade"].str.lower().str.contains("s"), "Nivel_Senioridade"] = "Sênior"

# Garante que é maiuscula
df["Nivel_Senioridade"] = df["Nivel_Senioridade"].str.strip().str.capitalize()

# Vendo quem é n/d e convertendo pra moda
moda = df["Nivel_Senioridade"].mode()[0]
df.loc[df["Nivel_Senioridade"].str.lower().isin(["n/d"]), "Nivel_Senioridade"] = moda

### Coluna avaliacao tecnica e comportamental ###
# Definindo 10 e 0 como max e min
df["Avaliacao_Tecnica"] = df["Avaliacao_Tecnica"].clip(lower = 0, upper = 10)
df["Avaliacao_Comportamental"] = df["Avaliacao_Comportamental"].clip(lower = 0, upper = 10)

# Corrigindo os valores nulos com a media aritmetica
media_tecnica = df["Avaliacao_Tecnica"].mean()
df.loc[df["Avaliacao_Tecnica"].isna(), "Avaliacao_Tecnica"] = (media_tecnica).round(2)

media_comportamental = df["Avaliacao_Comportamental"].mean()
df.loc[df["Avaliacao_Comportamental"].isna(), "Avaliacao_Comportamental"] = (media_comportamental).round(2)

# Ajeitando a pontuacao das casas decimais, converte os numeros pra string e dps troca o ponto pela virgula
df["Avaliacao_Tecnica"] = df["Avaliacao_Tecnica"].astype(str).str.replace(".", ",", regex=False)
df["Avaliacao_Comportamental"] = df["Avaliacao_Comportamental"].astype(str).str.replace(".", ",", regex=False)

# Variaveis dos df
tecnica = df["Avaliacao_Tecnica"]
comportamental = df["Avaliacao_Comportamental"]

### Coluna engajamento ###
# Corrigindo os nulos N/A
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].replace(["N/A", ""], pd.NA)

# Mudando a %
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].str.replace("%","",regex=False).astype(float)/100

# Ajeitando os nulos NaN
media_engajamento = df["Engajamento_PIGs"].mean()
df.loc[df["Engajamento_PIGs"].isna(), "Engajamento_PIGs"] = media_engajamento

# Bota o df arredondado dentro de uma variavel
df["Engajamento_PIGs"] = df["Engajamento_PIGs"].round(2)
engajamento = df["Engajamento_PIGs"]

### Coluna score###
# Transformar as avaliacoes para float dnv criando outros df pra manter o original normal
df["Avaliacao_Tecnica_Float"] = df['Avaliacao_Tecnica'].str.replace(",",".").astype(float)
df["Avaliacao_Comportamental_Float"] = df['Avaliacao_Comportamental'].str.replace(",",".").astype(float)

# Calcular o score 
df['Score_Desempenho'] =(df["Avaliacao_Tecnica_Float"]*0.5 + df['Avaliacao_Comportamental_Float']*0.5).round(2)
score = df["Score_Desempenho"]
# Excluir os outros df
df = df.drop(columns=["Avaliacao_Tecnica_Float", "Avaliacao_Comportamental_Float"])

### Coluna status ###
df["Status_Membro"] = "Padrão"
df.loc[(df["Score_Desempenho"] >= 7) & (df["Engajamento_PIGs"] >= 0.8), "Status_Membro"] = "Em destaque"
status = df["Status_Membro"]

# Chamada da planilha
print(df.head())

# Salvando
df.to_csv("PlanilhaDados_Modificada.csv", index=False)
