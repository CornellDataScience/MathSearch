autopep8 --in-place --recursive .
flake8 -vv --output-file=lint_log.txt 
flake8
mv lint_log.txt ../logs