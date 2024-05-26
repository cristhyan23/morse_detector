import cv2
import mediapipe as mp
import numpy as np
import time

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

# Dicionário Morse
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9'
}

def morse_to_text(morse_code):
    words = morse_code.strip().split("   ")
    translated_text = []
    for word in words:
        if word not in MORSE_CODE_DICT.keys():
            translated_text.append("")
        translated_word = ''.join(MORSE_CODE_DICT.get(char, '') for char in word.split())
        translated_text.append(translated_word)
    return ' '.join(translated_text)


# Função para calcular a distância entre os lábios
def mouth_aspect_ratio(landmarks):
    top_lip = np.array([landmarks[13].x, landmarks[13].y])
    bottom_lip = np.array([landmarks[14].x, landmarks[14].y])
    return np.linalg.norm(top_lip - bottom_lip)

# Parâmetros de detecção de movimento
MOUTH_THRESHOLD = 0.05  # Ajuste este valor conforme necessário
DOT_DURATION = 0.3  # Duração de um ponto em segundos
DASH_DURATION = 1.0  # Duração de um traço em segundos
LETTER_PAUSE = 5.0  # Tempo de pausa entre letras em segundos
morse_code = ""
last_movement_time = time.time()
mouth_open_time = None
save_phrase = []  # Lista para armazenar as palavras traduzidas

# Captura de vídeo da câmera do notebook
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
            
            landmarks = face_landmarks.landmark
            mar = mouth_aspect_ratio(landmarks)

            if mar > MOUTH_THRESHOLD:
                if mouth_open_time is None:
                    mouth_open_time = time.time()  # Registra o tempo de início da abertura da boca
            else:
                if mouth_open_time is not None:
                    blink_duration = time.time() - mouth_open_time
                    if blink_duration < DOT_DURATION:
                        morse_code += "."
                    elif blink_duration < DASH_DURATION:
                        morse_code += "-"
                    mouth_open_time = None  # Reseta o tempo de abertura da boca

    # Traduza o código Morse
    word = morse_to_text(morse_code)
    
    # Atualizar e mostrar a frase
    if len(word) > 0 and time.time() - last_movement_time > LETTER_PAUSE:
        save_phrase.append(word)
        morse_code = ""  # Resetar após decodificação
        last_movement_time = time.time()  # Reiniciar o tempo do último movimento detectado

    phrase_text = " ".join(save_phrase)
    
    # Mostrar o frame, código Morse atual e frase
    cv2.putText(frame, f"Morse Code: {morse_code}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Translated Word: {word}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Phrase: {phrase_text}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Frame', frame)

    # Verificar se a tecla 'c' foi pressionada para limpar a frase
    if cv2.waitKey(1) & 0xFF == ord('c'):
        save_phrase.clear()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   

cap.release()
cv2.destroyAllWindows()
