# Experimento 007 — Clima na matriz de LEDs

Este protótipo consulta a condição atual do tempo pela API Open-Meteo no Linux do Arduino UNO Q e mostra o resultado na matriz azul 8×13 integrada à placa.

- **Tempo bom:** sol animado.
- **Tempo ruim ou instável:** nuvem com chuva.
- **Sem conexão/API:** interrogação piscando.

A classificação inicial considera códigos WMO `0`, `1` e `2` como tempo bom. Os outros códigos são exibidos como tempo ruim/instável. A API não exige chave. A consulta se repete a cada 10 minutos.

## Arquivos do App Lab

Crie um App no Arduino App Lab e copie:

- `python/main.py` para `python/main.py` do App.
- `sketch/sketch.ino` para `sketch/sketch.ino` do App.

A placa precisa estar conectada a uma rede Wi-Fi com acesso à internet. No topo de `python/main.py`, `LATITUDE` e `LONGITUDE` estão configuradas para Rio Branco, Acre. Altere os valores se quiser consultar outra cidade.

Clique em **Run** no App Lab. A aba Python do Console mostra a temperatura, o código do clima e eventuais erros. O padrão da matriz é atualizado depois de cada consulta.

## Como funciona

O script Python usa `urllib` (biblioteca padrão) para buscar `current=weather_code,temperature_2m` na API Open-Meteo. Ele envia o estado numérico `0` (bom), `1` (ruim/instável) ou `2` (erro) ao sketch pela chamada `Bridge.call("set_weather_state", estado)`. O sketch desenha e anima os quadros na matriz integrada.

## Limites desta primeira versão

“Bom” e “ruim” são uma simplificação para demonstrar o fluxo completo. A classificação não leva em conta preferências pessoais nem previsão futura. Depois, o experimento pode incluir chuva, temperatura e vento, ou receber uma cidade pela interface.
