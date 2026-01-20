import os, asyncio, uuid, pygame, edge_tts

async def processo_falar(texto): # Mudamos o nome aqui para bater com o brain.py
    voice = "pt-BR-AntonioNeural"
    id_sessao = str(uuid.uuid4())[:8]
    output_file = f"res_{id_sessao}.mp3"
    
    try:
        communicate = edge_tts.Communicate(texto, voice)
        await communicate.save(output_file)
        await asyncio.sleep(0.2)

        if os.path.exists(output_file):
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            pygame.mixer.music.unload()
            
            # Tentativa de remoção segura
            try:
                os.remove(output_file)
            except:
                pass 
                
    except Exception as e:
        print(f"Erro no motor de áudio: {e}")