#!/bin/bash
cpath=`pwd`"/../../../Client/Assets/"

#get modify version
nowr=`svn info $cpath | grep Revision`
nowr=${nowr:${#nowr}-5:5}

yesterday=$(date -v -1d '+%Y-%m-%d')
yesterday=`svn info $cpath -r '{'$yesterday'}' | grep Revision`
yesterday=${yesterday:${#yesterday}-5:5}

for file in `svn log $cpath -r $nowr:$yesterday -v | grep "^ *M" | grep ".meta" | grep -v ".dll.meta" | grep -v ".unity.meta" | grep -v ".cs.meta"`
do
	if [[ $file =~ ".meta" ]]
	then
		tempname=${file:7:${#file}-7}
		tempname="/Users/build_leiting/LX6/trunk/"$tempname
		lastr=`svn log $tempname | grep line | sed -n '1p'`
		lastr=${lastr:1:5}
		if [ $yesterday -gt $lastr ]
		then
			modify=`svn diff $tempname -r $yesterday | grep "^ *+" | grep guid`
		else
			modify=`svn diff $tempname -r $lastr | grep "^ *+" | grep guid`
		fi		
		if [ ${#modify} -gt 5 ]
		then
			echo $tempname
			echo $modify
		fi
	fi
done

