#!/bin/bash
cd /home/user/AImodel/DS/ChatLog/PhD_PM_FANS/code/V/A
export MPLCONFIGDIR=/tmp/mpl
PY=/home/user/anaconda3/bin/python
for f in CycloPropane Propane R134a 1-Butene IsoButene R1234yf "R1233zd(E)" n-Butane R245fa Benzene CycloPentane R218 n-Pentane Toluene CycloHexane n-Hexane n-Octane MM n-Decane MDM D4 MD3M D6; do
  echo "### $f"
  timeout 300 $PY fig15_fluid_scan.py "$f" 2>&1 | tail -8
  echo
done
echo "ALL DONE"
