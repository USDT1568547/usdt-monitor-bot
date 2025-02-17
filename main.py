import os
import requests
import time

# ✅ 환경 변수에서 정보 가져오기
USDT_CONTRACT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# ✅ 환경 변수 확인
print("WALLET_ADDRESS:", WALLET_ADDRESS)
print("TELEGRAM_BOT_TOKEN:", TELEGRAM_BOT_TOKEN)
print("CHAT_ID:", CHAT_ID)

# ✅ USDT 입금 확인 함수
def check_usdt_deposit(wallet_address):
    url = f'https://apilist.tronscanapi.com/api/transaction?address={wallet_address}&limit=10'
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()
        
        # API 응답 출력 (디버깅용)
        print("API 응답:", data)

    except requests.RequestException as e:
        print(f"⚠️ API 요청 실패: {e}")
        return

    for tx in data.get('data', []):
        if tx.get('contractType') == 'TriggerSmartContract':
            token_info = tx.get('tokenInfo', {})
            if token_info.get('address') == USDT_CONTRACT_ADDRESS:
                receiver = tx.get('transferToAddress')  # 수신자 주소
                sender = tx.get('ownerAddress')  # 발신자 주소
                amount = int(tx.get('amount', 0)) / 1_000_000  # USDT 단위 변환
                
                # 내 지갑으로 들어온 트랜잭션인지 확인
                if receiver.lower() == wallet_address.lower():
                    message = (
                        f"🚀 [USDT 입금 감지] 🚀\n\n"
                        f"📌 보낸 주소: {sender}\n"
                        f"💰 입금 금액: {amount} USDT\n"
                        f"🔍 확인 링크: https://tronscan.org/#/address/{wallet_address}"
                    )
                    send_telegram_alert(message)

# ✅ 텔레그램 메시지 전송 함수
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # HTTP 오류 체크
        
        # 텔레그램 메시지 응답 출력 (디버깅용)
        print("텔레그램 응답:", response.text)
        
        print("✅ 알림 전송 성공")
    except requests.RequestException as e:
        print(f"⚠️ 텔레그램 메시지 전송 실패: {e}")

# ✅ 10초마다 실행 (주기적 모니터링)
if __name__ == "__main__":
    print("🚀 USDT 모니터링 봇 시작!")
    while True:
        check_usdt_deposit(WALLET_ADDRESS)
        time.sleep(30)  # 10초에서 30초로 간격 조정
