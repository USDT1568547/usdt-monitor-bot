import os
import requests
import time

# ✅ 환경변수에서 정보 가져오기 (GitHub Secrets에서 설정)
USDT_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
WALLET_ADDRESS = os.environ['WALLET_ADDRESS']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# ✅ USDT 입금 확인 함수
def check_usdt_deposit(wallet_address):
    url = f'https://apilist.tronscanapi.com/api/transaction?address={wallet_address}&limit=10'
    response = requests.get(url)
    data = response.json()

    for tx in data.get('data', []):
        if tx.get('contractType') == 'TriggerSmartContract':
            if tx.get('tokenInfo', {}).get('address') == USDT_CONTRACT_ADDRESS:
                sender = tx['ownerAddress']
                amount = int(tx['amount']) / 1_000_000
                message = f"🚀 [USDT 입금 감지] 🚀\n\n"
                message += f"📌 보낸 주소: {sender}\n"
                message += f"💰 입금 금액: {amount} USDT\n"
                message += f"🔍 확인 링크: https://tronscan.org/#/address/{wallet_address}"
                
                send_telegram_alert(message)

# ✅ 텔레그램 메시지 전송 함수
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=params)

# ✅ 10초마다 실행 (주기적 모니터링)
while True:
    check_usdt_deposit(WALLET_ADDRESS)
    time.sleep(10)
