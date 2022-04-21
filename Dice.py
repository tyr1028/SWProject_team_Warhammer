import random

def dice(number_of_dice = 1, type = "default"):
    dice_result_list = []

    for _ in range(number_of_dice):
            dice_result = random.randint(1, 6)
            dice_result_list.append(dice_result)

    if type == "2d3":
        dice_2d3_result_list = []
        for i in dice_result_list:
            dice_2d3_result_list.append((i-1)//2 +1)
        result = "2d3룰에 의해" + str(dice_2d3_result_list) + "가 나왔습니다(주사위:" + dice_result_list +")" 
        print(result)

        return dice_2d3_result_list
    
    else:
        result = "주사위" + str(dice_result_list) + "가 나왔습니다"
        print(result)

        return dice_result_list
