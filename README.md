# External skill template

Скилл купи слона
https://vk.com/dev/marusia_skill_docs

#### Install:

make install

#### Run:

make run

#### Tests:

make test

#### flake, mypy:

make flake
make mypy

#### Query:

curl -H "Content-Type: application/json" --data @body.json http://localhost:8000

#### Metrics:

http://localhost:8000/metrics

#### Probes:
http://localhost:8000/readiness_probe
http://localhost:8000/liveness_probe
http://localhost:8000/readiness_probe

