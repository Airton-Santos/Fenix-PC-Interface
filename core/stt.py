# core/stt.py
import speech_recognition as sr

def capturar_voz(reconhecedor, timeout=None, phrase_limit=None):
    """Captura áudio do microfone e converte em texto via Google STT"""
    with sr.Microphone() as source:
        try:
            # O listen agora tem um timeout para não ficar travado se você não falar
            audio = reconhecedor.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            
            # Converte áudio para texto
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            return texto.lower().strip()
            
        except sr.UnknownValueError:
            # Ocorreu um silêncio ou barulho que a Feni não entendeu
            return None
        except sr.RequestError:
            # Falha de conexão com a internet
            print("Senhor, estou com dificuldades de conexão com os serviços de voz.")
            return None
        except Exception:
            # Qualquer outro erro (microfone desconectado, etc)
            return None