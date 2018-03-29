#!/bin/bash

projectDir=$1
questionSourceFile=$2

cd $projectDir
auto-multiple-choice prepare --mode s --prefix $projectDir/pdfName $questionSourceFile
#auto-multiple-choice prepare --mode s --prefix /home/bill/Documents/AMCScripts/someName simple.tex

