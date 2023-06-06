//Universidade Estadual do Rio Grande do Sul
//Disciplina: IA - 2023
//Aluno: Fernando Caletti de Barros
//Atividade 04 - 2
/** ***************************************************************
 * Agente com Id visual
 * retorna a foto (imagem) quando pedido
 **************************************************************** */
package AgenteRoom;

import jade.core.Agent;
import jade.core.behaviours.*;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;

public class AgenteRoom extends Agent
{
    private double custoPorOperacao = 0.00;
    
    private boolean serviceResult = true;
    
    @Override
    protected void setup()
    {
        ParseArgs();
        
        System.out.println("Ola! Eu sou " + getLocalName());
        System.out.println("Meu custo é: " + custoPorOperacao);


        ServiceDescription sd = new ServiceDescription();
        sd.setType("corte");
        sd.setName("Serra1");
        sd.setOwnership(getLocalName());
        register(sd);

        addBehaviour(new CyclicBehaviour(this)
        {
            public void action()
            {
                ACLMessage msg = receive();
                if (msg != null)
                {
                    ACLMessage reply = msg.createReply();
                    
                    if(msg.getContent().equals("custoOperacao") && (msg.getPerformative() == ACLMessage.CFP))
                    {
                        reply.setPerformative(ACLMessage.PROPOSE);
                        reply.setContent("custoOperacao");
                        reply.addUserDefinedParameter("custo", Double.toString(custoPorOperacao));
                        send(reply);
                    }
                    
                    if(msg.getContent().equals("executarServico") && (msg.getPerformative() == ACLMessage.ACCEPT_PROPOSAL))
                    {
                        if(serviceResult)
                        {
                            reply.setPerformative(ACLMessage.INFORM);
                            reply.setContent("concluido");
                            send(reply);    
                            serviceResult = false;
                        }
                        else
                        {
                            reply.setPerformative(ACLMessage.FAILURE);
                            reply.setContent("error");
                            send(reply);    
                            serviceResult = true;
                        }
                        
                    }
                    
                    if(msg.getContent().equals("retentarServico") && (msg.getPerformative() == ACLMessage.REQUEST))
                    {
                        reply.setPerformative(ACLMessage.AGREE);
                        reply.setContent("aceito");
                        send(reply);   
                        
                        reply.setPerformative(ACLMessage.INFORM);
                        reply.setContent("concluido");
                        send(reply);   
                    }

                    
                    if(msg.getContent().equals("rejeitaServico") && (msg.getPerformative() == ACLMessage.REJECT_PROPOSAL))
                    {
                        //Servico rejeitado, não faz nada...
                    }
                }
                block();
            }
        });
    }

    protected void takeDown()
    {
        try
        {
            DFService.deregister(this);
        } catch (FIPAException e)
        {
        }
        doDelete();
    }

    void register(ServiceDescription sd)
    {
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(getAID());
        dfd.addServices(sd);

        try
        {
            DFService.register(this, dfd);
        } catch (FIPAException fe)
        {
        }
    }

    private void ParseArgs()
    {
        Object[] args = getArguments();
        custoPorOperacao = Double.parseDouble((String)args[0]);
    }
}
