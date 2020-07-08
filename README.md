# Algo Positivo
Projeto integrador do 2º período de Análise e Desenvolvimento de Sistemas, Faculdade de Tecnologia de São José dos Campos.
Este é um projeto da parceria entre a FATEC de São José dos Campos e a SPC Brasil.

## Motivação
Com a mudança do modelo de operação do Cadastro Positivo, surgiu a necessidade de
realizar uma gestão de informação mais eficaz para garantir a qualidade, o uso adequado e
gerar valor através dos dados. E para gerar valor através destes dados, será mapeado de
forma geral o perfil dos clientes, de modo que a área de marketing possa compreender
melhor quem são seus clientes e criar campanhas mais assertivas para determinado nicho,
ajudando na tomada de decisões.

## Solução 
Um software capaz de analisar dados e gerar um relatório com informações dos clientes,
contendo alguns indicadores que serão úteis para a equipe da área de marketing da SPC
Brasil.

## Funcionamento 
Será desenvolvido um programa em Python onde ele será responsável por gerar as
informações úteis e enviar para todos os e-mails cadastrados em um banco de dados
SQLite3.

Os dados que serão gerados são: total e média de idade dos clientes por região, estado,
sexo, faixa etária, quantidade de transações por modalidade de cada região e faixa etária. Os
mesmos serão enviados no formato de arquivo JSON para que possa ser aberto em outras
ferramentas de análise como Excel.

Primeiramente o programa vai ler os dados dos clientes e de operações para extrair as
informações necessárias para então realizar a análise, evitando dados incompletos como
operações com IDs de pessoas não cadastradas na base ou estado não encontrado.
Após a filtragem para obter dados confiáveis o programa passa para a etapa de analise e
gerir os dados que serão usados pela área de marketing.
Por fim, após estar pronto o arquivo com os dados úteis, eles serão enviados de forma
automática para os endereços de e-mail cadastrados.

## Visão do usuário final 
Obs.: O usuário não executará o programa, isto só foi feito para que os dados fossem enviados, para fins de demonstração.  
![previa](https://github.com/IsraelAugusto0110/PI_ADS_2Sem/blob/master/Ignorar/Previa.gif)

Imagem pequena ? Então [*clique aqui*](https://github.com/IsraelAugusto0110/PI_ADS_2Sem/blob/master/Ignorar/Previa.gif).  
Os dados enviados podem ser encontrados [*clicando aqui*](https://github.com/IsraelAugusto0110/PI_ADS_2Sem/blob/master/C%C3%B3digos/Dados/Final/estados.json).

## Utilidades
| [*Código-fonte*](https://github.com/IsraelAugusto0110/PI_ADS_2Sem/blob/master/C%C3%B3digos/algopositivo.pyw)
| [*Documento de Visão*](https://github.com/IsraelAugusto0110/PI_ADS_2Sem/blob/master/Documenta%C3%A7%C3%A3o/Documento-de-Vis%C3%A3o.pdf)
| [*Diagrama de fluxo de dados*](https://github.com/IsraelAugusto0110/PI_ADS_2Sem/blob/master/Documenta%C3%A7%C3%A3o/Fluxo-de-Dados.pdf)
| [*Backlog*](https://github.com/IsraelAugusto0110/PI_ADS_2Sem/blob/master/Documenta%C3%A7%C3%A3o/Backlog.pdf) |

## Desenvolvedores
| [*Wesley Dias (PO)*](https://www.linkedin.com/in/wesley-dias-bba3a11b2/)
| [*Israel Augusto (MASTER)*](https://www.linkedin.com/in/israel-augusto-santos-4651b7197)
| [*Denis Lima*](https://www.linkedin.com/in/denis-f-lima)
| [*Natalia Biscaro*](https://br.linkedin.com/in/nataliabiscaro)
| [*Euclides Rezende*](https://www.linkedin.com/in/euclides-rezende-0940458/) |
