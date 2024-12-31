import wx, LLM


def Init():
    global IA
    IA = LLM.Homeostasis()
    app = wx.App(False)
    frame = Home(None, title="Sistema de Controle Sanguineo")
    frame.Show()
    app.MainLoop()



class Home(wx.Frame):
    def __init__(self, *args, **kw):
        super(Home, self).__init__(*args, **kw)
        
        self.panel = wx.Panel(self)
        
        # Botões
        btn_calculadora = wx.Button(self.panel, label="Calculadora de Compatibilidade", pos=(20, 20))
        btn_fulano = wx.Button(self.panel, label="Fulano Doa/Recebe Para/De Quem?", pos=(20, 60))
        btn_encontrar_fator = wx.Button(self.panel, label="Encontrar Pessoas Com Sangue X ou RH Y", pos=(20, 100))


        # Eventos
        btn_calculadora.Bind(wx.EVT_BUTTON, self.telaCompatibilidade)
        btn_fulano.Bind(wx.EVT_BUTTON, self.telaDoadorReceptor)
        btn_encontrar_fator.Bind(wx.EVT_BUTTON, self.telaIdentificarPessoas)

	
	# Configurações
        self.SetSize((400, 200))
        self.SetTitle("Home")
        self.Centre()
        self.Show()

    def telaCompatibilidade(self, event):
        compatibilidade_frame = Compatibilidade(None)
        compatibilidade_frame.Show()     

    def telaDoadorReceptor(self, event):
        DoarReceber_frame = Doador_Receptor(None)
        DoarReceber_frame.Show()

    def telaIdentificarPessoas(self, event):
        encontrar_fator_frame = identificarPessoas(None)
        encontrar_fator_frame.Show()


