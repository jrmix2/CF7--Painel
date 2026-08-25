# CF7 Painel Online

Primeira versão pronta para hospedagem.

## O que já funciona
- Bancas por casa
- Depósitos, saques e transferências
- Cadastro e finalização Green/Red/Anulada
- Gestão de unidade e risco
- Meta mensal e stop diário
- Gráfico e desempenho por casa
- Importação de print via IA (backend)

## Rodar no computador
1. Instale Python 3.11+
2. `pip install -r requirements.txt`
3. Configure a variável `OPENAI_API_KEY`
4. `uvicorn app:app --host 0.0.0.0 --port 8000`
5. Abra `http://localhost:8000`

## Importante
A chave da API fica somente no servidor. Nunca coloque a chave dentro do HTML/JavaScript público.

## Próximo passo
Hospedar em um serviço que execute Python e configurar a variável de ambiente OPENAI_API_KEY.
Depois, trocar localStorage por banco de dados + login para acessar os mesmos dados em qualquer aparelho.
