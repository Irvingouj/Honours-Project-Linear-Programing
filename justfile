set shell := ["powershell.exe", "-c"]

test :
  python3 src/tester.py 

add:
  git add

commit target:
  git commit -m "{{target}}"

push target: add && commit
  git push