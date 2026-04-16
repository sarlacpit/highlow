#!/usr/bin/env python3
"""
MC-COIN HIGH-LOW CARD CHALLENGE  —  RETRO ARCADE EDITION
"""

import random
import time
import sys
import os

# ── ANSI colour palette ────────────────────────────────────────────────────────
R    = '\033[91m'
G    = '\033[92m'
Y    = '\033[93m'
B    = '\033[94m'
M    = '\033[95m'
C    = '\033[96m'
W    = '\033[97m'
BOLD = '\033[1m'
DIM  = '\033[2m'
RESET= '\033[0m'

# ── Deck setup ─────────────────────────────────────────────────────────────────
SUITS  = ['♠', '♥', '♦', '♣']
RANKS  = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
VALUES = {r: i + 2 for i, r in enumerate(RANKS)}   # 2→2 … A→14

def create_deck():
    deck = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck

def suit_color(suit):
    return R if suit in ('♥', '♦') else C

# ── ASCII card renderer ────────────────────────────────────────────────────────
CARD_BACK = [
    "┌─────────┐",
    "│ ▓ ▓ ▓ ▓ │",
    "│ ▓ ▓ ▓ ▓ │",
    "│ ▓ ▓ ▓ ▓ │",
    "│ ▓ ▓ ▓ ▓ │",
    "│ ▓ ▓ ▓ ▓ │",
    "└─────────┘",
]

def card_lines(card):
    """Return 7 plain strings for a face-up card."""
    rank, suit = card
    tl = rank.ljust(2)
    br = rank.rjust(2)
    return [
        "┌─────────┐",
        f"│{tl}       │",
        "│         │",
        f"│    {suit}    │",
        "│         │",
        f"│       {br}│",
        "└─────────┘",
    ]

def print_two_cards(left_card, right_card, right_hidden=False):
    """Print two cards side-by-side with ANSI colour."""
    llines = card_lines(left_card)
    rlines = CARD_BACK if right_hidden else card_lines(right_card)

    lcol = suit_color(left_card[1])
    rcol = DIM + M if right_hidden else suit_color(right_card[1])

    print()
    for l, r in zip(llines, rlines):
        print(f"    {lcol}{l}{RESET}   {rcol}{r}{RESET}")
    print()

# ── UI helpers ─────────────────────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewrite(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pause():
    print(f"\n  {DIM}[ PRESS ENTER TO CONTINUE ]{RESET}", end='')
    input()

def hbar(char='═', width=50, color=M):
    print(f"  {color}{BOLD}{char * width}{RESET}")

# ── Score display ──────────────────────────────────────────────────────────────
def scoreboard(p_name, p_coins, cpu_coins, bank=100):
    hbar('─', 46, C)
    def bar(coins):
        filled = max(0, min(20, round(coins / bank * 20)))
        return f"{'█'*filled}{'░'*(20-filled)}"
    print(f"  {G}{BOLD}{p_name:<14}{RESET}  {Y}{bar(p_coins)}{RESET}  {Y}{p_coins:>5} ₥{RESET}")
    print(f"  {R}{BOLD}{'COMPUTER':<14}{RESET}  {M}{bar(cpu_coins)}{RESET}  {Y}{cpu_coins:>5} ₥{RESET}")
    hbar('─', 46, C)
    print()

# ── Result FX ─────────────────────────────────────────────────────────────────
def fx_win(bet):
    print(f"\n  {G}{BOLD}╔══════════════════════════════════╗{RESET}")
    print(f"  {G}{BOLD}║   ★  CORRECT!  +{bet:<5} McCoins  ★  ║{RESET}")
    print(f"  {G}{BOLD}╚══════════════════════════════════╝{RESET}")
    print(f"  {Y}   ♪  ding  ding  ding  ♪{RESET}\n")

def fx_lose(bet):
    print(f"\n  {R}{BOLD}╔══════════════════════════════════╗{RESET}")
    print(f"  {R}{BOLD}║   ✗  WRONG!   -{bet:<5} McCoins  ✗  ║{RESET}")
    print(f"  {R}{BOLD}╚══════════════════════════════════╝{RESET}")
    print(f"  {M}   ♩  wah  wah  wahhh  ♩{RESET}\n")

