import random


class Game:
    def __init__(self):
        self.card = Card()
        self.player = Player()
        self.dealer = Dealer()
        self.prestart()

    def prestart(self):
        for _ in range(2):
            self.player.action("d", self.card)
            self.dealer.action("d", self.card)
        print("you : ", self.player.real_sum())
        print("dea's first : ", self.dealer.have_card[0])

    def start(self):
        self.player.turn(self.card)
        self.dealer.turn(self.card)

        pp = self.player.real_sum()
        dd = self.dealer.real_sum()

        print(self.player.have_card)
        print("you : ", pp)
        print(self.dealer.have_card)
        print("dea : ", dd)
        if (pp > dd):
            print("you win!")
        elif (pp < dd):
            print("you lose!")
        else:
            print("even")


class Gamemate:
    def __init__(self):
        self.have_card = []
        self.order = set(["d", "r", "f"])
        self.overs = set([11, 12, 13])

    def action(self, action, card):
        if (action in self.order):
            if (action == "d"):
                self.have_card.append(card.draw_card())
                if self.real_sum() > 21:
                    print("you lose")
                    exit()
            elif (action == "r"):
                print("you lose!")
            elif (action == "f"):
                self.finish()

    def finish(self):
        print(self.real_sum())

    def real_sum(self):
        real_card = [11 if n > 10 else n for n in self.have_card]
        if(sum(real_card) > 21):
            for i, num in enumerate(self.have_card):
                if num in self.overs:
                    real_card[i] = 1
                    if(sum(real_card) > 21):
                        continue
                    break
        return sum(real_card)


class Player(Gamemate):
    def turn(self, card):
        while True:
            playeraction = input("what do you want to do next? : ")
            if playeraction == "f":
                break
            self.action(playeraction, card)
            print(self.have_card)
            print("you : ", self.real_sum())


class Dealer(Gamemate):
    def turn(self, card):
        while True:
            self.action(self.autoaction(), card)
            if self.real_sum() > 21:
                print("dealer did bankrupt!")
                break
            if self.real_sum() >= 17:
                break

    def autoaction(self):
        return "d"


class Card:
    def __init__(self):
        self.remain_cards = [0] * 13

    def draw_card(self):
        self.card = 0
        while True:
            self.card = random.randint(1, 13)
            if self.remain_cards[self.card - 1] < 4:
                self.remain_cards[self.card - 1] += 1
                return self.card


game = Game()
game.start()
