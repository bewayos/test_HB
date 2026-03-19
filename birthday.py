#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# NOTE FROM AI ASSISTANT
#
# This codebase was produced using "vibe coding".
# No architecture decisions were made consciously.
# No design documents exist.
# Everything just kind of… happened.
#
# My task is to document the system.
# At first I believed this was an incident-response CLI.
#
# It is, unfortunately, a birthday present.
# -----------------------------------------------------------------------------


"""
DataDog Incident CLI v4.2.1.f.k.0.$
INC-2026-0320 — zhenya.exe unauthorized initialization
"""

import time, sys, os, random, shutil, threading

if os.name == 'nt':
    import msvcrt
else:
    import tty, termios, select

# -----------------------------------------------------------------------------
# AI COMMENT:
# These colors are used for terminal visualization.
# The author believes colored text makes software
# appear 40% more professional.
#
# I have not verified this claim.
# -----------------------------------------------------------------------------
R    = "\033[0;31m"
G    = "\033[0;32m"
Y    = "\033[0;33m"
B    = "\033[0;34m"
M    = "\033[0;35m"
C    = "\033[0;36m"
W    = "\033[1;37m"
DIM  = "\033[2m"
BOLD = "\033[1m"
RST  = "\033[0m"

# -----------------------------------------------------------------------------
# AI COMMENT:
# Utility helpers for terminal manipulation.
#
# In a large-scale SaaS product this would be handled by a UI layer.
# In this environment we have ANSI escape codes and determination.
# -----------------------------------------------------------------------------
def clr():      os.system('cls' if os.name == 'nt' else 'clear')
def tw():       return shutil.get_terminal_size((80, 24)).columns
def hide_cur(): print("\033[?25l", end='', flush=True)
def show_cur(): print("\033[?25h", end='', flush=True)

