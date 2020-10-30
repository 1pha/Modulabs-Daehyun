import random
import matplotlib.pyplot as plt

doors = [1, 2, 3]

no_change = 0 # 문을 바꾸지 않은 경우
change = 0 # 문을 바꾼 경우

trial = int(input()) # 시행횟수

for _ in range(trial):

    # 10억이 있는 곳
    prize = random.randint(0, 2)

    # 참가자가 고른 문
    player_choice = random.randint(0, 2)

    empty_door = []
    for door in range(3):

        # 참가자가 선택하지 않았으면서 염소가 있는 문
        # 즉, 사회자가 선택할 수 있는 문의 후보를 만드는 것
        if door != player_choice and door != prize:
            empty_door.append(doors[door])


    # 사회자가 선택한 문
    com = random.sample(empty_door, 1)[0]

    # 만약 플레이어가 고른 곳이 실제로 상품이 있던 경우
    # 그리고 플레이어가 문을 바꾸지 않은 경우
    if player_choice == prize:
        no_change += 1

    # 문을 열 수 있는 후보 군이 애초에 한 개라면
    # 한 개는 사회자가 보여줬고, 한 개는 상품이 있어서 못 고르고, 한 개는 내가 골랐다는 뜻
    # 즉 내가 고른 건 염소, 그니까 바꿨어야한다는 게 답
    if len(empty_door) == 1:
        change += 1

plt.title(f'With trials of {trial}')
plt.bar(['No Change', 'Change'], [no_change, change])
plt.grid()
plt.show()