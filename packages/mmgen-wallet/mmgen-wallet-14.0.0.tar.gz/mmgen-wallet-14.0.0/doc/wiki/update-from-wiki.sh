#!/bin/bash

CUR_DIR=$(dirname $0)
WIKI_DIR=$(realpath --relative-to $PWD $CUR_DIR/../../wiki)
echo "Copying changed files from '$WIKI_DIR' to '$CUR_DIR'"
declare -A DIRS=(
	[install-linux]='
		Install-Bitcoind-from-Source-on-Linux.md
		Install-Bitcoind.md
		Install-MMGen-Wallet-on-Linux.md'
	[install-mswin]='
		Install-Bitcoind.md
		Install-MMGen-Wallet-on-Microsoft-Windows.md'
	[using-mmgen-wallet]='
		Getting-Started-with-MMGen-Wallet.md
		Altcoin-and-Forkcoin-Support.md
		Tracking-and-spending-ordinary-Bitcoin-addresses.md
		Recovering-Your-Keys-Without-the-MMGen-Wallet-Software.md
		MMGen-Wallet-Quick-Start-with-Regtest-Mode.md
		Subwallets.md
		XOR-Seed-Splitting:-Theory-and-Practice.md
		Tool-API.md
		Test-Suite.md'
)

for i in ${!DIRS[*]}; do
	for j in ${DIRS[$i]};do
		out=$(rsync -a --info=name $WIKI_DIR/$j $CUR_DIR/$i/${j//\:}) # ':' is illegal in FAT/NTFS
		[ "$out" ] && echo '-->' $i/$out
	done
done
