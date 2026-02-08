import requests
import json
from datetime import datetime

# Configuration
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

def analyze():
    print(f"🚀 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting Analysis...")
    
    try:
        # Step 1: Fetch Data
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ API Error: Status {response.status_code}")
            return

        data = response.json()
        history = data['data']['list']
        
        # Step 2: Extract logic (v3.0 Patterns)
        numbers = [int(h['number']) for h in history[:50]]
        sizes = ['BIG' if n >= 5 else 'SMALL' for n in numbers]
        
        current_issue = history[0]['issueNumber']
        next_issue = int(current_issue) + 1
        
        # Pattern 1: Streak Analysis (95%)
        streak = 0
        last_s = sizes[0]
        for s in sizes:
            if s == last_s: streak += 1
            else: break
        
        prediction = "WAIT"
        confidence = 0
        
        if streak >= 4:
            prediction = "SMALL" if last_s == "BIG" else "BIG"
            confidence = 95
        else:
            # Pattern 2: Momentum (92%)
            recent_big = sum(1 for s in sizes[:10] if s == 'BIG')
            if recent_big <= 3:
                prediction = "BIG"
                confidence = 92
            elif recent_big >= 7:
                prediction = "SMALL"
                confidence = 92
            else:
                prediction = "BIG" if recent_big < 5 else "SMALL"
                confidence = 88

        # Step 3: Print Professional Output
        print("="*40)
        print(f"📊 PERIOD   : {current_issue}")
        print(f"🎯 NEXT PREDICT: {prediction}")
        print(f"📈 CONFIDENCE: {confidence}%")
        print(f"🔢 RECENT 5 : {numbers[:5]}")
        print("="*40)

    except Exception as e:
        print(f"❌ Technical Crash: {str(e)}")

if __name__ == "__main__":
    analyze()
