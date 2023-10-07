Tvým cílem bude napsat program, který je nejen schopen přežít, ale i zničit ostatní programy. Programy jsou však velmi omezené, takže to nebude jednoduché.

Z důvodu, aby byla úloha zajímavější, nejsou následující instrukce kompletní. Vše co v nich je
je pravda, ale některé drobnosti jsou možná zatajeny. Nijak výrazně neovlivňují výsledek, ale
můžou se hodit.

Narozdíl od běžného programování tu je pár drobných rozdílů.

- Paměť pro data a kód je společná. To znamená, že můžeš přepsat svůj vlastní kód.
  Stačí zapsat do paměti na správné místo správné byty.
- Na počítači běží několik (až 8) procesů, ty ale mají společnou paměť.
  To znamená, že můžeš přepsat kód jiného procesu pokud zjistíš, kde běží.
- Paměť je omezená. Tvůj kód se navíc musí vejít do 256 bytů.
- Kromě paměti (která je sdílená pro všechny programy) má každý program své vlastní registry.
  Registr je taková proměnná, která je ale čistě pro tvůj program a nikdo ji nemůže číst
  ani do ní zapisovat. Ve všech registrech je na začátku nula. V prvním registru je vždy nula a není povolené do něj zapisovat.
  Registry nemají jména, ale čísla, indexuje se od nuly. Registrů je 6 a mají velikost 32 bitů.

Tvůj program běží, dokud nenastane některé z následujícího:
- Vykonal jsi neplatnou instrukci. Tedy něco, co není v tabulce níže. Toto se může snadno stát,
  pokud jsi neopatrně zapisoval do paměti a špatně sis papřepsal instrukce.
- Vykonal jsi instrukci "bomba" ve chvíli, kdy zbývala na odpočtu nula.
- Zacyklil jsi se. (Formálně: vykonal jsi totožnou sekvenci instrukcí na totožných adresách třikrát za sebou.)

Tvým cílem je běžet déle, než programy ostatních. (Tedy jednou z možných metod přežití může být zkusit zničit ostatní programy.)

## Registry
| Číslo | Popis                                       |
|-------|---------------------------------------------|
| 0 | Vždy obsahuje nulu. Do něj nelze zapisovat. |
| 1 | Druhý registr.                              |
| 2 | Třetí registr.                              |
| 3 | Čtvrtý registr.                             |
| 4 | Pátý registr.                               |
| 5 | Šestý registr.                              |

## Paměť

Paměť má předem neznámý rozsah.

- Vždy obsahuje 256 bytů, které "nepatří" žádnému hráči. Najdeš tam také speciální adresy:

| Adresa | Popis |
|--------|-------|
| 42 (0x2a) | Obsahuje adresu nejbližšího programu. |
| 43 (0x2b) | Obsahuje adresu druhého nejbližšího programu. |

- Poté pro každého hráče obsahuje dalších 256 bytů, kde se nachází jeho počáteční program.
- Nevíš, v jakém pořadí jsi ani kolik programů běží - tedy jestli jsou před tebou nějaké programy, nebo ne.

## Instrukce

Každá instrukce je 4 byty (32 bitů) dlouhá. První byte je kód instrukce, další tři jsou argumenty.

Všechna čísla ve slouepčku `Kód` uvedená v této tabulce jsou hexadecimální. Tedy například číslo `69` je ve skutečnosti `0x69`,
což je v desítkové soustavě 105. Dvojice čísel (v tomto případě tedy třeba `69` je jeden byte = 8 bitů.)

Ve sloupečku kód je předpis instrukce. Když je někde číslo, je pevně dané. Otazníky znamená, že hodnota daných bitů
může být libovolná a nezáleží na ní. Zápis typu `reg1(4b)` znamená, že následují 4 bity, které určují registr, který instrukce
použije. Zápis typu `imm(16b)` znamená, že následuje 16 bitů, které určují číslo (vyloženě číselný argument), které instrukce použije.

Neboj se, pokud to zatím nedává smysl, z příkladů bude vše jasné.

