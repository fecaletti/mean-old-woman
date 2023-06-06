//Universidade Estadual do Rio Grande do Sul
//Disciplina: IA - 2023
//Aluno: Fernando Caletti de Barros
//Atividade 04 - 1

package AgenteClass;

import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.*;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.SearchConstraints;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import static jade.tools.sniffer.Agent.i;
import jade.util.leap.Properties;
import java.util.Enumeration;
import java.util.ArrayList;
import java.util.Map;
import java.util.TreeMap;
import java.util.Set;

/**
 * Agente Class: <br>
 * -procura agentes no alcance e solicita informacoes <br>
 * -protocolo: comando "enviaStatus" para solicitar informacoes
 */
public class AgenteClass extends Agent
{
    AID agentes[];
    ArrayList<AID> agentesRequisitados = new ArrayList<AID>();

    int msgEnviadas = 0;

    int msgRecebidas = 0;
    
    Map<AID, Double> custoPorAgente = new TreeMap<AID, Double>();
    
    boolean aguardandoServico = false;
    
    @Override
    protected void setup()
    {
        System.out.println("Ola! Eu sou " + getLocalName());

        // Mostra mensagens recebidas
        addBehaviour(new CyclicBehaviour(this)
        {
            public void action()
            {
                // Processa mensagens recebidas
                ACLMessage msg = receive();
                if (msg != null)
                {
                    msgRecebidas++;
                    System.out.print("Mensagem enviada por:");
                    System.out.println(msg.getSender());
                    
//                    mostraMensagem(msg);
                    System.out.println("Recebido -> " + msg.getContent() + " - " + msg.getPerformative());
                    if(msg.getContent().equals("custoOperacao") && (msg.getPerformative() == ACLMessage.PROPOSE))
                    {
                        Properties propriedades = msg.getAllUserDefinedParameters();
                        Object custo = propriedades.get("custo");
                        
                        custoPorAgente.put(msg.getSender(), Double.parseDouble((String)custo));
                    }
                    
                    
                    
                    if(msg.getContent().equals("error") && (msg.getPerformative() == ACLMessage.FAILURE))
                    {
                        ACLMessage reply = new ACLMessage(ACLMessage.REQUEST);
                        reply.setContent("retentarServico");
                        reply.addReceiver(msg.getSender());
                        send(reply);
                    }
                    
                    
                    if(msg.getContent().equals("concluido") && (msg.getPerformative() == ACLMessage.INFORM))
                    {
                        aguardandoServico = false;
                        agentesRequisitados.clear();

                    }
                }
                block();
            }
        });

        // Mostra agentes que estao no ar
        addBehaviour(new TickerBehaviour(this, 5000)
        {
            protected void onTick()
            {
                System.out.println("");
                System.out.println(myAgent.getLocalName() + ":AgenteClass");
                System.out.println("Estao no ar:");
                agentes = buscaAgentes("");
                if (agentes.length == 0)
                {
                    System.out.println("Nenhum :/ ");
                } else
                {
                    for(int i=0;i<agentes.length;i++)
                        System.out.println(agentes[i].getLocalName());
                }

                System.out.println("");
                System.out.println("Enviadas:" + Integer.toString(msgEnviadas) + "; Recebidas:" + Integer.toString(msgRecebidas));
            }
        });

        // Polling dos agentes
        addBehaviour(new TickerBehaviour(this, 2000)
        {
            protected void onTick()
            {
                if (agentes != null)
                {
                    for (AID agente : agentes)
                    {
                        if(agentesRequisitados.contains(agente))
                            continue;
                        
                        ACLMessage msg = new ACLMessage(ACLMessage.CFP);
                        msg.setContent("custoOperacao");
                        msg.addReceiver(agente);
                        send(msg);
                        msgEnviadas++;
                        agentesRequisitados.add(agente);
                    }    
                    
                    
                    System.out.println("Temos -> " + custoPorAgente.size());
                    
                    //Todos os agentes já retornaram seus custos?
                    if(agentes.length == custoPorAgente.size())
                    {
                        double menorCusto = Double.MAX_VALUE;
                        AID agenteAlvo = null;

                        Set<AID> keys = custoPorAgente.keySet();
                        for(AID agent : keys)
                        {
                            double custo = custoPorAgente.get(agent);
                            if(custo >= menorCusto)
                                continue;

                            menorCusto = custo;
                            agenteAlvo = agent;
                        }

                        //Requisita serviço para agente com menor custo
                        RequisitaServico(agenteAlvo, menorCusto);
                        aguardandoServico = true;
                        //Rejeita demais servicos
                        for(AID agent : keys)
                        {
                            if(agent == agenteAlvo)
                                continue;

                            RejeitaProposta(agent);
                        }
                        //Reseta map
                        custoPorAgente.clear();
                    }
                }
            }
        });
    }

    private boolean RequisitaServico(AID agente, double valor)
    {
        System.out.println("Requisitando servico para " + agente + " com o custo de " + valor + "...");
        ACLMessage msg = new ACLMessage(ACLMessage.ACCEPT_PROPOSAL);
        msg.setContent("executarServico");
        msg.addReceiver(agente);
        send(msg);
        return true;
    }
    
    private boolean RejeitaProposta(AID agente)
    {
        System.out.println("Rejeitando proposta de " + agente + "...");
        ACLMessage msg = new ACLMessage(ACLMessage.REJECT_PROPOSAL);
        msg.setContent("rejeitaServico");
        msg.addReceiver(agente);
        send(msg);
        return true;
    }
    
    AID[] buscaAgentes(String service)
    {
        if(aguardandoServico == true)
            return agentes;
        
        DFAgentDescription dfd = new DFAgentDescription();
        ServiceDescription sd = new ServiceDescription();
        //sd.setType(service);
        dfd.addServices(sd);

        SearchConstraints ALL = new SearchConstraints();
        ALL.setMaxResults(new Long(-1));

        try
        {
            DFAgentDescription[] result = DFService.search(this, dfd, ALL);
            AID[] agentes = new AID[result.length];
            for (i = 0; i < result.length; i++)
            {
                agentes[i] = result[i].getName();
            }
            return agentes;

        } catch (FIPAException fe)
        {
            fe.printStackTrace();
        }

        return null;
    }
    
    void mostraMensagem(ACLMessage msg)
    {
        Properties propriedades = msg.getAllUserDefinedParameters();
        Enumeration parametros = propriedades.keys();
        String parametro;
        String valor;
        //System.out.println(msg.toString());
        while (parametros.hasMoreElements())
        {
            parametro = (String) parametros.nextElement();
            valor = (String) propriedades.getProperty(parametro);
            System.out.print(parametro);
            System.out.print(":");
            System.out.println(valor);
        }
    }    
}
