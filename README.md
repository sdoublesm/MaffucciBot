# MaffucciBot
![LOGO](/assets/logo.jpg "LOGO")

Bot che, al momento della pubblicazione di un nuovo articolo sul sito web dell'Istituto Maffucci di Calitri, invia una notifica sul canale Telegram [@IstitutoMaffucci](https://t.me/IstitutoMaffucci).

Si tratta sostanzialmente un RSS reader che al momento dell'esecuzione opera un controllo sui link presenti nel feed RSS del sito web dell'Istituto (disponibile al link https://istitutosuperioremaffucci.edu.it/feed/) e li confronta con quelli presenti nel "database", che non è altro che il file ``.txt`` denominato ``feed_datab.txt``.

L'esecuzione dello script ``main.py`` è unica e, per far sì che il controllo avvenga periodicamente (ogni 2 minuti è già più che sufficiente), vi è la necessità di impostare un ``cronjob`` o una soluzione analoga. Lo script ``asyncmain.py`` sfrutta invece una funzione asincrona quindi esegue in loop il controllo ogni minuto.

## Replit Version
Il file ``replit.py`` contiene invece una versione dello script MOLTO GREZZA (creata solo per testing) ideata per l'hosting più che spartano su Replit. L'idea di base è eseguire lo script alla ricezione di richieste HTTP, che vengono inviate molto frequentemente da [UptimeRobot](https://uptimerobot.com/) a ``https://maffuccibot.sdoublesm.repl.co/``, e di successivo feedback ``200 OK``.
## Screenshot
![Screenshot](/assets/screenshot.jpg "screenshot")