| Kód           | Instrukce | Popis                                                                                                                                                                                                                 | Příklad                                                                                                                                                |
|---------------| --------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `69 ?? ?? ??` | NOP | Nic neudělá.                                                                                                                                                                                                          | `69 00 00 00`                                                                                                                                          |
| `01 reg1(4b) reg2(4b) imm(16b)` | ADD | `reg1 += reg2 + imm`                                                                                                                                                                                                  | `01 12 00 00 00 04` - k hodnotě prvního registru přičte hodnotu reigstru 2 plus 4 a výsledek uloží do prvního registru.                                |
| `02 reg1(4b) reg2(4b) imm(16b)` | SUB | `reg1 -= reg2 + imm`                                                                                                                                                                                                  | `02 12 00 00 00 04` - od hodnoty prvního registru odečte (hodnotu reigstru 2 plus 4) a výsledek uloží do prvního registru.                             |
| `03 reg1(4b) reg2(4b) imm(16b)` | MUL | `reg1 *= reg2 + imm`                                                                                                                                                                                                  | `03 12 00 00 00 04` - hodnotu prvního registru vynásobí (hodnotou reigstru 2 plus 4) a výsledek uloží do prvního registru.                             |
| `05 reg1(4b) reg2(4b) imm(16b)` | LOAD | `reg1 = mem[reg2+imm]`                                                                                                                                                                                                | `05 12 00 00 00 04` - hodnotu prvního registru nastaví na hodnotu v paměti na adrese (hodnota druhého registru plus 4).                                |
| `06 reg1(4b) reg2(4b) imm(16b)` | STORE | `mem[reg2+imm] = reg1`                                                                                                                                                                                                | `06 12 00 00 00 04` - hodnotu v paměti na adrese (hodnota druhého registru plus 4) nastaví na hodnotu prvního registru.                                |
| `07 reg1(4b) reg2(4b) imm(16b)` | MOV | `reg1 = reg2 + imm`                                                                                                                                                                                                   | `07 12 00 00 00 04` - hodnotu prvního registru nastaví na hodnotu druhého registru plus 4.                                                             |
| `10 reg1(4b) reg2(4b) imm(16b)` | JUMP | `if (reg1 == reg2) pc += imm`                                                                                                                                                                                         | `10 12 00 00 00 04` - pokud je hodnota prvního registru rovna hodnotě druhého registru, skočí o čtyři instrukce dopředu.                               |
| `11 reg1(4b) reg2(4b) imm(16b)` | REVJUMP | `if (reg1 == reg2) pc -= imm`                                                                                                                                                                                         | `11 12 00 00 00 04` - pokud je hodnota prvního registru rovna hodnotě druhého registru, skočí o čtyři instrukce dozadu.                                |
| `12 reg1(4b) reg2(4b) imm(16b)` | LTJUMP | `if (reg1 < reg2) pc += imm`                                                                                                                                                                                          | `12 12 00 00 00 04` - pokud je hodnota prvního registru menší než hodnota druhého registru, skočí o čtyři instrukce dopředu.                           |
| `13 reg1(4b) reg2(4b) imm(16b)` | REVLTJUMP | `if (reg1 < reg2) pc -= imm`                                                                                                                                                                                          | `13 12 00 00 00 04` - pokud je hodnota prvního registru menší než hodnota druhého registru, skočí o čtyři instrukce dozadu.                            |
| `14 reg1(4b) reg2(4b) imm(16b)` | NEQJUMP | `if (reg1 != reg2) pc += imm`                                                                                                                                                                                         | `14 12 00 00 00 04` - pokud je hodnota prvního registru nerovna hodnotě druhého registru, skočí o čtyři instrukce dopředu.                             |
| `15 reg1(4b) reg2(4b) imm(16b)` | REVNEQJUMP | `if (reg1 != reg2) pc -= imm`                                                                                                                                                                                         | `15 12 00 00 00 04` - pokud je hodnota prvního registru nerovna hodnotě druhého registru, skočí o čtyři instrukce dozadu.                              |
| `20 reg1(4b) ?(4b) imm(16b)` | SETIMMLOW | `reg1[low] = imm`                                                                                                                                                                                                     | `20 12 00 00 00 04` - nastaví dolních 16 bitů prvního registru na hodnotu 4.                                                                           |
| `21 reg1(4b) ?(4b) imm(16b)` | SETIMMHIGH | `reg1[high] = imm`                                                                                                                                                                                                    | `21 12 00 00 00 04` - nastaví horních 16 bitů prvního registru na hodnotu 4.                                                                           |
| `42 IMM1(8b) IMM2(16b)` | TELEPORT | Zmrazí program. Pokud jiný program také spustí instrukci TELEPORT, tyto dva programy si okamžitě prohodí místa. Pokud žádný program TELEPORT nezavolá po dobu IMM1 instrukcí, program skočí o IMM2 instrukcí dopředu. | `42 10 00 00` - zmrzne program na 16 instrukcí. Pokud nikdo nezavolá teleport, skočí o 0 dopředu (tedy na tu samou instrukci a zavolá teleport znovu). |
| `50 imm(16b) ?? ??` | BOMB | Každým spuštěním se hodnota IMM sníží o 1. Pokud byla hodnota 0, nelze snížit a program umře.                                                                                                                         | `50 00 00 00` - program zanikne hned po spuštění této instrukce.                                                                                       |

