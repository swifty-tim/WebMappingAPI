for file in /$1/*; do
   if [ -d $file ]; then
    for subfile in $file/*; do
        if [[ $subfile == *.py ]]; then
            pylint $subfile
        fi
    done
    fi
    if [[ $file == *.py ]]; then
        pylint $file
    fi
done
