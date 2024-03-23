declare sub matrix()
declare sub xparadox()
declare sub net()
declare sub video()
declare sub hoop()
declare sub bounce()
declare sub oldtv()
declare sub score()
declare sub basketball()

DIM SHARED x
DIM SHARED y
DIM SHARED touch
DIM SHARED points
DIM SHARED previous
DIM SHARED direction
DIM SHARED count

CLS
LOCATE 10, 32: PRINT "LOADING PROGRAM"
FOR i = 10 TO 60
    COLOR 7
    LOCATE 16, 1 + i: PRINT CHR$(219)
    COLOR 7
    LOCATE 17, 40: PRINT x * 2; "%"
    x = x + 1
    FOR j = 1 TO 500000: NEXT j
NEXT i
CLS
CALL matrix
SCREEN 12
CLS
CALL xparadox
CLS
CALL video
CLS
points = 0
touch = o
x = 60
y = 440
CALL basketball
CALL net
CALL score

DO
    A$ = INPUT$(1)
    IF A$ = "a" OR A$ = "s" OR A$ = "z" OR A$ = "x" THEN
        IF A$ = "z" THEN
            FOR m = 1 TO 20
                CIRCLE (x, y), (m), 0, bf
            NEXT m
            x = x - 10
            y = y + 10
            direction = 3
            IF x <= 10 THEN
                x = x + 10
                y = y - 10
            END IF
            IF y >= 450 THEN
                y = y - 10
                x = x + 10
            END IF
            CALL hoop
            CALL bounce
            CALL basketball
            CALL net
            CALL score
        ELSEIF A$ = "x" THEN
            FOR m = 1 TO 20
                CIRCLE (x, y), (m), 0, bf
            NEXT m
            y = y + 10
            x = x + 10
            direction = 4
            IF y >= 450 THEN
                y = y - 10
                x = x - 10
            END IF
            CALL hoop
            CALL bounce
            CALL basketball
            CALL net
            CALL score
        ELSEIF A$ = "a" THEN
            FOR m = 1 TO 20
                CIRCLE (x, y), (m), 0, bf
            NEXT m
            direction = 4
            x = x - 10
            y = y - 10
            IF x <= 10 THEN
                x = x + 10
                y = y + 10
            END IF
            IF y <= 10 THEN
                y = y + 10
                x = x + 10
            END IF
            CALL hoop
            CALL bounce
            CALL basketball
            CALL net
            CALL score
        ELSEIF A$ = "s" THEN
            FOR m = 1 TO 20
                CIRCLE (x, y), (m), 0, bf
            NEXT m
            x = x + 10
            y = y - 10
            direction = 2
            IF y <= 10 THEN
                y = y + 10
                x = x - 10
            END IF
            CALL hoop
            CALL bounce
            CALL basketball
            CALL net
            CALL score
        END IF
        previous = points
        IF x >= 480 AND x <= 520 THEN
            IF y >= 138 AND y <= 161 THEN touch = touch + 1
            IF touch = 1 AND x >= 480 AND x <= 520 AND y <= 145 AND y <= 168 THEN
                points = points + 1
                IF points = previous + 1 THEN touch = 0
            ELSE
                touch = 0
            END IF
        ELSE
            touch = 0
        END IF
    ELSE
        EXIT DO
    END IF
LOOP
CALL oldtv
END

SUB matrix
FOR t = 1 TO 90000
    1 DEF SEG = &HB800
    2 FOR i% = 0 TO 159 STEP 4
        3 IF RND < .0005 THEN j% = 3840 ELSE j% = -1
        4 IF j% > 0 THEN POKE j% + i%, PEEK(j% - 160 + i%)
        5 IF j% > 0 THEN j% = j% - 160
        6 IF j% > 0 THEN GOTO 4
        7 IF j% = 0 THEN IF RND > .3 THEN POKE i%, 96 * RND + 32 ELSE POKE i%, 32
    8 NEXT
NEXT t
END SUB

SUB xparadox
CLS
PRINT
PRINT
PRINT
PRINT
PRINT
PRINT
PRINT
PRINT
PRINT "      ²²   ²²_²²²²²²      ²     ²²²²²²        ²     ²²²²²²²   ²²²²²  ²²   ²² "
PRINT "       ²² ²²__²²   ²²    ²²²    ²²   ²²      ²²²    ²²    ²² ²²   ²²  ²² ²²  "
PRINT "        ²²²___²²²²²²    ²² ²²   ²²²²²²      ²² ²²   ²²    ²² ²²   ²²   ²²²   "
PRINT "       ²² ²²__²²       ²²²²²²²  ²²   ²²    ²²²²²²²  ²²    ²² ²²   ²²  ²² ²²  "
PRINT "      ²²   ²²_²²      ²²     ²² ²²    ²²  ²²     ²² ²²²²²²²   ²²²²²  ²²   ²² "
PRINT
PRINT
PRINT "        ²²²²²  ²²²²²    ²²²   ²²²²²  ²  ² ²²²² ²²²²²² ²²²²²  ²²²   ²²²   ²² "
PRINT "        ²²  ²² ²²  ²²  ²²  ²²  ²  ²  ²  ² ²  ² ²²²²²²   ²   ²²  ²² ²²²²  ²² "
PRINT "        ²²²²²  ²²²²²   ²²  ²²  ²  ²  ²  ² ²      ²²     ²   ²²  ²² ²² ²² ²² "
PRINT "        ²²     ²²  ²²  ²²  ²²  ²  ²  ²  ² ²  ²   ²²     ²   ²²  ²² ²²  ²²²² "
PRINT "        ²²     ²²   ²²  ²²²²  ²²²²²  ²²²² ²²²²   ²²   ²²²²²  ²²²²  ²²   ²²² "
PRINT
SLEEP 1
END SUB

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

