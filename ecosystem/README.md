# Ecossistema

Uma atividade de estrutura de dados

## Problema

Escreva um programa em Python simulando um ecossistema que consiste em um rio, modelado como uma lista,
que contem dois tipos de animais: ursos e peixes.

No ecossistema, cada elemento da lista deve ser um objeto do
tipo `Urso`, `Peixe` ou `None`.

A cada rodada do jogo, baseada em um processo aleatório, cada
animal tenta se mover para uma posição da lista adjacente (a
esquerda ou direita) ou permanece na sua mesma posição.

Se dois animais do mesmo tipo colidirem (urso com urso ou peixe com peixe),
eles permanecem em suas posições originais, mas uma nova instância do
animal deve ser posicionada em um local vazio, aleatoriamente determinado.

Se um Urso e um peixe colidirem, entretanto, o peixe morre.
