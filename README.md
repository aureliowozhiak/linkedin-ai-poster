# README - Bot de Comentários no LinkedIn

## Visão Geral
Este projeto é um bot automatizado que faz login no LinkedIn, carrega posts do feed e gera comentários engajadores utilizando a API da OpenAI. Ele utiliza Selenium para automação do navegador e WebDriver Manager para gerenciar o driver do Chrome.

## Requisitos
Antes de iniciar, certifique-se de ter os seguintes requisitos instalados:

- Python 3.7+
- Google Chrome instalado
- WebDriver Manager
- Selenium
- Biblioteca OpenAI

## Instalação
1. Clone este repositório:
   ```sh
   git clone https://github.com/aureliowozhiak/linkedin-ai-poster.git
   cd linkedin-ai-poster
   ```
2. Instale as dependências necessárias:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure as credenciais em um arquivo `secret.py`:
   ```
   EMAIL=seu_email@exemplo.com
   PASSWORD=sua_senha
   OPENAI_API_KEY=sua_chave_api_openai
   ```

## Como Usar
1. Execute o script:
   ```sh
   python3 app.py
   ```
2. O bot verificará se existem cookies salvos. Se não houver, ele fará login no LinkedIn e salvará os cookies.
3. Ele acessará o feed do LinkedIn, lerá o primeiro post e gerará um comentário com a API da OpenAI.
4. O bot publicará automaticamente o comentário e atualizará a página a cada 10 segundos para interagir com novas postagens.

## Estrutura do Projeto
```
/
├── bot.py            # Script principal
├── requirements.txt  # Dependências do projeto
├── secret.py             # Credenciais (NÃO COMITE ESTE ARQUIVO)
└── linkedin_cookies.pkl  # Cookies salvos para login automático
```

## Possíveis Problemas e Soluções
### 1. Chrome não encontrado
Se o bot exibir a mensagem "Chrome binary not found in common locations.", instale o Google Chrome ou edite o caminho no código.

### 2. Login falha
Se o login falhar, apague o arquivo `linkedin_cookies.pkl` e execute o bot novamente para refazer a autenticação.

### 3. Erro ao gerar comentário
Se a API da OpenAI falhar, verifique se sua chave `OPENAI_API_KEY` está correta e se você tem créditos suficientes.

## Aviso Legal
Este bot automatiza interações no LinkedIn e pode violar os termos de uso da plataforma. Use por sua conta e risco.
