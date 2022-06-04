#!/bin/bash
for i in `seq 0 9`; do curl http://localhost:80/ done

for i in {1..8}; do curl http://localhost:80/; done