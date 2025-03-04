import cmath
import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from math import sqrt, atan, degrees
from numpy import array, imag, linalg, real

# Carrega os arquivos de layout Kivy
Builder.load_file('determinante.kv')
Builder.load_file('main.kv')
Builder.load_file('operacao.kv')

j = complex(0, 1)  # Número complexo j (unidade imaginária)

def polar(x):
    """
    Converte um número complexo da forma retangular para polar.
    Retorna amplitude e ângulo em graus.
    """
    parte_real = real(x)
    parte_imaginaria = imag(x)
    amplitude = sqrt(parte_real ** 2 + parte_imaginaria ** 2)
    angulo = degrees(atan(parte_imaginaria / parte_real))
    return amplitude, angulo

def numero_real(string):
    """
    Verifica se a string pode ser convertida para float (número real).
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def num_complexo(string):
    """
    Converte uma string em número complexo, tratando casos especiais como "j" e "-j".
    """
    if string == "-j":
        return complex(0, -1)
    if string == "j":
        return complex(0, 1)
    if "+" in string:
        partes = string.split("+")
        real_val = float(partes[0])
        imag_val = float(partes[1].replace("j", ""))
    elif "-" in string:
        partes = string.split("-")
        if partes[0] == "":
            real_val = 0.0
            imag_val = float("-" + partes[1].replace("j", ""))
        else:
            real_val = float(partes[0])
            imag_val = float("-" + partes[1].replace("j", ""))
    else:
        if string.endswith("j"):
            real_val = 0.0
            imag_val = float(string.replace("j", ""))
        else:
            real_val = float(string.replace("j", ""))
            imag_val = 0.0
    return complex(real_val, imag_val)

class DeterminanteComplexoLayout(Screen):
    """
    Interface para o cálculo do determinante de uma matriz complexa.
    """
    def calcular_determinante(self):
        # Captura as entradas de texto para os coeficientes
        a_entrada = self.ids.a_input.text
        b_entrada = self.ids.b_input.text
        c_entrada = self.ids.c_input.text
        d_entrada = self.ids.d_input.text
        e_entrada = self.ids.e_input.text
        f_entrada = self.ids.f_input.text

        # Converte as entradas para número real ou complexo conforme necessário
        a = float(a_entrada) if numero_real(a_entrada) else num_complexo(a_entrada)
        b = float(b_entrada) if numero_real(b_entrada) else num_complexo(b_entrada)
        c = float(c_entrada) if numero_real(c_entrada) else num_complexo(c_entrada)
        d = float(d_entrada) if numero_real(d_entrada) else num_complexo(d_entrada)
        e = float(e_entrada) if numero_real(e_entrada) else num_complexo(e_entrada)
        f = float(f_entrada) if numero_real(f_entrada) else num_complexo(f_entrada)

        # Define a matriz A e o vetor B
        A = array([[a, c], [b, d]])
        B = array([[e], [f]])

        try:
            # Resolve o sistema linear A * I = B
            I = linalg.solve(A, B)
            I1 = I[0][0]
            I2 = I[1][0]
            I1_real, I1_imag = real(I1), imag(I1)
            I2_real, I2_imag = real(I2), imag(I2)

            # Exibe o resultado em notações retangular e polar
            self.ids.resultado_label.text = (
                "RETANGULAR:\n"
                "1)     {:.4f}  {:.4f}j\n"
                "2)     {:.4f}  {:.4f}j\n\n"
                "POLAR:\n"
                "1)     {:.4f} | {:.4f}°\n"
                "2)     {:.4f} | {:.4f}°\n"
            ).format(I1_real, I1_imag, I2_real, I2_imag, *polar(I1), *polar(I2))

        except linalg.LinAlgError:
            # Caso a matriz não seja inversível, exibe mensagem de erro
            self.ids.resultado_label.text = "A matriz não é inversível. Não é possível calcular a solução."

    def polar_para_retangular(self, amplitude, angulo):
        """
        Converte coordenadas polares para retangulares.
        """
        real_val = amplitude * math.cos(math.radians(angulo))
        imag_val = amplitude * math.sin(math.radians(angulo))
        return complex(real_val, imag_val)

    def retangular_para_polar(self, x):
        """
        Converte um número complexo de retangular para polar.
        """
        amplitude = abs(x)
        angulo = cmath.phase(x)
        return amplitude, math.degrees(angulo)

    def definir_entrada(self, entrada):
        """
        Processa a string de entrada, identificando números (retangular ou polar)
        e separando as operações.
        """
        partes = entrada.split()  # Divide a entrada em partes
        self.operacao = []
        self.numeros = [] 
        i = 0
        while i < len(partes):
            parte_string = partes[i]
            if "|" in parte_string:
                # Converte entrada polar para número complexo
                r, ang = parte_string.split("|")
                num = self.polar_para_retangular(float(r), float(ang))
                self.numeros.append(num)
            elif parte_string in ["j", "-j"]:
                # Trata casos onde a entrada é apenas "j" ou "-j"
                num = complex(0, 1) if parte_string == "j" else complex(0, -1)
                self.numeros.append(num)
            else:
                num = complex(parte_string)
                self.numeros.append(num)
            # Se houver uma operação após o número, ela é armazenada
            if i+1 < len(partes):
                self.operacao.append(partes[i+1])
            i += 2

    def realizar_operacao(self):
        """
        Realiza as operações de multiplicação/divisão primeiro e depois
        soma/subtração, respeitando a precedência.
        """
        if "*" in self.operacao or "/" in self.operacao:
            i = 0
            while i < len(self.numeros) - 1:
                if self.operacao[i] == "*":
                    resultado = self.numeros[i] * self.numeros[i + 1]
                    del self.operacao[i]
                    del self.numeros[i + 1]
                    self.numeros[i] = resultado
                elif self.operacao[i] == "/":
                    resultado = self.numeros[i] / self.numeros[i + 1]
                    del self.operacao[i]
                    del self.numeros[i + 1]
                    self.numeros[i] = resultado
                else:
                    i += 1
        resultado = self.numeros[0]
        for i in range(1, len(self.numeros)):
            if self.operacao[i-1] == "+":
                resultado += self.numeros[i]
            elif self.operacao[i-1] == "-":
                resultado -= self.numeros[i]
        return resultado

    def calcular(self):
        """
        Lê a entrada do usuário, processa as operações e exibe o resultado
        nas formas retangular e polar.
        """
        entrada = self.ids.entrada_input.text
        self.definir_entrada(entrada)
        resultado = self.realizar_operacao()
        amplitude, angulo = self.retangular_para_polar(resultado)

        self.ids.resultado_retangular_label.text = f"(Retangular): {resultado.real:.5f} {resultado.imag:+.5f}j"
        self.ids.resultado_polar_label.text = f"(Polar): {amplitude:.5f} | {angulo:.5f}°"

class OperacaoScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class DeterminanteScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass

class ComplexCalculatorLayout(BoxLayout):
    entrada_input = ObjectProperty()
    resultado_retangular_label = ObjectProperty()
    resultado_polar_label = ObjectProperty()
    
    def polar_para_retangular(self, amplitude, angulo):
        real_val = amplitude * math.cos(math.radians(angulo))
        imag_val = amplitude * math.sin(math.radians(angulo))
        return complex(real_val, imag_val)
    
    def retangular_para_polar(self, x):
        amplitude = abs(x)
        angulo = cmath.phase(x)
        return amplitude, math.degrees(angulo)
    
    def definir_entrada(self, entrada):
        partes = entrada.split()
        self.operacao = [] 
        self.numeros = [] 
        i = 0
        while i < len(partes):
            parte_string = partes[i]
            if "|" in parte_string:
                r, ang = parte_string.split("|")
                num = self.polar_para_retangular(float(r), float(ang))
                self.numeros.append(num)
            elif parte_string in ["j", "-j"]:
                num = complex(0, 1) if parte_string == "j" else complex(0, -1)
                self.numeros.append(num)
            else:
                num = complex(parte_string)
                self.numeros.append(num)
            if i+1 < len(partes):
                self.operacao.append(partes[i+1])
            i += 2
    
    def realizar_operacao(self):
        if "*" in self.operacao or "/" in self.operacao:
            i = 0
            while i < len(self.numeros) - 1:
                if self.operacao[i] == "*":
                    resultado = self.numeros[i] * self.numeros[i + 1]
                    del self.operacao[i]
                    del self.numeros[i + 1]
                    self.numeros[i] = resultado
                elif self.operacao[i] == "/":
                    resultado = self.numeros[i] / self.numeros[i + 1]
                    del self.operacao[i]
                    del self.numeros[i + 1]
                    self.numeros[i] = resultado
                else:
                    i += 1
        resultado = self.numeros[0]
        for i in range(1, len(self.numeros)):
            if self.operacao[i-1] == "+":
                resultado += self.numeros[i]
            elif self.operacao[i-1] == "-":
                resultado -= self.numeros[i]
        return resultado

    def calcular(self):
        entrada = self.ids.entrada_input.text
        self.definir_entrada(entrada)
        resultado = self.realizar_operacao()
        amplitude, angulo = self.retangular_para_polar(resultado)

        self.ids.resultado_retangular_label.text = f"(Retangular): {resultado.real:.5f} {resultado.imag:+.5f}j"
        self.ids.resultado_polar_label.text = f"(Polar): {amplitude:.5f} | {angulo:.5f}°"

class MyApp(App):
    def build(self):
        sm = ScreenManager()  # Gerencia as telas da aplicação
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DeterminanteScreen(name='determinante'))
        sm.add_widget(OperacaoScreen(name='operacao'))
        return sm
    
MyApp().run()
