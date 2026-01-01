import psutil
import os
import shutil
# Importações necessárias para o volume funcionar
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def obter_processos_pesados():
    processos = []
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            processos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    processos = sorted(processos, key=lambda p: p['memory_info'].rss, reverse=True)[:3]
    resultado = "Os processos mais pesados agora são: "
    for p in processos:
        mb = p['memory_info'].rss / (1024 * 1024)
        resultado += f"{p['name']} com {mb:.0f} MB. "
    return resultado

def saude_hardware():
    uso_disco = psutil.disk_usage('/').percent
    # Intervalo menor para resposta mais rápida
    cpu_total = psutil.cpu_percent(interval=0.1) 
    return f"Senhor, o processador está em {cpu_total}% e o disco principal em {uso_disco}%."

def limpar_temporarios():
    pasta_temp = os.environ.get('TEMP')
    arquivos_removidos = 0
    if not pasta_temp: return "Não localizei a pasta TEMP."

    for nome in os.listdir(pasta_temp):
        caminho_completo = os.path.join(pasta_temp, nome)
        try:
            if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                os.unlink(caminho_completo)
                arquivos_removidos += 1
            elif os.path.isdir(caminho_completo):
                shutil.rmtree(caminho_completo)
                arquivos_removidos += 1
        except: continue
            
    return f"Protocolo concluído. Removi {arquivos_removidos} itens da pasta temporária."

def analisar_conexoes():
    try:
        conexoes = psutil.net_connections()
        processos_ativos = []
        for conn in conexoes:
            if conn.status == 'ESTABLISHED' and conn.pid:
                try:
                    p = psutil.Process(conn.pid)
                    if p.name() not in processos_ativos:
                        processos_ativos.append(p.name())
                except: continue
        
        if processos_ativos:
            return "Programas usando a rede: " + ", ".join(processos_ativos[:4])
        return "Nenhuma conexão externa suspeita."
    except:
        return "Não consegui acessar a tabela de conexões agora."

def encerrar_projeto():
    print("Encerrando Projeto Fenix. Até logo, Senhor.")
    os._exit(0)