class Compatibilidade(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
	# Configurações
        self.SetTitle("Compatibilidade")
        self.SetSize((450, 750))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Inputs
        self.nome_doador_label = wx.StaticText(panel, label="Informações do Doador:")

        self.idade_label = wx.StaticText(panel, label="Idade:")
        self.idade_input = wx.TextCtrl(panel)

        self.peso_label = wx.StaticText(panel, label="Peso(kg):")
        self.peso_input = wx.TextCtrl(panel)

        self.tipo_doador_label = wx.StaticText(panel, label="Tipo Sanguíneo (O, A, B, AB):")
        self.tipo_doador_input = wx.TextCtrl(panel)

        self.rh_doador_label = wx.StaticText(panel, label="Fator Rh(+/-):")
        self.rh_doador_input = wx.TextCtrl(panel)

        self.nome_receptor_label = wx.StaticText(panel, label="Informações do Receptor:")

        self.tipo_receptor_label = wx.StaticText(panel, label="Tipo Sanguíneo(O, A, B, AB):")
        self.tipo_receptor_input = wx.TextCtrl(panel)

        self.rh_receptor_label = wx.StaticText(panel, label="Fator Rh (+/-):")
        self.rh_receptor_input = wx.TextCtrl(panel)
        
        # Botões
        self.check_button = wx.Button(panel, label="Confirmar")
        self.result_label = wx.StaticText(panel, label="")
        
        # Layout
        for widget in [
            self.nome_doador_label,
            self.idade_label, self.idade_input, self.peso_label, self.peso_input,
            self.tipo_doador_label, self.tipo_doador_input, self.rh_doador_label, self.rh_doador_input,
            self.nome_receptor_label, self.tipo_receptor_label, self.tipo_receptor_input, self.rh_receptor_label, self.rh_receptor_input,
            self.check_button, self.result_label
        ]:
            sizer.Add(widget, flag=wx.EXPAND | wx.ALL, border=5)
        
        panel.SetSizer(sizer)
        
        # Eventos
        self.check_button.Bind(wx.EVT_BUTTON, self.verificar)
    
    def verificar(self, event):
        try:
            idade = int(self.idade_input.GetValue())
            peso = float(self.peso_input.GetValue())
            tipo_doador = self.tipo_doador_input.GetValue().strip().lower()
            rh_doador = self.rh_doador_input.GetValue().strip().lower()
            tipo_receptor = self.tipo_receptor_input.GetValue().strip().lower()
            rh_receptor = self.rh_receptor_input.GetValue().strip().lower()
            
            resultado = IA.pode_doar(idade, peso, tipo_doador, rh_doador, tipo_receptor, rh_receptor)
            self.result_label.SetLabel(resultado)
        except ValueError:
            self.result_label.SetLabel("Erro: Certifique-se de preencher os campos corretamente.")

class identificarPessoas(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
	# Configurações
        self.SetTitle("Buscador")
        self.SetSize((400, 400))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Inputs
        self.tipo_Sanguineo_label = wx.StaticText(panel, label="Tipo Sanguíneo:")
        self.tipo_input = wx.TextCtrl(panel)
        self.espaco = wx.StaticText(panel, label="")
        self.fator_rh_label = wx.StaticText(panel, label="Fator RH:")
        self.fator_input = wx.TextCtrl(panel)

        # Botões
        self.check_buttonTipo = wx.Button(panel, label="Buscar")
        self.result_labelTipo = wx.StaticText(panel, label="")

        self.check_buttonFator = wx.Button(panel, label="Buscar")
        self.result_labelFator = wx.StaticText(panel, label="")

        # Layout
        for widget in [
            self.tipo_Sanguineo_label,
            self.tipo_input, self.check_buttonTipo, self.result_labelTipo, 
            self.espaco, self.fator_rh_label, 
            self.fator_input, self.check_buttonFator, self.result_labelFator
        ]:
            sizer.Add(widget, flag=wx.EXPAND | wx.ALL, border=5)
        
        panel.SetSizer(sizer)

        # Eventos
        self.check_buttonTipo.Bind(wx.EVT_BUTTON, self.verificarTipo)
        self.check_buttonFator.Bind(wx.EVT_BUTTON, self.verificarFator)
        
    def verificarTipo(self, event):
        try:
            tipo = self.tipo_input.GetValue().strip().lower()
            resultadoTipo = IA.identificar_pessoas(tipo_sanguineo=tipo)
            self.result_labelTipo.SetLabel(resultadoTipo)
        except ValueError:
            self.result_labelTipo.SetLabel("Erro: Certifique-se de preencher os campos corretamente.")

    def verificarFator(self, event):
        try:
            fator = self.fator_input.GetValue().strip()
            resultadoFator = IA.identificar_pessoas(fatorrh=fator)
            self.result_labelFator.SetLabel(resultadoFator)
        except ValueError:
            self.result_labelFator.SetLabel("Erro: Certifique-se de preencher os campos corretamente.")
        
class Doador_Receptor(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
	# Configurações
        self.SetTitle("Doador/Receptor")
        self.SetSize((400, 400))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Inputs
        self.tipo_Sanguineo_label2 = wx.StaticText(panel, label="Inserir nome:")
        self.nome_input = wx.TextCtrl(panel)
        self.espaco = wx.StaticText(panel, label="")

        # Botões
        self.check_buttonTipo = wx.Button(panel, label="Buscar")
        self.result_label = wx.StaticText(panel, label="")

        # Layout
        for widget in [
            self.tipo_Sanguineo_label2, self.nome_input,
            self.espaco, self.check_buttonTipo, self.result_label
        ]:
            sizer.Add(widget, flag=wx.EXPAND | wx.ALL, border=5)
        
        panel.SetSizer(sizer)

        # Eventos
        self.check_buttonTipo.Bind(wx.EVT_BUTTON, self.verificarTipo)
        
    def verificarTipo(self, event):
        try:
            nome = self.nome_input.GetValue().strip().lower()
            resultadoTipo = IA.DoadorReceptor(nome)
            self.result_label.SetLabel(resultadoTipo)
        except ValueError:
            self.result_label.SetLabel("Erro: Certifique-se de preencher os campos corretamente.")
        

