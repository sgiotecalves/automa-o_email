import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
 
# Configurações globais
CRITICAL_THRESHOLD = 50  # Valor crítico de estoque
ALERT_EMAIL = "giovanaalves.1404@gmail.com"  # Substitua pelo seu e-mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "giovanaalves.1404@gmail.com"  # Substitua pelo seu e-mail
SMTP_PASSWORD = "ihtc qoee sddy wkrc"  # Substitua pela senha de aplicativo gerada no Gmail
 
# Função para leitura de dados do CSV
# Função para leitura de dados do CSV
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        # Verificar se as colunas necessárias existem
        if 'esteira' not in data.columns or 'estoque' not in data.columns:
            print("Erro: As colunas 'esteira' e/ou 'estoque' não foram encontradas no arquivo.")
            return None
        return data
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

 
# Função para analisar os dados
def analyze_data(data):
    return data[data['estoque'] < CRITICAL_THRESHOLD]
 
# Função para gerar alertas na tela
def display_alerts(critical_rows):
    for index, row in critical_rows.iterrows():
        print(f"⚠️ Alerta: Estoque baixo na esteira {row['esteira']}! Estoque atual: {row['estoque']}")
 
# Função para enviar email
def send_email_alerts(critical_rows):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Inicia conexão segura
            server.login(SMTP_USER, SMTP_PASSWORD)  # Autentica com o servidor SMTP
 
            for _, row in critical_rows.iterrows():
                msg = MIMEMultipart()
                msg['From'] = ALERT_EMAIL
                msg['To'] = ALERT_EMAIL
                msg['Subject'] = f"Alerta Crítico - Esteira {row['esteira']}"
 
                body = f"""
                Alerta crítico!
                A esteira {row['esteira']} está com nível de estoque crítico.
                Estoque atual: {row['estoque']}
                """
                msg.attach(MIMEText(body, 'plain'))
                server.sendmail(ALERT_EMAIL, ALERT_EMAIL, msg.as_string())
                print(f"Email enviado para {ALERT_EMAIL} sobre a esteira {row['esteira']}.")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
 
# Função para salvar histórico de alertas em Excel
def save_report(critical_rows, output_path="relatorio_alertas.xlsx"):
    try:
        if os.path.exists(output_path):
            historical_data = pd.read_excel(output_path)
            new_data = pd.concat([historical_data, critical_rows])
        else:
            new_data = critical_rows
 
        # Adicionando a coluna de data/alerta sem gerar o aviso SettingWithCopyWarning
        new_data = new_data.copy()
        new_data.loc[:, 'data_alerta'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data.to_excel(output_path, index=False)
        print(f"Relatório salvo em {output_path}")
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")
 
# Função principal
def main():
    file_path = "dados_estoque.csv"  # Nome do arquivo CSV com os dados
    data = load_data(file_path)
 
    if data is not None:
        critical_rows = analyze_data(data)
 
        if not critical_rows.empty:
            display_alerts(critical_rows)
            send_email_alerts(critical_rows)
            save_report(critical_rows)
        else:
            print("Todos os níveis de estoque estão dentro do esperado.")
    else:
        print("Falha na leitura dos dados. Verifique o arquivo.")
 
if __name__ == "__main__":
    main()