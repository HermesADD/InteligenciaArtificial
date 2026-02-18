%=====================
% Definimos los hechos
%=====================

hombre(yo).
hombre(papa).
hombre(hijo1).
hombre(hijo2).

mujer(esposa).
mujer(hija_esposa).


era_viuda(esposa).
era_viudo(papa).

pareja(yo, esposa).
pareja(papa, hija_esposa).

madre_bio(esposa, hija_esposa).
madre_bio(hija_esposa, hijo1).
madre_bio(esposa, hijo2).

padre_bio(papa, yo).
padre_bio(papa, hijo1).
padre_bio(yo, hijo2).

%==========================
% Reglas
%==========================

conyuge(X,Y) :- pareja(X,Y).
conyuge(X,Y) :- pareja(Y,X).

madre(M, H) :- madre_bio(M, H).
madre(M, H) :-
    mujer(M),
    conyuge(M, P),
    padre_bio(P, H),
    M \= P.

padre(P, H) :- padre_bio(P, H).
padre(P, H) :-
    hombre(P),
    conyuge(P, M),
    madre_bio(M, H),
    P \= M.

padres(X, Y) :- padre(X, Y).
padres(X, Y) :- madre(X, Y).

hermano(X, Y) :-
    hombre(X),
    X \= Y,
    padres(P, X),
    padres(P, Y).

hermana(X, Y) :-
    mujer(X),
    X \= Y,
    padres(P, X),
    padres(P, Y).

tio(T, S) :-
    hombre(T),
    padres(P, S),
    (
        hermano(T, P);
        conyuge(T, TA), tia(TA, S)
    ).

tia(T, S) :-
    mujer(T),
    padres(P, S),
    ( hermana(T, P)
    ; conyuge(T, TO), tio(TO, S)
    ).

abuelo(A, N) :-
    hombre(A),
    padres(A, P),
    padres(P, N).

abuela(A, N) :-
    mujer(A),
    padres(A, P),
    padres(P, N).

suegro(S, Y) :- 
    hombre(S),
    conyuge(Y, Z),
    padre(S, Z).

suegra(S, Y) :-
    mujer(S),
    conyuge(Y, Z),
    madre(S, Z).

yerno(Y, S) :- 
    hombre(Y),
    conyuge(Y, Z),
    padres(S, Z).

nuera(N, S) :-
    mujer(N),
    conyuge(N, Z),
    padres(S, Z).

cunado(X, Y) :- 
    hombre(X),
    conyuge(Y, Z),
    (hermano(X, Z) ; hermana(X, Z)).

cunada(X, Y) :-
    mujer(X),
    conyuge(Y, Z),
    (hermano(X, Z) ; hermana(X, Z)).

hijo_directo(X, Y) :- padres(Y, X).

hijo_politico(X, Y) :-
    conyuge(X, Z),
    hijo_directo(Z, Y).

hijo(X, Y) :-
    hombre(X),
    (hijo_directo(X, Y); hijo_politico(X, Y)).

hija(X, Y) :-
    mujer(X),
    (hijo_directo(X,Y); hijo_politico(X,Y)).
