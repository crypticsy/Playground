declare sub net()

SCREEN 12
CLS
x = 20
y = 440
WHILE a <= 4
    r = x - 10
    d = y + 10
    s$ = RIGHT$(TIME$, 2)
    FOR i = 1 TO 1000000
    NEXT i
    c$ = RIGHT$(TIME$, 2)
    IF c$ <> s$ THEN a = a + 1
    FOR m = 1 TO 20
        CIRCLE (r, d), (m), 0, bf
    NEXT m

    FOR l = 1 TO 20
        CIRCLE (x, y), (l), 6, bf
    NEXT l
    strip1 = x - 24
    CIRCLE (strip1, y), 20, 0, bf
    strip2 = x + 24
    CIRCLE (strip2, y), 20, 0, bf
    q = x - 20
    w = x + 20
    LINE (q, y)-(w, y), 0, BF
    x = x + 10
    y = y - 10

    CALL net
WEND

SUB net
SCREEN 12
LINE (540, 46)-(560, 46), 7, BF
LINE (460, 138)-(460, 147), 8, BF
LINE (460, 147)-(480, 204)
LINE (480, 204)-(500, 147)
LINE (500, 147)-(520, 204)
LINE (520, 204)-(540, 147)
LINE (480, 147)-(470, 176)
LINE (480, 147)-(500, 204)
LINE (500, 204)-(520, 147)
LINE (520, 147)-(530, 176)
LINE (480, 204)-(520, 204)
LINE (470, 177)-(530, 177)
FOR i = 540 TO 560
    LINE (i, 46)-(i, 460), 7, BF
NEXT i

FOR k = 138 TO 148
    LINE (460, k)-(539, k), 8, BF
NEXT k

FOR a = 460 TO 480
    LINE (0, a)-(640, a), 8, BF
NEXT a
END SUB

