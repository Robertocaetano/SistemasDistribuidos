#SISTEMAS DISTRIBUÍDOS
#ROBERTO JUNIO SILVA CAETANO
#11821ECP001

import threading
import time


#definição da Thread e o processamento de cada uma
class myThread (threading.Thread):
    def __init__ (self, id):
        threading.Thread.__init__(self)
        self.id = id
        self.awake = False
        self.text = ''
        self.next = None
        self.finished = False

    def setNext(self, next):
        self.next = next

    def run(self):
        print(f'Thread {self.id} - Esta funcionando')

        #Roda enquanto não finalizar o processo
        while not self.finished:
            #Se não deve acordar. Volta a dormir por 1 segundo
            if not self.awake:
                time.sleep(1)

            #Se for minha vez de acordar
            else:
                #Flag pra checar se eu achei alguma letra minuscula
                find = False
                #laço para verificar 
                for i in range (0, len(self.text)):
                    #método islower() para verificar se possui letra minúscula no text repassado, 
                    # se possui, seta a flag find como true e realiza a mudança da ultima letra encontrada
                    #Quando achar a primera minuscula
                    #Faz a troca e quebra o laço
                    if self.text[i].islower():
                        find = True
                        self.text = self.text[:i] + self.text[i].upper() + self.text[i+1:]
                        break

                #Se eu fiz alguma troca, volto a dormir por 1 segundo e acordo a proxima Thread
                if find:
                    #imprime o texto modificado
                    print(f'Thread#{self.id} -- {self.text}')
                    #coloa a Thread pra durmir
                    self.awake = False
                    #acorda a proxima Thread
                    self.next.wakeUp(self.text)
                #Se nao fiz troca, o trabalho esta terminado
                else: 
                    #logo o trabalho está terminado
                    self.finished = True
                    

        #Agora que eu sei que ja terminei, aviso a proxima Thread para encerrar os trabalhos
        self.next.finished = True
        print(f'Thread#{self.id} - Terminado..')
    
    #acorda a Thread e recebe o texto para processar
    def wakeUp(self, text):
        self.text = text
        self.awake = True

class Anel:
    def __init__(self, n):
        #inicio do anel com o número de threads repassados via input anteriormente
        #onde self.threads recebera uma lista da class myThread
        self.threads = [myThread(i) for i in range(0, n)]
        #laço fechando o Anel definindo a posição da Thread nele 
        for i in range(0, n-1):
            self.threads[i].setNext(self.threads[i+1])
        self.threads[n-1].setNext(self.threads[0])

    #processamento do anel
    def start(self, text):
        for t in self.threads:
            t.start()
        self.threads[0].wakeUp(text)

    def join(self):
        for t in self.threads:
            t.join()

def main():
    #Recebo o número de Threads a serem utilizadas
    numberOfThreads = int(input('Digite número de Threads a ser utilizadas: '))
    #inicializo o anel
    anel = Anel(numberOfThreads)
    #Recebo a string a ser tratada
    text = input('Digite uma string a ser tratada pelas threads:')
    #processa anel
    anel.start(text)
    #metodo invocado para executar o anel até que a thread termine para evitar deadlock
    anel.join()

main()