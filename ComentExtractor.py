import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"

DEVELOPER_KEY = "API_KEY_GENERADA" #Cuidado hay que tener una cuenta de google cloud i tener el servicio de google cloud activado con su API KEY generada

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

# ID del video
video_id = '2ZF8k_6xPVc'

total_comments_to_retrieve = 772
# Configura los parámetros para la primera solicitud
request = youtube.commentThreads().list(
    part='snippet',
    videoId=video_id,
    maxResults=100 # Número máximo de comentarios por página
)

# Variable para rastrear el número de comentarios recuperados
comments_retrieved = 0

# Abre un archivo para escribir todos los comentarios
with open('Phone_coments.txt', 'w', encoding='utf-8') as file:
    # Realiza solicitudes hasta que alcances el número total deseado
    while comments_retrieved < total_comments_to_retrieve:
        # Realiza la solicitud para la página actual
        response = request.execute()

        # Escribe los comentarios de la página actual en el archivo
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            file.write(comment + '\n')
            comments_retrieved += 1

            # Verifica si ya has alcanzado el número total deseado
            if comments_retrieved >= total_comments_to_retrieve:
                break

        # Verifica si hay más páginas de comentarios (paginación)
        if 'nextPageToken' in response:
            # Obtiene el token de la próxima página
            next_page_token = response['nextPageToken']

            # Configura los parámetros para la siguiente página
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token
            )
        else:
            # No hay más páginas, salir del bucle
            break
