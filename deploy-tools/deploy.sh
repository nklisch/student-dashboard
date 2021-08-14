 #!/bin/bash
 npm --prefix ../frontend run build
 cp ../frontend/build/* ../backend/html/
 docker-compose up -d --force-recreate --build