SUB video
x = 20
y = 400
number1 = 0
number2 = 0
WHILE a < 6
    IF x > 520 THEN number2 = 1
    IF number2 = 0 THEN
        r = x - 10
    ELSEIF number2 = 1 THEN
        r = x + 10
    END IF
    IF y < 10 THEN number1 = 1
    IF number1 = 0 THEN
        d = y + 10
    ELSEIF number1 = 1 THEN
        d = y - 10
    END IF
    s$ = RIGHT$(TIME$, 2)
    FOR i = 1 TO 700000
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
    IF number2 = 0 THEN
        x = x + 10
    ELSEIF number2 = 1 THEN
        x = x - 10
    END IF
    IF number1 = 1 THEN
        y = y + 10
    ELSEIF number1 = 0 THEN
        y = y - 10
    END IF
    CALL net
    CALL score
WEND
count = 1
END SUB

SUB hoop
IF x >= 440 AND x <= 465 AND y >= 115 AND y <= 161 THEN
    FOR j = 1 TO 4
        FOR m = 1 TO 20
            CIRCLE (x, y), (m), 0, bf
        NEXT m
        IF direction = 4 THEN
            x = x - 10
            y = y + 10
        ELSEIF direction = 2 THEN
            x = x - 10
            y = y - 10
        ELSEIF direction = 1 THEN
            x = x + 10
            y = y - 10
        ELSEIF direction = 3 THEN
            x = x + 10
            y = y + 10
        END IF
        FOR o = 1 TO 1000
        NEXT o
        CALL basketball
        CALL net
    NEXT j
ELSEIF x >= 464 AND x <= 480 AND y >= 115 AND y <= 161 THEN
    FOR j = 1 TO 4
        previous = points
        IF x >= 480 AND x <= 520 THEN
            IF y >= 138 AND y <= 161 THEN touch = touch + 1
            IF touch = 1 AND x >= 480 AND x <= 520 AND y <= 145 AND y <= 168 THEN
                points = points + 1
                IF points = previous + 1 THEN touch = 0
            ELSE
                touch = 0
            END IF
        ELSE
            touch = 0
        END IF
        FOR m = 1 TO 20
            CIRCLE (x, y), (m), 0, bf
        NEXT m
        IF direction = 1 THEN
            x = x + 10
            y = y - 10
        ELSEIF direction = 2 THEN
            x = x + 10
            y = y + 10
        ELSEIF direction = 3 THEN
            x = x + 10
            y = y + 10
        ELSEIF direction = 4 THEN
            x = x + 10
            y = y - 10
        END IF
        FOR o = 1 TO 1000
        NEXT o
        CALL basketball
        CALL net
    NEXT j
END IF
END SUB

SUB bounce
IF x = 530 THEN
    FOR j = 1 TO 3
        previous = points
        IF x >= 480 AND x <= 520 THEN
            IF y >= 138 AND y <= 161 THEN touch = touch + 1
            IF touch = 1 AND x >= 480 AND x <= 520 AND y <= 145 AND y <= 168 THEN
                points = points + 1
                IF points = previous + 1 THEN touch = 0
            ELSE
                touch = 0
            END IF
        ELSE
            touch = 0
        END IF
        FOR m = 1 TO 20
            CIRCLE (x, y), (m), 0, bf
        NEXT m
        x = x - 10
        IF direction = 4 THEN
            y = y + 10
        ELSEIF direction = 2 THEN
            y = y - 10
        END IF
        IF x < 10 THEN
            x = x + 10
            IF direction = 4 THEN
                y = y - 10
            ELSEIF direction = 2 THEN
                y = y + 10
            END IF
        END IF
        IF y >= 450 THEN
            y = y - 10
            x = x + 10
        END IF
        FOR o = 1 TO 1000
        NEXT o
        CALL basketball
        CALL net
    NEXT j
END IF
END SUB

SUB score
LINE (540, 2)-(636, 77), 0, BF
LINE (542, 4)-(638, 75), 6, B
LINE (544, 6)-(636, 73), 4, B
LINE (546, 8)-(634, 71), 1, B
IF count = 1 THEN
    LOCATE 3, 70: PRINT "Score="; points * 5
ELSEIF count = o THEN
    LOCATE 3, 70: PRINT "Score"
END IF
IF points > 20 THEN
    CALL oldtv
    END
END IF
END SUB

SUB basketball
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
END SUB

SUB oldtv
WHILE a <= 65
    SCREEN 13
    t% = RND * 345
    WAIT &H3DA, 8
    FOR i% = 0 TO 199
        FOR j% = 0 TO 319
            k% = ((k% + t% XOR j% XOR i%)) AND &HFF
            PSET (j%, i%), k%
    NEXT j%, i%
    a = a + 1
WEND
END SUB


