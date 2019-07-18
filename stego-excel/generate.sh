#!/usr/bin/env bash
set -euo pipefail

if ! which bsdtar &>/dev/null; then
    echo 'Error: bsdtar is not installed, but it is required to generate the task'
    exit 1
fi

if ! which python3 &>/dev/null; then
    echo 'Error: python3 is not installed, but it is required to generate the task'
    exit 1
fi

FLAG='LKLCTF{3XceL_F1Le_i5_n0t_0n1Y_a_T4blE_2be0915a_4810eac0}'

shopt -s dotglob
set -x

rm -f 'Transactions-info.xlsx'
python3 ./gen-helper.py

rm -rf 'tmp'
mkdir -p 'tmp'
cd 'tmp'
bsdtar -xf ../Transactions-info.xlsx
printf "<!-- %s -->\n" "${FLAG}" >> 'xl/styles.xml'
bsdtar -cavf ../Transactions-info.zip *
cd ..
mv Transactions-info.zip Transactions-info.xlsx
