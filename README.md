# HyperReal_GambleSimulator-Discord
부스타빗과 비슷한 해시 알고리즘으로 만들어진 디스코드 봇 입니다.
단순히 숫자 넣으면 랜덤 값 계산해서 결과 값 출력하는 프로그램입니다.

## 이 코드는 그 어떠한 나쁜 의도 없이 쓰여진 코드입니다. 친구들과 있는 서버에서 재미용으로만 사용 해주세요.

### 사용한 추가 패키지
```discord.py, statistics```

## 작동 원리
랜덤한 sha256 해시를 생성 후, 그 값에서 출력 값과 다음 해시 값을 뽑아내어 결과를 반환합니다.
