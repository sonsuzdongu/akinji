# akinji
socket.io stress testing / benchmarking tool

# prerequisites
<pre>pip install socketIO-client</pre>

# usage

Command below opens 100 sockets to locahost:3000, waits for 100 seconds and listens for "some msg" and print those messages

<pre>python akinji.py -c 100 --host localhost --port 3000 --waitFor 100 --on "some msg"</pre>

# known issues
CTRL+C doesnt work since threads joined. you may need to kill the process from another shell