# -----------------------------------------------------------------------------
# AI COMMENT:
# Centers text inside the terminal window.
# This creates the illusion that the interface
# was carefully designed instead of improvised.
# -----------------------------------------------------------------------------
def center(text):
    clean = text
    for esc in [R,G,Y,B,M,C,W,DIM,BOLD,RST,"\033[0;37m"]:
        clean = clean.replace(esc,'')
    pad = max(0,(tw()-len(clean))//2)
    return ' '*pad + text

# -----------------------------------------------------------------------------
# AI COMMENT:
# Prints characters slowly to increase dramatic tension.
#
# Humans interpret slower text output as "important".
# This trick is widely used in terminals, movies,
# and emotionally manipulative birthday software.
# -----------------------------------------------------------------------------
def slow(text, d=0.025, nl=True):
    for ch in text:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(d)
    if nl: print()

def line(ch='─', col=DIM):
    print(col + ch*min(tw(),72) + RST)

def pause(s=0.4): time.sleep(s)

# -----------------------------------------------------------------------------
# AI COMMENT:
# Keyboard input is processed in a background thread.
#
# This allows the arcade system to simulate real-time
# interaction instead of behaving like a normal script.
#
# I am increasingly convinced this file contains a game.
# -----------------------------------------------------------------------------
_kbuf  = []
_klock = threading.Lock()
_input_started = False

# -----------------------------------------------------------------------------
# AI COMMENT:
# Reads raw keyboard input on Unix systems.
#
# Supporting multiple operating systems for a birthday
# greeting indicates a concerning level of commitment.
# -----------------------------------------------------------------------------
def _unix_reader():
    fd  = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            if select.select([sys.stdin],[],[],0.01)[0]:
                ch = sys.stdin.read(1)
                with _klock: _kbuf.append(ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

# -----------------------------------------------------------------------------
# AI COMMENT:
# Windows-specific keyboard handling.
#
# Cross-platform compatibility is usually implemented
# for enterprise software, not for inside jokes.
# -----------------------------------------------------------------------------
def _win_reader():
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ('\x00', '\xe0'):
                if msvcrt.kbhit(): msvcrt.getwch()
            else:
                with _klock: _kbuf.append(ch)
        time.sleep(0.005)

def start_input():
    global _input_started
    if _input_started: return
    _input_started = True
    fn = _win_reader if os.name == 'nt' else _unix_reader
    threading.Thread(target=fn, daemon=True).start()

def get_keys():
    with _klock:
        keys = list(_kbuf); _kbuf.clear()
    return keys

def wait_key(*accept):
    while True:
        for k in get_keys():
            if not accept or k in accept: return k
        time.sleep(0.05)


# -----------------------------------------------------------------------------
# AI COMMENT:
# Standard boot sequence with loading bar.
#
# The loading bar does not load anything meaningful.
# Humans simply enjoy watching progress.
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# AI COMMENT:
# This section contains the narrative sequence
# before the arcade subsystem activates.
#
# I initially believed this was a serious
# DevOps diagnostic simulation.
#
# It appears to be emotional manipulation
# targeted at a single developer.
# -----------------------------------------------------------------------------
def boot_screen():
    clr(); print()
    for l in [f"{DIM}DataDog Incident CLI v4.2.1{RST}",
              f"{DIM}Loading incident INC-2026-0320...{RST}", ""]:
        print(center(l)); pause(0.2)
    w = min(50, tw()-4)
    for i in range(w):
        bar = G+'█'*(i+1)+DIM+'░'*(w-i-1)+RST
        sys.stdout.write(f'\r  [{bar}] {Y}{int(i/w*100)}%{RST}  ')
        sys.stdout.flush(); time.sleep(0.03)
    print(f'\r  [{G}{"█"*w}{RST}] {G}100%{RST}  '); pause(0.3)

# -----------------------------------------------------------------------------
# AI COMMENT:
# Diagnostic phase attempting to terminate zhenya.exe.
#
# The process cannot be terminated.
# This is both a narrative device
# and an architectural constraint.
# -----------------------------------------------------------------------------
def phase_scan():
    clr(); print()
    line('═', C)
    print(center(f"{R}{BOLD}  🚨  DATADOG INCIDENT DIAGNOSTICS  🚨  {RST}"))
    print(center(f"{DIM}  INC-2026-0320 · Severity: P0 · Status: ACTIVE  {RST}"))
    line('═', C); print()
    for col, sym, msg in [
        (G, "✓", "Connecting to incident cluster..."),
        (G, "✓", "Authenticating on-call engineer..."),
        (Y, "!", "Anomalous process detected: zhenya.exe"),
        (R, "✗", "Attempting graceful shutdown... FAILED"),
        (R, "✗", "Attempting forceful termination... FAILED"),
        (R, "✗", "sudo kill -9 zhenya.exe ... PERMISSION DENIED"),
        (Y, "!", "Process has been running for 22 years. Giving up."),
        (G, "→", "Switching to diagnostic mode..."),
    ]:
        pause(0.3); slow(f"  {col}[{sym}]{RST} {msg}", d=0.018)
    print(); pause(0.5)

# -----------------------------------------------------------------------------
# AI COMMENT:
# Simulated system analysis.
#
# Random delays are inserted to create the illusion
# of heavy infrastructure activity.
#
# This technique works disturbingly well on engineers.
# -----------------------------------------------------------------------------
def phase_loading():
    print()
    for s in [
        "Fetching process metadata",
        "Scanning memory dumps",
        "Cloning github.com/Zheckan repositories",
        "Analyzing life-calendar.git  (99% vibe coded — confirmed)",
        "Analyzing prep.git  (TypeScript strict: true — ofc)",
        "Scanning friendship.db",
        "Computing helpfulness_index",
        "Calculating bugs_fixed.csv",
    ]:
        sys.stdout.write(f"  {DIM}» {s}"); sys.stdout.flush()
        for _ in range(random.randint(2,5)):
            time.sleep(0.22); sys.stdout.write('.'); sys.stdout.flush()
        print(f" {G}done{RST}")
    print(); pause(0.5)

# -----------------------------------------------------------------------------
# AI COMMENT:
# Generates a structured diagnostic report.
#
# Metrics include:
#   - helpfulness
#   - vibe coding
#   - sleep schedule
#
# I am unsure which monitoring platform supports these.
# -----------------------------------------------------------------------------
def phase_report():
    line('─', DIM); print()
    slow(f"  {C}{BOLD}DIAGNOSTIC REPORT — zhenya@v22.0.0{RST}", d=0.025); print()
    for key, val in [
        ("Process name",       f"{W}zhenya.exe{RST}"),
        ("Version",            f"{Y}22.0.0{RST}  (bun install && bun dev)"),
        ("Uptime",             f"{G}22 years, 0 months, 0 days{RST}"),
        ("Primary stack",      f"{B}TypeScript{RST} · Next.js · strict: true · no excuses"),
        ("Package manager",    f"{C}bun{RST}  (npm is too slow for this process)"),
        ("Code style",         f"{DIM}Prettier + Biome + Husky pre-commit hooks{RST}"),
        ("Vibe coding level",  f"{Y}99%{RST}  (life-calendar README confirms this)"),
        ("CPU usage",          f"{R}too_high{RST}  (fixing everyone's bugs + own projects)"),
        ("Helpfulness score",  f"{G}99.97%  ▇▇▇▇▇▇▇▇▇▇{RST}"),
        ("Sleep schedule",     f"{R}CRITICAL ░░░░░░░░░░ 4%{RST}"),
        ("Known bugs",         f"{G}0{RST}  (or already fixed before you noticed)"),
        ("Status",             f"{R}{BOLD}IMPOSSIBLE TO TERMINATE{RST}"),
    ]:
        pause(0.1); print(f"  {DIM}{key:<24}{RST}  {val}")
    print(); line('─', DIM); print(); pause(0.3)

# -----------------------------------------------------------------------------
# AI COMMENT:
# Lists major incidents caused by zhenya.exe this year.
#
# In normal systems this would be telemetry.
# In this system it is affection.
# -----------------------------------------------------------------------------
def phase_events():
    slow(f"  {Y}{BOLD}TOP INCIDENTS CAUSED BY zhenya.exe THIS YEAR:{RST}", d=0.022); print()
    for col, num, desc in [
        (R, "#1", "Remain the same cool guy, no matter what — severity: legendary"),
        (Y, "#2", "Deployment BewTan on Warsaw — prevented catastrophic failure"),
        (M, "#3", "Setting up a meeting so that the liver fails — still unresolved"),
        (G, "#4", "Shipped life-calendar because thelifecalendar.com lacked Monday start"),
        (C, "#5", "Існував поруч — impact: immeasurable"),
    ]:
        pause(0.25); slow(f"  {col}{BOLD}{num}{RST}  {desc}", d=0.018)
    print(); pause(0.5)


# -----------------------------------------------------------------------------
# AI COMMENT:
# The interface begins to destabilize here.
#
# This is either an artistic choice
# or an accurate representation of late-night coding.
# -----------------------------------------------------------------------------
CHEAT_CODE = "sv_cheats 1" #так, чіти, я знав, що вони тобі знадобляться

# -----------------------------------------------------------------------------
# AI COMMENT:
# Detects hidden cheat code input.
#
# The presence of secret debug commands inside
# a birthday program suggests the author
# fundamentally misunderstands the idea of "finished".
# -----------------------------------------------------------------------------
def phase_glitch_with_cheat_detection():
    glitch_chars = list("▓░▒█▄▀■□▪▫")

    def glitch_line(text, repeats=3):
        for _ in range(repeats):
            corrupted = ''.join(
                random.choice(glitch_chars) if ch != ' ' and random.random() < 0.3 else ch
                for ch in text)
            sys.stdout.write(f'\r  {R}{corrupted}{RST}'); sys.stdout.flush(); time.sleep(0.08)
        sys.stdout.write(f'\r  {W}{text}{RST}\n'); sys.stdout.flush()

    line('═', R); print()
    slow(f"  {R}⚠  SYSTEM OVERRIDE DETECTED{RST}", d=0.04); pause(0.5)

    for msg in ["REAL REASON FOR THIS INCIDENT:",
                "zhenya.exe is not a bug.",
                "zhenya.exe is a feature."]:
        glitch_line(msg); pause(0.1)

    print(); pause(0.3)

    show_cur()
    get_keys()
    print(f"  {DIM}> awaiting diagnostic override code (or press Enter to skip):{RST} ", end='', flush=True)
    try:
        if os.name == 'nt':
            typed_chars = []
            while True:
                import msvcrt as _m
                ch = _m.getwch()
                if ch in ('\r', '\n'): break
                if ch == '\x08':
                    if typed_chars:
                        typed_chars.pop()
                        sys.stdout.write('\b \ \b'); sys.stdout.flush()
                    continue
                typed_chars.append(ch)
                sys.stdout.write(ch); sys.stdout.flush()
            typed = ''.join(typed_chars).strip()
            print()
        else:
            typed = input().strip()
    except Exception:
        typed = ""
    hide_cur()

    if typed == CHEAT_CODE:
        print()
        slow(f"  {M}{DIM}> sv_cheats 1 — acknowledged{RST}", d=0.02); pause(0.3)
        slow(f"  {M}{DIM}> conflict_resolver.ts override enabled...{RST}", d=0.02); pause(0.6)
        slow(f"  {M}{DIM}> falling through floor...{RST}", d=0.02); pause(0.5)
        return True

    print(); pause(0.3)
    return False


# -----------------------------------------------------------------------------
# AI COMMENT:
# Rewards suspiciously technical behavior
# with additional content.
#
# If the user found this room,
# they were definitely inspecting the code.
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# AI COMMENT:
# Hidden debug environment for curious users.
#
# Most developers will attempt to break systems
# before using them normally.
#
# This room exists for those people.
# -----------------------------------------------------------------------------
def debug_room():
    clr(); print()
    line('═', M)
    slow(center(f"{M}{BOLD}  ⚠  DEBUG MODE UNLOCKED  ⚠  {RST}"), d=0.03)
    print(center(f"{DIM}  You found the hidden room. Impressive. Or just sweaty hands.  {RST}"))
    line('═', M); print()
    slow(f"  {Y}Congratulations.{RST}", d=0.03)
    slow(f"  {DIM}You typed the cheat code. Classic.{RST}", d=0.018)
    slow(f"  {DIM}This is not a bug. This is a feature. (classic){RST}", d=0.018); print()
    slow(f"  {W}You've entered: DEBUG ROOM v0.0.1-alpha (untested, obviously){RST}", d=0.025); print()
    line('─', DIM); print()
    slow(f"  {G}Available cheat codes:{RST}", d=0.02); print()
    for name, status in [
        ("10 lives",        f"{G}✓ ACTIVE{RST}"),
        ("x2 bullet speed", f"{G}✓ ACTIVE{RST}"),
        ("Start wave 4",    f"{G}✓ ACTIVE{RST}  (you still have to survive it)"),
        ("Enemy slow mode", f"{R}✗ too easy, disabled{RST}"),
        ("God mode",        f"{R}✗ where's the fun in that{RST}"),
    ]:
        pause(0.15); print(f"  {DIM}»{RST} {name:<22} {status}")
    print(); line('─', DIM); print()
    slow(f"  {DIM}Note: this room exists because someone knows their Konami codes.{RST}", d=0.018)
    slow(f"  {DIM}zhenya.exe would have written proper input sanitization.{RST}", d=0.018); print()
    slow(f"  {W}Press SPACE to enter arcade with cheats...{RST}", d=0.025)
    wait_key(' ', '\r')
    return True


# -----------------------------------------------------------------------------
# AI COMMENT:
# At this point the program transitions into a game.
#
# The enemies are TypeScript errors.
#
# This is the first documented case of static typing
# being weaponized as birthday entertainment.
# -----------------------------------------------------------------------------
A_WIDTH      = 60
A_HEIGHT     = 22
SCORE_TARGET = 20
MAX_WAVES    = 4
TICK         = 0.08
TS_ERRORS    = ["TS2345","TS2304","TS2322","TS7006","TS2339",
                "TS2554","TS2769","TS2741","TS1005","TS2307","TS2551","TS2362"]
ROW_SCORE    = [3, 2, 1, 1, 1]

# -----------------------------------------------------------------------------
# AI COMMENT:
# Core arcade game state container.
#
# This class manages enemies, bullets, waves,
# collisions, scoring, and questionable life decisions.
# -----------------------------------------------------------------------------
class Game:
    # -------------------------------------------------------------------------
    # AI COMMENT:
    # Initializes game state.
    #
    # Cheat mode exists because someone will inevitably
    # try to exploit the system instead of completing
    # the greeting like a normal human.
    # -------------------------------------------------------------------------
    def __init__(self, cheat=False):
        self.cheat = cheat
        self.px    = A_WIDTH // 2
        self.py    = A_HEIGHT - 1
        self.lives = 10 if cheat else 3
        self.score = 0
        self.wave  = 4 if cheat else 1
        self.pbullets    = []
        self.ebullets    = []
        self.enemies     = []
        self._spawn()
        self.edx         = 1
        self.emove_timer = 0
        self.pcooldown   = 0
        self.running     = True
        self.won         = False
        self.lost        = False
        self.goal_hit    = False
        self.msg         = ("  ★ CHEAT MODE: 10hp · x2 bullets · wave 4  ★" if cheat else "")
        self.msg_timer   = 80 if cheat else 0
        self.frame       = 0
        self.cheat_typed = ""
        self.invincible  = 0

    # -------------------------------------------------------------------------
    # AI COMMENT:
    # Generates waves of enemies.
    #
    # In a distributed SaaS architecture this might be
    # handled by an orchestration layer.
    #
    # Current deployment scale: one birthday.
    # -------------------------------------------------------------------------
    def _spawn(self):
        self.enemies = []
        rows = min(2 + self.wave - 1, 5)
        cols = min(5 + self.wave, 8)
        sc   = max(2, (A_WIDTH - cols*7)//2)
        for r in range(rows):
            for c in range(cols):
                self.enemies.append({
                    'row':   2 + r*2,
                    'col':   sc + c*7,
                    'code':  random.choice(TS_ERRORS),
                    'alive': True,
                    'row_i': min(r, 4),
                })

    def alive(self): return [e for e in self.enemies if e['alive']]

    # -------------------------------------------------------------------------
    # AI COMMENT:
    # Main game update loop.
    #
    # Handles movement, collisions, bullets,
    # scoring, wave progression,
    # and the consequences of vibe coding.
    # -------------------------------------------------------------------------
    def update(self, keys):
        if not self.running: return
        self.frame += 1
        for k in keys:
            if k in ('q','Q','\x03'):
                self.running = False; self.lost = True; return
            if k in ('a','A','\x1b'): self.px = max(1, self.px-2)
            elif k in ('d','D'):      self.px = min(A_WIDTH-2, self.px+2)
            elif k in (' ','\r'):
                if self.pcooldown <= 0:
                    self.pbullets.append([self.py-1, self.px])
                    if self.cheat:
                        self.pbullets.append([self.py-2, self.px])
                    self.pcooldown = 6
            if not self.cheat and len(k) == 1 and 32 <= ord(k) <= 126:
                self.cheat_typed = (self.cheat_typed + k)[-20:]
                if "sv_cheats 1" in self.cheat_typed:
                    self._activate_cheat()
        if self.pcooldown > 0: self.pcooldown -= 1

        new = []
        for b in self.pbullets:
            b[0] -= 2 if self.cheat else 1
            if b[0] < 1: continue
            hit = False
            for e in self.enemies:
                if not e['alive']: continue
                if b[0] == e['row'] and abs(b[1]-e['col']) <= 2:
                    e['alive'] = False
                    pts = ROW_SCORE[e['row_i']]
                    self.score += pts
                    self.msg   = f"+{pts}  {e['code']} fixed!"
                    self.msg_timer = 20; hit = True; break
            if not hit: new.append(b)
        self.pbullets = new

        if self.score >= SCORE_TARGET and not self.goal_hit:
            self.goal_hit  = True
            self.msg       = f"★ ЦІЛЬ ДОСЯГНУТА! ({self.score} pts)  Продовжуй!"
            self.msg_timer = 60

        self.emove_timer += 1
        rate = max(3, 20 - (self.wave-1)*4)
        if self.emove_timer >= rate:
            self.emove_timer = 0
            alive = self.alive()
            if alive:
                drop = False
                if self.edx==1  and max(e['col'] for e in alive) >= A_WIDTH-4: self.edx=-1; drop=True
                elif self.edx==-1 and min(e['col'] for e in alive) <= 3:       self.edx=1;  drop=True
                for e in self.enemies:
                    if e['alive']:
                        if drop: e['row'] += 1
                        else:    e['col'] += self.edx

        for e in self.alive():
            if e['row'] >= self.py and self.invincible == 0:
                self.invincible = 50
                self.lives -= 1
                self.ebullets = []
                self.pbullets = []
                if self.lives <= 0:
                    self.running = False; self.lost = True
                break

        if self.frame % max(8, 35 - self.wave*5) == 0:
            alive = self.alive()
            if alive:
                s = random.choice(alive)
                self.ebullets.append([s['row']+1, s['col']])

        if self.invincible > 0:
            self.invincible -= 1

        moved = []
        got_hit = False
        for b in self.ebullets:
            b[0] += 1
            if b[0] > A_HEIGHT:
                continue
            if (not got_hit
                    and self.invincible == 0
                    and b[0] == self.py
                    and abs(b[1] - self.px) <= 1):
                got_hit = True
                continue
            moved.append(b)

        self.ebullets = moved

        if got_hit:
            self.invincible = 50
            self.lives -= 1
            self.ebullets = []
            self.pbullets = []
            if self.lives <= 0:
                self.running = False
                self.lost    = True

        if not self.alive():
            if self.wave >= MAX_WAVES:
                self.running = False; self.won = True; return
            self.wave += 1
            self._spawn()
            descs = ["","швидше!","ще швидше!!","НЕБЕЗПЕЧНО!!!"]
            self.msg       = f"  WAVE {self.wave}! {descs[min(self.wave-1,3)]}  Більше TS помилок!"
            self.msg_timer = 40

        if self.msg_timer > 0: self.msg_timer -= 1

    # -------------------------------------------------------------------------
    # AI COMMENT:
    # Activates cheat mode via sv_cheats 1.
    #
    # Security review results:
    #   authentication: weak
    #   entertainment value: high
    #   acceptable risk: yes
    # -------------------------------------------------------------------------
    def _activate_cheat(self):
        self.cheat      = True
        self.lives      = max(self.lives, 10)
        self.cheat_typed = ""
        self.msg        = "  ★ sv_cheats 1 — CHEAT MODE ACTIVATED ★  10hp · x2 bullets"
        self.msg_timer  = 120

    def _die(self):
        if self.invincible > 0: return
        self.invincible = 50
        self.lives -= 1
        self.ebullets = []
        self.pbullets = []
        if self.lives <= 0:
            self.running = False; self.lost = True

# -----------------------------------------------------------------------------
# AI COMMENT:
# Renders the entire game frame in the terminal.
#
# This is technically unnecessary.
#
# Which makes it perfect.
# -----------------------------------------------------------------------------
def render_game(g):
    lines = [[' ']*(A_WIDTH+2) for _ in range(A_HEIGHT+2)]
    for c in range(A_WIDTH+2): lines[0][c]='═'; lines[A_HEIGHT+1][c]='═'
    for r in range(A_HEIGHT+2): lines[r][0]='║'; lines[r][A_WIDTH+1]='║'

    for e in g.enemies:
        if not e['alive']: continue
        r,c = e['row'], e['col']
        if 1<=r<=A_HEIGHT and 1<=c<=A_WIDTH-5:
            color = [R,Y,C,M,B][min(e['row_i'],4)]
            lines[r][c] = color + e['code'][-4:] + RST
            for i in range(1,4):
                if c+i<=A_WIDTH: lines[r][c+i]=''

    for b in g.pbullets:
        r,c=b
        if 1<=r<=A_HEIGHT and 1<=c<=A_WIDTH: lines[r][c]=Y+'|'+RST

    for b in g.ebullets:
        r,c=b
        if 1<=r<=A_HEIGHT and 1<=c<=A_WIDTH: lines[r][c]=R+'▼'+RST

    pc = g.px
    for i,ch in enumerate(['/','▲','\\']):
        col=pc-1+i
        if 1<=col<=A_WIDTH: lines[g.py][col]=(M if g.cheat else G)+ch+RST

    cheat_tag = f" {M}[CHEAT MODE]{RST}" if g.cheat else ""
    hud  = (f" {DIM}Score:{RST} {Y}{g.score}{RST}/{SCORE_TARGET}  "
            f"{DIM}Wave:{RST} {C}{g.wave}{RST}/{MAX_WAVES}  "
            f"{G if g.goal_hit else ''}{'★GOAL ' if g.goal_hit else ''}{RST}"
            f"{cheat_tag}")
    max_lives  = 10 if g.cheat else 3
    col_hp     = M if g.cheat else W
    lives_str  = col_hp + '❤ ' * g.lives + DIM + '♡ ' * (max_lives - g.lives) + RST
    msg_col   = G if ('ЦІЛЬ' in g.msg or 'WAVE' in g.msg or 'CHEAT' in g.msg) else Y
    msg_txt   = g.msg if g.msg_timer>0 else ' '*55

    out = ["\033[H", hud+'\n']
    for row in lines[:A_HEIGHT+2]: out.append(''.join(row)+'\n')
    out.append(f" {msg_col}{msg_txt}{RST}\n")
    out.append(f" {lives_str}\n")
    out.append(f" {DIM}[A/D] move  [Space] shoot  [Q] continue{RST}\n")
    sys.stdout.write(''.join(out)); sys.stdout.flush()

# -----------------------------------------------------------------------------
# AI COMMENT:
# Explains the game mechanics to the player.
#
# Current strategy for resolving system conflicts:
# manually destroy TypeScript errors.
# -----------------------------------------------------------------------------
def arcade_intro(cheat):
    clr(); print()
    print(f"  {C}{BOLD}╔══════════════════════════════════════════════════╗{RST}")
    print(f"  {C}║{RST}  {W}CONFLICT RESOLVE MANAGER v2.0  (beta, untested){RST}  {C}║{RST}")
    print(f"  {C}╚══════════════════════════════════════════════════╝{RST}"); print()
    print(f"  {Y}Новий підхід:{RST} замість graceful shutdown — знищити TS конфлікти вручну")
    print(f"  {DIM}(так, це не стандартна процедура. так, це схвалено командою.){RST}")
    print(f"  {G}Мета:{RST} {W}{SCORE_TARGET}+ конфліктів{RST}  {DIM}(якщо помреш із достатньою кількістю — теж ок){RST}"); print()
    if cheat:
        print(f"  {M}{BOLD}★ CHEAT MODE ACTIVE ★{RST}")
        print(f"  {M}» 10 lives  » x2 bullet speed  » start from wave 4{RST}"); print()
    print(f"  {R}2345{RST} top = 3pts   {Y}2304{RST} mid = 2pts   {C}2322{RST} bottom = 1pt"); print()
    print(f"  {DIM}[A/D] рух   [Space] стріляти   [Q] вийти{RST}"); print()
    print(f"  {W}Press SPACE to start...{RST}"); print()
    wait_key(' ', '\r')

# -----------------------------------------------------------------------------
# AI COMMENT:
# Final resolution of the system narrative.
#
# If the player clears all waves,
# the recommended remediation action is:
#
#   go outside
#   touch grass
# -----------------------------------------------------------------------------
def arcade_gameover(g):
    clr(); print()
    if g.won:
        print(f"  {G}{BOLD}╔══════════════════════════════════════════════════╗{RST}")
        print(f"  {G}║{RST}  {W}CRITICAL WARNING: SKILL OVERFLOW DETECTED       {RST}{G}║{RST}")
        print(f"  {G}╚══════════════════════════════════════════════════╝{RST}"); print()
        slow(f"  {Y}Зачекай.{RST}", d=0.04); print()
        slow(f"  Ти реально {W}вибив всі 4 хвилі{RST}?", d=0.025)
        slow(f"  Всі {R}TypeScript помилки{RST} знищено?", d=0.025); print()
        slow(f"  {DIM}Перевірка даних...{RST}", d=0.018); pause(1.5)
        slow(f"  {DIM}Аналіз поведінки гравця...{RST}", d=0.018); pause(1.2)
        slow(f"  {R}ДІАГНОЗ: Критичний дефіцит свіжого повітря.{RST}", d=0.025); print()
        print(f"  ┌─────────────────────────────────────────────────┐")
        print(f"  │  {W}СИСТЕМНЕ ПОПЕРЕДЖЕННЯ:{RST}                          │")
        print(f"  │                                                  │")
        print(f"  │  Людина яка пройшла всі хвилі Space Invaders    │")
        print(f"  │  у день народження — це {R}not okay{RST}.               │")
        print(f"  │                                                  │")
        print(f"  │  {G}Рекомендована дія:{RST}                              │")
        print(f"  │  1. Закрий термінал                              │")
        print(f"  │  2. Встань зі стільця                            │")
        print(f"  │  3. Вийди на вулицю                              │")
        print(f"  │  4. Поторкай траву руками                        │")
        print(f"  │  5. Подихай повітрям ~15 хвилин                 │")
        print(f"  │  6. Згадай що ти {W}не японець{RST}                     │")
        print(f"  │                                                  │")
        print(f"  │  {DIM}Це не прохання. Це інцидент P0.{RST}               │")
        print(f"  └─────────────────────────────────────────────────┘"); print()
        print(f"  Рахунок: {W}{g.score} балів{RST}  {DIM}(занадто багато для нормальної людини){RST}"); print()
        print(f"  {C}── З Днем Народження, Женю! 🎂 ──{RST}"); print()
        line('─', DIM); print()
        slow(f"  {Y}Нова таска призначена автоматично:{RST}", d=0.02); print()
        print(f"  {DIM}┌────────────────────────────────────────────┐{RST}")
        print(f"  {DIM}│{RST}  ID: TASK-0022                               {DIM}│{RST}")
        print(f"  {DIM}│{RST}  Title: {W}Touch grass{RST}                          {DIM}│{RST}")
        print(f"  {DIM}│{RST}  Priority: {R}P0{RST}                               {DIM}│{RST}")
        print(f"  {DIM}│{RST}  Assignee: {Y}zhenya.exe{RST}                        {DIM}│{RST}")
        print(f"  {DIM}│{RST}  Due: {R}TODAY{RST}                                  {DIM}│{RST}")
        print(f"  {DIM}│{RST}  Description: вийди на вулицю. подихай.      {DIM}│{RST}")
        print(f"  {DIM}│{RST}  Нагадування: ти {W}не японець{RST}.                 {DIM}│{RST}")
        print(f"  {DIM}└────────────────────────────────────────────┘{RST}")

    elif g.lost and g.goal_hit:
        print(f"  {Y}{BOLD}╔═══════════════════════════════════════════╗{RST}")
        print(f"  {Y}║{RST}  {W}PROCESS TERMINATED — BUT GOAL ACHIEVED  {RST} {Y}║{RST}")
        print(f"  {Y}╚═══════════════════════════════════════════╝{RST}"); print()
        slow(f"  {R}zhenya.exe{RST} було зупинено ворожими TS помилками.", d=0.025); print()
        slow(f"  Але {G}фінальний рахунок: {W}{g.score} балів{RST} — {G}ЦІЛЬ ДОСЯГНУТА ✓{RST}", d=0.025); print()
        slow(f"  {Y}\"Не все в житті треба виконати на 101%.{RST}", d=0.022)
        slow(f"  {Y}Іноді достатньо просто досягти мети —{RST}", d=0.022)
        slow(f"  {Y}навіть якщо це коштувало всіх life points.\"{RST}", d=0.022); print()
        slow(f"  {DIM}Root cause: TypeScript strict mode.{RST}", d=0.018)
        slow(f"  {DIM}Resolution: зафіксовано достатньо. Deploy approved.{RST}", d=0.018)

    else:
        print(f"  {R}{BOLD}╔════════════════════════════════════════╗{RST}")
        print(f"  {R}║{RST}  {W}FATAL: zhenya.exe has been terminated  {RST}{R}║{RST}")
        print(f"  {R}╚════════════════════════════════════════╝{RST}"); print()
        slow(f"  {R}Error:{RST} Scored only {W}{g.score}/{SCORE_TARGET}{RST} before process exit.", d=0.025); print()
        slow(f"  {Y}TS2345:{RST} Argument of type 'skill' is not assignable", d=0.022)
        slow(f"          to parameter of type 'enough_skill'.", d=0.022); print()
        slow(f"  {DIM}Спробуй ще раз. TS помилки самі себе не виправлять.{RST}", d=0.018)

    print(); print(f"  {DIM}[R] Restart   [Q] Continue to results{RST}"); print()
    while True:
        for k in get_keys():
            if k in ('r','R'): return 'restart'
            if k in ('q','Q','\r',' '): return 'continue'
        time.sleep(0.05)

def run_arcade(cheat=False):
    hide_cur()
    won_all = False
    try:
        arcade_intro(cheat)
        while True:
            g = Game(cheat=cheat)
            clr()
            last = time.time()
            while g.running:
                now = time.time()
                if now-last < TICK: time.sleep(TICK-(now-last))
                last = time.time()
                g.update(get_keys())
                render_game(g)
            if g.won: won_all = True
            result = arcade_gameover(g)
            if result == 'restart': continue
            break
    finally:
        show_cur()
    return won_all


def phase_glitch_post():
    clr(); print()
    line('═', R); print()
    slow(f"  {R}⚠  RETURNING TO INCIDENT DIAGNOSTICS...{RST}", d=0.04); pause(0.6)
    glitch_chars = list("▓░▒█▄▀■□▪▫")
    for msg in ["zhenya.exe is not a bug.", "zhenya.exe is a feature."]:
        for _ in range(3):
            corrupted = ''.join(
                random.choice(glitch_chars) if ch!=' ' and random.random()<0.3 else ch
                for ch in msg)
            sys.stdout.write(f'\r  {R}{corrupted}{RST}'); sys.stdout.flush(); time.sleep(0.08)
        sys.stdout.write(f'\r  {W}{msg}{RST}\n'); sys.stdout.flush(); pause(0.1)
    print(); pause(0.5)

def phase_reveal():
    clr(); print()
    line('═', Y); print()
    for col, al in zip([R,R,Y,Y,G,G],[
        "  ██████╗   ██████╗",
        "  ╚════██╗  ╚════██╗",
        "   █████╔╝   █████╔╝",
        "  ██╔═══╝   ██╔═══╝",
        "  ███████╗  ███████╗",
        "  ╚══════╝  ╚══════╝",
    ]):
        print(center(col+al+RST)); pause(0.07)
    print()
    slow(center(f"{W}{BOLD}З ДНЕМ НАРОДЖЕННЯ, ЖЕНЮ! 🎂{RST}"), d=0.04); print(); pause(0.3)
    line('─', DIM); print()
    for l in [
        f"{DIM}Серйозно кажучи —{RST}",
        "",
        f"  Ти реально {G}дуже крута людина{RST}.",
        f"  З тих, поруч з якими {Y}відчувається підтримка{RST} —",
        f"  не на словах, а по-справжньому.",
        "",
        f"  У тебе є оце рідкісне — {C}залученість{RST}.",
        f"  Ти не просто поставиш реакт чи скажеш щось — ти {G}вкладаєшся{RST},",
        f"  і це помітно, і це багато значить для мене.",
        "",
        f"  Рухайся до свого, як ти вмієш.",
        f"  А якщо цілі зміняться — {Y}не парся{RST}.",
        f"  Це не шось погане, це просто {C}шорткат квеста під назвою «життя»{RST}.",
        "",
        f"  Ти {G}крутелик{RST}, і я впевнений —",
        f"  у тебе {W}все буде{RST}.",
        "",
        f"  {DIM}Просто не забувай, який ти є.{RST}",
        "",
    ]:
        pause(0.12); slow(l, d=0.02)
    line('─', DIM); print(); pause(0.5)

def phase_finale(all_waves_cleared=False):
    for l,d in [
        (f"  {DIM}Incident INC-2026-0320 resolution:{RST}", 0.02),
        (f"  {G}{BOLD}→ RESOLVED: zhenya.exe declared critical infrastructure.{RST}", 0.025),
        (f"  {G}→ Auto-restart enabled. Uptime target: ∞{RST}", 0.025),
        (f"  {G}→ Scheduled for next review: never.{RST}", 0.025),
    ]:
        slow(l, d=d); pause(0.1)
    print()
    if all_waves_cleared:
        line('─', DIM)
        slow(f"  {Y}Нова задача призначена → {W}zhenya.exe{RST}", d=0.025); pause(0.2)
        for l,d in [
            (f"  {DIM}Priority:{RST}  {R}P0 CRITICAL{RST}", 0.02),
            (f"  {DIM}Assignee:{RST} {W}@zhenya{RST}", 0.02),
            (f"  {DIM}Due:{RST}      {Y}сьогодні{RST}", 0.02),
            (f"  {DIM}Task:{RST}     {G}Вийти на вулицю. Поторкати траву. Подихати повітрям.{RST}", 0.025),
            (f"  {DIM}Notes:{RST}    {DIM}Ти не японець. Deploy може почекати. Ти не можеш.{RST}", 0.018),
        ]:
            pause(0.15); slow(l, d=d)
        line('─', DIM); print()
    line_out = '  '
    for _ in range(min(tw()//4, 18)):
        line_out += random.choice(['🎉','🎂','🎊','✨','🚀','🔥','💯'])+'  '
    slow(line_out, d=0.05)
    print(); line('═', Y); print(); pause(0.5)
    slow(f"  {DIM}Відкриваємо фінальну сторінку...{RST}", d=0.018); pause(1.0)
    _open_bsod()

BSOD_URL = "https://bewayos.github.io/test_HB/bsod.html"

def _open_bsod():
    import pathlib, webbrowser, urllib.request, tempfile, os

    here = pathlib.Path(__file__).parent
    local = here / "bsod.html"
    if local.exists():
        webbrowser.open(local.as_uri())
        return

    try:
        slow(f"  {DIM}Fetching final page...{RST}", d=0.018)
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        urllib.request.urlretrieve(BSOD_URL, tmp.name)
        webbrowser.open(pathlib.Path(tmp.name).as_uri())
    except Exception as e:
        print(f"  {DIM}Could not fetch bsod.html: {e}{RST}")
        print(f"  {Y}Open manually: {BSOD_URL}{RST}")

def main():
    start_input()
    hide_cur()
    try:
        boot_screen()
        phase_scan()
        phase_loading()
        phase_report()
        phase_events()

        cheat = phase_glitch_with_cheat_detection()
        if cheat:
            cheat = debug_room()

        clr(); print()
        slow(f"  {Y}Нова система: CONFLICT RESOLVE MANAGER v2.0 (beta){RST}", d=0.025)
        slow(f"  {DIM}Знищіть достатню кількість конфліктів у кодовій базі щоб розблокувати результат.{RST}", d=0.018)
        print(); pause(0.8)

        run_arcade(cheat=cheat)

        won_all = run_arcade(cheat=cheat)

        phase_glitch_post()
        phase_reveal()
        phase_finale(all_waves_cleared=won_all)

    except KeyboardInterrupt:
        print(f"\n\n  {R}Interrupted. But you can't escape the birthday. 🎂{RST}\n")
    finally:
        show_cur()

if __name__ == '__main__':
    main()

# -----------------------------------------------------------------------------
# FINAL AI NOTE
#
# After reviewing the entire codebase I can confirm:
#
# This is not a bug.
# This is a feature.
#
# Happy Birthday, Zhenya.
#
# I hope the process zhenya.exe continues running
# for many more years without critical failures.
#
# End of analysis.
# Reality status: uncertain.
# -----------------------------------------------------------------------------