def fx_tie():
    print(f"\n  {Y}{BOLD}╔══════════════════════════════════╗{RESET}")
    print(f"  {Y}{BOLD}║   ◈   PUSH!   IT'S A TIE!   ◈   ║{RESET}")
    print(f"  {Y}{BOLD}╚══════════════════════════════════╝{RESET}\n")

# ── Input helpers ──────────────────────────────────────────────────────────────
def get_bet(player_coins):
    while True:
        print(f"  {C}How many McCoins do you wager?  {DIM}(1 – {player_coins}){RESET}")
        raw = input(f"  {W}BET ₥:{Y} ").strip()
        if raw.isdigit():
            bet = int(raw)
            if 1 <= bet <= player_coins:
                return bet
        print(f"  {R}Invalid bet. Enter a whole number between 1 and {player_coins}.{RESET}")

def get_guess():
    while True:
        print(f"  {C}Will the NEXT card be:{RESET}")
        print(f"    {G}[H]{RESET} Higher      {R}[L]{RESET} Lower      {Y}[Q]{RESET} Quit")
        ch = input(f"  {W}CALL:{Y} ").strip().upper()
        if ch in ('H', 'L', 'Q'):
            return ch
        print(f"  {R}Press H, L, or Q!{RESET}")

# ── Screens ────────────────────────────────────────────────────────────────────
def title_screen():
    clear()
    print(f"""
{M}{BOLD}  ╔════════════════════════════════════════════════════╗
  ║                                                    ║
  ║  {Y}  __  __  ____     ____  ___  ___  _  _  {M}         ║
  ║  {Y} |  \/  |/ ___|   / ___|/ _ \|_ _|| \| | {M}         ║
  ║  {Y} | |\/| | |      | |  | | | | | | |  \ | {M}         ║
  ║  {Y} | |  | | |___   | |__| |_| | | | | |\ | {M}         ║
  ║  {Y} |_|  |_|\____|   \____\___/ |___||_| \_| {M}         ║
  ║                                                    ║
  ║     {C}H I G H  —  L O W   C H A L L E N G E{M}         ║
  ║                                                    ║
  ║           {W}★  RETRO ARCADE EDITION  ★{M}              ║
  ║                                                    ║
  ╚════════════════════════════════════════════════════╝{RESET}
""")
    time.sleep(0.3)
    typewrite(f"  {Y}{BOLD}[ INSERT MCCOIN TO PLAY ]{RESET}", delay=0.06)
    time.sleep(0.5)

def round_header(p_name, p_coins, cpu_coins, round_num, bank):
    clear()
    hbar('═', 50)
    print(f"  {Y}{BOLD}  MC-COIN HIGH-LOW  ·  {p_name}  ·  ROUND {round_num}{RESET}")
    hbar('═', 50)
    print()
    scoreboard(p_name, p_coins, cpu_coins, bank)

def game_over_screen(winner, p_name, p_coins, cpu_coins):
    clear()
    if winner == 'player':
        print(f"""
{G}{BOLD}
  ╔══════════════════════════════════════════════╗
  ║                                              ║
  ║   {Y}  ★ ★ ★   Y O U   W I N !   ★ ★ ★  {G}   ║
  ║                                              ║
  ║      {W}The computer is totally BANKRUPT!{G}     ║
  ║      {C}You cleaned out the house!{G}             ║
  ║                                              ║
  ║   {Y}  FINAL:  {p_name}  =  {p_coins} McCoins ₥{G}        ║
  ║                                              ║
  ╚══════════════════════════════════════════════╝
{RESET}""")
    else:
        print(f"""
{R}{BOLD}
  ╔══════════════════════════════════════════════╗
  ║                                              ║
  ║   {Y}  ✗ ✗ ✗  G A M E  O V E R  ✗ ✗ ✗  {R}    ║
  ║                                              ║
  ║      {W}You have been utterly RUINED!{R}          ║
  ║      {M}The computer reigns supreme!{R}            ║
  ║                                              ║
  ║   {Y}  COMPUTER FINAL:  {cpu_coins} McCoins ₥{R}          ║
  ║                                              ║
  ╚══════════════════════════════════════════════╝
{RESET}""")

