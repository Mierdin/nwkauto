i=0

rm -f ./hosts

echo "[vsrx]" >> hosts

vagrant ssh-config | grep Port | while read -r line ; do
    i=$((i+1))
    echo "vsrx0$i" ${line//Port / ip_addr=127.0.0.1 ncssh_port=} >> hosts
done
