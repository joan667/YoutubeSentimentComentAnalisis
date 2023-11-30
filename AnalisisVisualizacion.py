from collections import defaultdict
from transformers import pipeline
import matplotlib.pyplot as plt

classifier = pipeline("zero-shot-classification")


#Paso 1. leemos todos los comentarios que hemos guardado previamente i los metemos en un array
with open('Phone_coments.txt', 'r', encoding='utf-8') as file:
    lines_array = [line.strip() for line in file.readlines()]


#Paso 2. Escribimos en un fichero todos esos comentarios que nos interessan, que traten sobre el producto que nos interessa.
#Tambien escribimos en otro fichero la certeza de que ese comentario trate sobre ese tema
with open('Valid_Phone_Coments.txt', 'w', encoding='utf-8') as file1, open('Valid_Phone_Coments_Pesos.txt', 'w', encoding='utf-8') as file2:
    
    
    for line in lines_array:
        
        #classificamos el comentario dependiendo de si trata sobre el producto o no
        res = classifier(
            line.replace("&#39;","\""),
            candidate_labels = ["About S23","About Other"] #Etiquetas con las que vamos a classificar
        )
        
        #Comprovamos con que certeza ese comentario habla sobre el prodcto, Si supera el 0.6 lo acceptamos y lo escribimos en el fichero
        if(res['labels'][0] == 'About S23' and res['scores'][0] > 0.6):
            file1.write(line.replace("&#39;","\"") + "\n") #escritura comentario
            file2.write( str(res['scores'][0]) + "\n") #escritura del peso del comentario


#Paso 3. Guardar los comentarios i sus respectivos pesos en dos arrays diferents
with open('Valid_Phone_Coments.txt', 'r', encoding='utf-8') as file1, open('Valid_Phone_Coments_Pesos.txt', 'r', encoding='utf-8') as file2:
    comentarios = [line.strip() for line in file1.readlines()]
    pesos = [line.strip() for line in file2.readlines()]



#Passo 4. Obtener el "vector" de sentimientos para cada comentario
SentimentArray = []
WeightSentimentArray = []

for comentario, peso in zip(comentarios, pesos):
    res = classifier(
        comentario,

        candidate_labels = ["Excitement","Anger","Disgust","Joy","Sadness"]     #Etiquetas con las que vamos a classificar

    )
    SentimentArray.append(res['labels'][0])
    WeightSentimentArray.append( res['scores'][0] * float(peso) )
    
    SentimentArray.append(res['labels'][1])
    WeightSentimentArray.append( res['scores'][1] * float(peso) )
    
    SentimentArray.append(res['labels'][2])
    WeightSentimentArray.append( res['scores'][2] * float(peso) )
    
    SentimentArray.append(res['labels'][3])
    WeightSentimentArray.append( res['scores'][3] * float(peso) )
    
    SentimentArray.append(res['labels'][4])
    WeightSentimentArray.append( res['scores'][4] * float(peso) )



#Paso 5. Agregación i normalización de todos los "vectores" de sentimeinto
# Crea un defaultdict para agrupar los valores según sus índices
sumas = defaultdict(int)
# Itera sobre los elementos de ambos arrays
for sentiment, weight in zip(SentimentArray, WeightSentimentArray):
    # Usa los elementos como clave y suma los valores
    sumas[sentiment] += weight

# Convierte el resultado de defaultdict a una lista
resultado = list(sumas.items())

lista_sentimientos = [resultado[0][0], resultado[1][0],resultado[2][0],resultado[3][0],resultado[4][0]]
valores_normalizados = [resultado[0][1]/len(comentarios), resultado[1][1]/len(comentarios),
                        resultado[2][1]/len(comentarios),resultado[3][1]/len(comentarios),resultado[4][1]/len(comentarios)]




#Paso 6 y final. Visualizar el resultado mediante un diagrama de barras con matplotlib
import matplotlib.pyplot as plt

# Crear el gráfico de barras
plt.bar(lista_sentimientos, valores_normalizados ,  
        color = ['red' if val == 'Anger' or val == 'Sadness' or val == 'Disgust' else 'green' for val in lista_sentimientos])

# Configurar etiquetas y título
plt.xlabel('Sentimientos')
plt.ylabel('Porcentaje(%)')
plt.title('Analisis de sentimientos del video')


plt.show()
