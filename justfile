set shell := ["powershell.exe", "-c"]

test :
  python3 src/tester.py 

add:
  git add

commit target:
  git commit -m "{{target}}"

push target:
  git push

freeze:
  pip freeze > requirements.txt