# ── Main game loop ─────────────────────────────────────────────────────────────
def play():
    title_screen()

    print(f"\n  {C}ENTER YOUR NAME, CHALLENGER:{RESET}")
    raw_name = input(f"  {Y}> {RESET}").strip()
    p_name = (raw_name[:12] or "PLAYER 1").upper()

    BANK      = 100
    p_coins   = BANK
    cpu_coins = BANK

    print(f"\n  {G}{BOLD}Welcome, {p_name}!{RESET}")
    typewrite(f"  {W}Both players start with {Y}{BANK} McCoins ₥{W}.{RESET}", delay=0.03)
    typewrite(f"  {M}Guess higher or lower and bet your McCoins!{RESET}", delay=0.03)
    time.sleep(0.8)

    deck      = create_deck()
    current   = deck.pop()
    round_num = 1

    while p_coins > 0 and cpu_coins > 0:

        # Reshuffle when deck runs low
        if len(deck) < 2:
            deck = create_deck()
            typewrite(f"\n  {Y}♻  DECK RESHUFFLED!  ♻{RESET}", delay=0.04)
            current = deck.pop()

        # ── Round header
        round_header(p_name, p_coins, cpu_coins, round_num, BANK)

        # Show current card on left, face-down mystery card on right
        r, s = current
        col  = suit_color(s)
        print(f"  {W}CURRENT CARD:                  NEXT CARD:{RESET}")
        print_two_cards(current, current, right_hidden=True)
        print(f"  {col}{BOLD}  {r} of {s}   (value: {VALUES[r]}){RESET}\n")

        # ── Betting
        print(f"  {Y}──────  PLACE YOUR BET  ──────{RESET}")
        bet = get_bet(p_coins)

        # ── Guessing
        print(f"\n  {Y}──────  MAKE YOUR CALL  ──────{RESET}")
        guess = get_guess()

        if guess == 'Q':
            typewrite(f"\n  {Y}Thanks for playing, {p_name}! See ya next time!{RESET}", delay=0.04)
            return

        # ── Reveal
        nxt  = deck.pop()
        nr, ns = nxt
        ncol = suit_color(ns)

        print(f"\n  {W}REVEALING NEXT CARD . . .{RESET}")
        time.sleep(0.9)

        round_header(p_name, p_coins, cpu_coins, round_num, BANK)

        print(f"  {W}CURRENT CARD:                  NEXT CARD:{RESET}")
        print_two_cards(current, nxt, right_hidden=False)
        print(f"  {col}{BOLD}  {r} of {s}   (value: {VALUES[r]}){RESET}")
        print(f"  {ncol}{BOLD}  {nr} of {ns}   (value: {VALUES[nr]}){RESET}\n")

        # ── Outcome
        cv, nv = VALUES[r], VALUES[nr]

        if nv == cv:
            fx_tie()
            print(f"  {Y}No McCoins exchanged on a tie!{RESET}")
        elif (guess == 'H' and nv > cv) or (guess == 'L' and nv < cv):
            fx_win(bet)
            p_coins   += bet
            cpu_coins -= bet
            print(f"  {G}You gain {bet} ₥  —  Computer loses {bet} ₥{RESET}")
        else:
            fx_lose(bet)
            p_coins   -= bet
            cpu_coins += bet
            print(f"  {R}You lose {bet} ₥  —  Computer gains {bet} ₥{RESET}")

        p_coins   = max(0, p_coins)
        cpu_coins = max(0, cpu_coins)
        current   = nxt
        round_num += 1

        if p_coins == 0 or cpu_coins == 0:
            break

        pause()

    # ── Game over
    winner = 'player' if cpu_coins <= 0 else 'cpu'
    game_over_screen(winner, p_name, p_coins, cpu_coins)

    print(f"\n  {Y}PLAY AGAIN?  {W}[Y / N]:{RESET} ", end='')
    if input().strip().upper() == 'Y':
        play()
    else:
        print(f"\n  {M}{BOLD}Thanks for playing MC-COIN HIGH-LOW!{RESET}")
        print(f"  {C}  ★  INSERT MCCOIN TO CONTINUE  ★{RESET}\n")


if __name__ == '__main__':
    try:
        play()
    except KeyboardInterrupt:
        print(f"\n\n  {Y}Game aborted. McCoins returned to the abyss.{RESET}\n")
