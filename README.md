# Calculadora Complexa com Kivy

Este é um projeto em Python que utiliza o framework [Kivy](https://kivy.org/) para criar uma aplicação que trabalha com números complexos. A aplicação permite realizar operações aritméticas (soma, subtração, multiplicação e divisão) com números complexos e calcular o determinante de uma matriz 2x2 com coeficientes complexos, exibindo os resultados tanto na forma retangular quanto na forma polar.

## Funcionalidades

- **Operações com Números Complexos**  
  Permite a entrada de números complexos (em notação retangular ou polar) intercalados com operadores (+, -, *, /), realizando os cálculos respeitando a precedência das operações.

- **Cálculo do Determinante**  
  Resolve sistemas lineares 2x2 com coeficientes complexos, utilizando o cálculo do determinante. Caso a matriz não seja inversível, o usuário é informado sobre o erro.

- **Conversões entre Coordenadas Retangular e Polar**  
  O projeto inclui funções para converter números complexos entre as representações retangular e polar, facilitando a visualização dos resultados.

## Pré-requisitos

- Python 3.6 ou superior
- [Kivy](https://kivy.org/doc/stable/gettingstarted/installation.html)
- [NumPy](https://numpy.org/)
