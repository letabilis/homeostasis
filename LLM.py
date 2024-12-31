from swiplserver import PrologMQI

class Homeostasis():
    
    def __init__(self):
            self.API =  PrologMQI()
            self.prolog = self.API.create_thread()
            self.prolog.query("consult('conhecimento.pl').")


    def pode_doar(self, idade, peso, tipo_doador, rh_doador, tipo_receptor, rh_receptor):
                consulta = (
                    f"podedoar({idade}, {peso}, "
                    f"'{tipo_doador}', '{rh_doador}', "
                    f"'{tipo_receptor}', '{rh_receptor}')."
                )
                
                resultado = self.prolog.query(consulta)
                
                return "    Resultado: Compatíveis" if resultado else "    Resultado: Incompatíveis"
               
            
    def identificar_pessoas(self,  fatorrh=None, tipo_sanguineo=None):

                nomes = ""
                i = 0 

                if fatorrh is None:
                    resultado = self.prolog.query(f"tiposanguineo(X, {tipo_sanguineo}).")
                    
                    # Formatação
                    for nome in resultado:
                        nomes = nomes + nome['X'] + "," 
                        i += 1
                        if i == 3:
                            nomes = nomes + "\n"
                            i = 0 
        
                elif tipo_sanguineo is None:  # Se foi fornecido Fator Rh
                    resultado = self.prolog.query(f"fatorrh(X, {fatorrh}).")
                    
                    # Formatação
                    for nome in resultado:
                        nomes = nomes + nome['X'] + "," 
                        i += 1
                        if i == 3:
                            nomes = nomes + "\n"
                            i = 0

                return nomes

                

    def DoadorReceptor(self,  nomePessoa):
                '''
                Para quem Fulano pode doar sangue?
                De quem Fulano pode receber sangue?
                
                É isso que esta função resolve.
                
                Utilizamos a ideia de  Conjuntos para resolver este problema, em python Sets.
                
                Exemplo
                   
                   
                    Fulano: 
                        tiposanguineo(Fulano, X) : ab
                        fatorrh(Fulano, X): +
                    
                    Caso 1: 
                        De quem Fulano pode receber?
                            compativel(X, AB): [a, b, ab]
                            rhcomp(X, +): [-, +]
                    
                    Caso 2: 
                        Para quem Fulano pode doar?
                            compativel(AB, X): ...
                            rhcomp(+, X): ...


                    Para todo tipo sanguíneo resultante, pegue o nome dessas pessoas.
                        tiposanguineo(X, a)
                        tiposanguineo(X, b)
                        tiposanguineo(x, ab)

                    Para todo fator rh resultante, pegue o nome dessas pessoas.
                        fatorrh(X, -)
                        fatorrh(X, +)

                    Pegue as pessoas em comum.
                   
                    
               
                '''
                
                doadores, receptores = "Doa para:\n    ", "Recebe de:\n    "
                

                # Dados iniciais da pessoa.
                idade = self.prolog.query(f"idade({nomePessoa}, X).")[0]['X']
                peso = self.prolog.query(f"peso({nomePessoa}, X).")[0]['X']
                tipo_sanguineo = self.prolog.query(f"tiposanguineo({nomePessoa}, X).")[0]['X']
                fator_rh = self.prolog.query(f"fatorrh({nomePessoa}, X).")[0]['X']


                # Caso 0: Pessoa não identificada na base de dados.
                if not idade or not peso:
                    return f"{nomePessoa} não encontrada na base de dados!"
                

                # Caso 1: Observar Situacao Fisica
                resultado_teste_aptidao = self.prolog.query(f"aptidao({idade}, {peso}).")

                
                if resultado_teste_aptidao: # Resultado Não Nulo == Apto Para DOAR.
                    # Pra quem?


                    tipos_compativeis = self.prolog.query(f"compativel({tipo_sanguineo}, X).") 
                    # Exemplo de saída: [a, ab]


                    rh_compativeis = self.prolog.query(f"rhcomp({fator_rh}, X).") 
                    # Exemplo de saída: [+]
                    

                    # Conjuntos 
                    pessoas_tipo_compativeis = set()
                    pessoas_rh_compativeis = set()
                        

                    # Adicionando pessoas aos seus respectivos conjuntos.
                    for tipo in tipos_compativeis:
                        resultado = self.prolog.query(f"tiposanguineo(X, {tipo['X']}).")
                        for nome in resultado:
                            pessoas_tipo_compativeis.add(nome['X'])


                   
                    for rh in rh_compativeis:
                        resultado = self.prolog.query(f"fatorrh(X, {rh['X']}).")
                        for nome in resultado:
                           pessoas_rh_compativeis.add(nome['X'])
                    


                    # Resultado == Interseção
                    doa_para = pessoas_tipo_compativeis.intersection(pessoas_rh_compativeis)
                    
    
                    # Formatação
                    i = 0
                    for nomepessoa in doa_para:
                        p = nomepessoa  +  "," 
                        i+=1
                        if i == 2:
                            i=0
                            p += "\n    "
                        doadores += p

                
                
                

                # De quem RECEBE?
                
                tipos_compativeis = self.prolog.query(f"compativel(X, {tipo_sanguineo}).")
                rh_compativeis = self.prolog.query(f"rhcomp(X, {fator_rh}).")
            

                # Conjuntos
                pessoas_tipo_compativeis = set()
                pessoas_rh_compativeis = set()



                # Adicionando pessoas aos seus CONJUNTOS.
                for tipo in tipos_compativeis:
                        resultado = self.prolog.query(f"tiposanguineo(X, {tipo['X']}).")
                        for nome in resultado:
                            pessoas_tipo_compativeis.add(nome['X'])

                

                for rh in rh_compativeis:
                    resultado = self.prolog.query(f"fatorrh(X, {rh['X']}).")
                    for nome in resultado:
                        pessoas_rh_compativeis.add(nome['X'])
                

                # Resultado == Interseção

                recebe_de = pessoas_tipo_compativeis.intersection(pessoas_rh_compativeis)
                  



                # Formatação
                i = 0
                for nomepessoa in recebe_de:
                    p = nomepessoa  +  "," 
                    i+=1
                    if i == 2:
                        i=0
                        p += "\n    "
                    receptores += p

                resposta = doadores + "\n" + receptores

                return resposta

        
