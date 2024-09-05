import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import sqlite3
import random

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

# Criando a tabela de contas
cursor.execute('''CREATE TABLE IF NOT EXISTS contas (
                    id INTEGER PRIMARY KEY,
                    numero_conta TEXT,
                    saldo REAL
                )''')
conn.commit()

class BankApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Label para exibir mensagens
        self.label = Label(text="Bem-vindo ao Banco")
        self.layout.add_widget(self.label)

        # Campo para número da conta
        self.input_conta = TextInput(hint_text='Número da Conta', multiline=False)
        self.layout.add_widget(self.input_conta)

        # Campo para valor
        self.input_valor = TextInput(hint_text='Valor', multiline=False)
        self.layout.add_widget(self.input_valor)

        # Botão para criar conta
        self.button_criar_conta = Button(text='Criar Conta')
        self.button_criar_conta.bind(on_press=self.criar_conta)
        self.layout.add_widget(self.button_criar_conta)

        # Botão para depósito
        self.button_depositar = Button(text='Depositar')
        self.button_depositar.bind(on_press=self.depositar)
        self.layout.add_widget(self.button_depositar)

        # Botão para saque
        self.button_sacar = Button(text='Sacar')
        self.button_sacar.bind(on_press=self.sacar)
        self.layout.add_widget(self.button_sacar)

        # Botão para transferência
        self.button_transferir = Button(text='Transferir')
        self.button_transferir.bind(on_press=self.transferir)
        self.layout.add_widget(self.button_transferir)

        # Botão para consulta de saldo
        self.button_saldo = Button(text='Consultar Saldo')
        self.button_saldo.bind(on_press=self.consultar_saldo)
        self.layout.add_widget(self.button_saldo)

        return self.layout

    def criar_conta(self, instance):
        numero_conta = str(random.randint(100000, 999999))
        saldo_inicial = 0.0
        cursor.execute("INSERT INTO contas (numero_conta, saldo) VALUES (?, ?)", (numero_conta, saldo_inicial))
        conn.commit()
        self.label.text = f'Conta criada com sucesso! Número da conta: {numero_conta}'

    def depositar(self, instance):
        numero_conta = self.input_conta.text
        valor = float(self.input_valor.text)
        
        if self.conta_existe(numero_conta):
            cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE numero_conta = ?", (valor, numero_conta))
            conn.commit()
            self.label.text = f'Depósito de R${valor:.2f} realizado com sucesso!'
        else:
            self.label.text = 'Conta não encontrada!'

    def sacar(self, instance):
        numero_conta = self.input_conta.text
        valor = float(self.input_valor.text)
        
        if self.conta_existe(numero_conta):
            cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
            saldo_atual = cursor.fetchone()[0]
            if saldo_atual >= valor:
                cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE numero_conta = ?", (valor, numero_conta))
                conn.commit()
                self.label.text = f'Saque de R${valor:.2f} realizado com sucesso!'
            else:
                self.label.text = 'Saldo insuficiente!'
        else:
            self.label.text = 'Conta não encontrada!'

    def transferir(self, instance):
        conta_origem = self.input_conta.text
        conta_destino = self.input_valor.text.split(':')[0]  # Número da conta destino será o texto antes do valor
        valor = float(self.input_valor.text.split(':')[1])   # Valor será o texto depois dos ':'
        
        if self.conta_existe(conta_origem) and self.conta_existe(conta_destino):
            cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (conta_origem,))
            saldo_origem = cursor.fetchone()[0]
            if saldo_origem >= valor:
                cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE numero_conta = ?", (valor, conta_origem))
                cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE numero_conta = ?", (valor, conta_destino))
                conn.commit()
                self.label.text = f'Transferência de R${valor:.2f} realizada com sucesso!'
            else:
                self.label.text = 'Saldo insuficiente para transferência!'
        else:
            self.label.text = 'Conta origem ou destino não encontrada!'

    def consultar_saldo(self, instance):
        numero_conta = self.input_conta.text
        
        if self.conta_existe(numero_conta):
            cursor.execute("SELECT saldo FROM contas WHERE numero_conta = ?", (numero_conta,))
            saldo = cursor.fetchone()[0]
            self.label.text = f'Saldo atual: R${saldo:.2f}'
        else:
            self.label.text = 'Conta não encontrada!'

    def conta_existe(self, numero_conta):
        cursor.execute("SELECT * FROM contas WHERE numero_conta = ?", (numero_conta,))
        return cursor.fetchone() is not None

if __name__ == '__main__':
    BankApp().run()