Například, následující kód se zacyklí:

```
69 00 00 00  ; NOP
11 00 00 01  ; REVJUMP reg0, reg0, 0x0001
```

## Odevzdávání

Odevzdávat budeš zdrojový kód svého programu ve formátu, jako je příklad nahoře. Jak sis už mohl všimnout, `;` je komentář, vše až do konce řádku se ignoruje.
Prázdné řádky se také ignorují. Na každém jiném řádku je potřeba mít přesně 8 číslic, které dohromady dají (hexadecimálně) 32 bitů každé instrukce.

Odevzdávání této úlohy je složitější kvůli způsobu vyhodnocování. Jelikož je úloha komplexní, je zapotřebí dát účastníkovi podrobnou zpětnou vazbu.

Po odevzdání je možné se svým FIKS jménem a zvoleným heslem přihlásit na web `fiks.soptik.tech`, kde si můžeš zobrazit výsledky
svých odevzdání a zároveň stáhnout záznam toho, co se stalo. U "ostrých" sfinga odevzdání budeš mít k dispozici pouze omezený
log, který bude zobrazovat pouze tvoje akce -- je to z toho důvodu, abys nemohl tak jednoduše kopírovat kód ostatních programů.

Heslo si lze nastavit tak, že do sfingy odevzdáš soubor, který bude obsahovat pouze jediný řádek ve formátu `heslo:<moje heslo>`.

Web `fiks.soptik.tech` po přihlášení umožní i nahrát program přímo. Takovýto program bude spuštěn s jednoduchým protivníkem, který se
stále jenom cyklí. Dostaneš kompletní výpis celého stavu prostředí, abys mohl debugovat svoje programy.

Pokud chceš debugovací prostředí ve kterém dělá protivník něco jiného, přepiš jeho kód sám :)

Pokud bys měl s odevzdáním nebo webem jakékoliv problémy, ozvi se na FIKS discordu nebo na `petr.stastny@fit.cvut.cz`.

## Hodnocení

Body se udělují následovně:

- 0.01 bodu za úspěšné nastavení hesla
- celkem 1 bod za to, že odevzdáš validní program
- celkem 2 body za to, že porazíš protivníka, který se pouze cyklí.
- celkem 3-5 bodů za to, že porazíš protivníka, který na tebe bude aktivně útočit. Můžeš dostat i nižší počet bodů, pokud se mu zvládneš dost dlouho bránit, ale nepodaří se ti ho porazit.

Pokud dosáhneš alespoň 2 bodů, budeš zařazen do bitvy s ostatními účastníky.

Jednou týdně proběhne souboj mezi všemi účastníky, jejichž poslední odevzdaný program získal alespoň 2 body.
Pokud se souboje budou účastnit alespoň 4 účastníci, dostaneš až 2 extra body v závislosti na svém výkonu.
(Tyto body z různých týdnů se nesčítají.)

Po uzavření úlohy proběhne finální souboj, na základě kterého bude rozděleno až 5 bodů.

Maximum bodů, kolik můžeš získat, je 10.

Získané body za souboje uvidíš na portálu `fiks.soptik.tech`, do sfingy budou nahrané později po konci kola.