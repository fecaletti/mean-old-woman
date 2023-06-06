from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaRequestProtocol



class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour of the Time agent.
    """
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        if message == '':
            display_message(self.agent.aid.localname, 'request message received')
            now = datetime.now()
            reply = message.create_reply()
            reply.set_performative(ACLMessage.INFORM)
            reply.set_content(f'Enviando status => {now.strftime("%d/%m/%Y - %H:%M:%S")}')
            self.agent.send(reply)

class Pagent(Agent):
    def __init__(self, aid):
        super(Pagent, self).__init__(aid=aid)
        display_message(self.aid.localname, 'Hello World!')
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)

    def action(service):
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID('agente_destino'))
        message.set_content('Ola Agente')



if __name__ == '__main__':

    agents = list()
    port = int(argv[1])
    agent_name = 'agente_hello_pade{}@localhost:{}'.format(port, port)
    agente_hello = Pagent(AID(name=agent_name))
    agents.append(agente_hello)

    start_loop(agents)