# CryptoAlerts

Uma interface customizável que monitora cryptocurrencies a fim de lhe manter informado sobre quaisquer novos movimentos, sem a necessidade de passar o dia acompanhando gráficos.

## Flags

### Symbols

Pode ser indicado pelas flags -s ou --symbols. Determina as cotações que serão analisadas, seguindo o padrão de symbols da Novadax·

```
BTC_BRL => Bitcoin/Real Brasileiro
ETH_BRL => Ethereum/Real Brasileiro
LTC_BRL => Litecoin/Real Brasileiro
WAVES_USDT => Waves/USDT
OMG_USDT => OMG/USDT
ADA_EUR => ADA/Euro
NPXS_EUR => NPXS/Euro

Outras relações seguirão o mesmo padrão
```

```console
foo@bar:~$ python3 CryptoAlerts.py -s BTC_BRL,ADA_BRL,XMR_BRL,XLM_BRL
```

### Times

Pode ser indicado pelas flags -t ou --times. Determina os gráficos que serão analisados, seguindo o padrão de unidade da Novadax.

```
ONE_MIN => 1 minuto
FIVE_MIN => 5 minutos
FIFTEEN_MIN => 15 minutos
HALF_HOU => 30 minutos
ONE_HOU = 1 hora
ONE_DAY = 1 dia
ONE_WEE = 1 semana
ONE_MON = 1 mês
```

```console
foo@bar:~$ python3 CryptoAlerts.py -t HALF_HOU,ONE_HOU,ONE_DAY
```

### Windows

Pode ser indicado pelas flags -w ou --windows. Determina as janelas de tempo nas quais serão verificadas as médias móveis, caso deseje tal informação.

```console
foo@bar:~$ python3 CryptoAlerts.py -w 9,10,21,60,80
```

### Limits

Pode ser indicado pelas flags -l ou --limits. Determina preços limite às relações, de forma a ser alertado quando um limite é rompido. Informe o symbol seguido do preço.

```console
foo@bar:~$ python3 CryptoAlerts.py -l BTC_BRL,105439.50,ETH_BRL,3400
```

### Bollinger Bands

Pode ser indicado pelas flags -b ou --bollinger. Determina um número de períodos específico para análise das bandas de bollinger, caso deseje monitorar os ativos utilizando tal ferramenta.

```console
foo@bar:~$ python3 CryptoAlerts.py -b 20
```

## Progress

No presente momento, CryptoAlerts executa quase todas as funções propostas, exceto identificar automaticamente suportes e resistências e o alertar sobre isso.
