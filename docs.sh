#!/bin/bash
cat << EOF > README.md
# Edward
* A small bot that utilizes praw and chatterbot to connect to multiple services
* chatterbot: https://github.com/gunthercox/ChatterBot
* PRAW: https://praw.readthedocs.io/en/latest/

## Dependencies
* python 3.5+
* Be sure to export envars first:
\`\`\`
export REDDIT_CLIENT_ID=
export REDDIT_CLIENT_SECRET=
export REDDIT_USERNAME=
export REDDIT_PASSWORD=
export TWITTER_KEY=
export TWITTER_SECRET=
export TWITTER_TOKEN=
export TWITTER_TOKEN_SECRET=
export HIPCHAT_HOST=
export HIPCHAT_ROOM=
export HIPCHAT_ACCESS_TOKEN=
export GITTER_ROOM=
export GITTER_API_TOKEN=
\`\`\`

EOF

# Generate TOC
echo '## TOC' >> README.md
echo '# Edward' | toc - >> README.md
echo '## Dependencies' | toc - >> README.md
echo '## Usage' | toc - >> README.md
echo '## Docker' | toc - >> README.md
echo '## Module defs' | toc - >> README.md
myopts edward.py | toc - >> README.md
echo '## TODO' | toc - >> README.md

# Generate Usage docs
echo '## Usage' >> README.md
echo '```' >> README.md
python edward.py --help >> README.md
echo '```' >> README.md

# Generate Docker docs
echo '## Docker' >> README.md
cat << EOF >> README.md
Build and test with docker-compose
\`\`\`
make test
\`\`\`

Build and deploy to docker swarm
\`\`\`
make deploy

docker stack services edward
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
i3laoiilqi76        edward_mongo        replicated          1/1                 mongo:latest        *:27017->27017/tcp
qyio6ac50xyt        edward_bot          replicated          1/1                 bot:latest
\`\`\`
EOF

# Generate Module defs docs
echo '## Module defs' >> README.md
myopts edward.py >> README.md

echo '## TODO' >> README.md
cat << EOF >> README.md
* Rate limiting fixes
  * https://github.com/SerpentAI/requests-respectful
* pytest
* stack overflow
EOF
