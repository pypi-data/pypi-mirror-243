# readdbc
Um pacote python para ler dados no formato DBC (DBF comprimido) usado pelo DATASUS.  


# Uso
O código abaixo descompactará o arquivo `COLEBR15.dbc` e salvará o conteúdo em `COLEBR15.dbf`.
```
import readdbc

readdbc.dbc2dbf('COLEBR15.dbc', 'COLEBR15.dbf')
```

Esse descompacta e ja converte para .csv:
```
import readdbc

readdbc.dbc2csv('COLEBR15.dbc', 'COLEBR15.csv')
```


# Suporte
O pacote é testado em todas as versões oficiais do python (3.8 até a 3.12).  
Também testado em GNU/Linux e MacOS.  
Caso descubra algum bug ou comportamento inesperado nessas versões e plataforma, por favor entre em contato.  

Windows não é suportado por enquanto!  
Mas caso você seja um usuário do windows e queira ajudar, por favor entre em contato.  


# Inspiração
[read.dbc](https://github.com/danicat/read.dbc)  
An R package for reading data in the DBC (compressed DBF) format used by DATASUS.
