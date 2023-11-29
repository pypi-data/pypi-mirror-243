
## Reference
https://www.digitalocean.com/community/tutorials/how-to-use-vault-to-protect-sensitive-ansible-data
https://www.shellhacks.com/ansible-sudo-a-password-is-required/
https://github.com/priximmo
https://github.com/Pro-Tweaker/SEEDbox



docker compose  --env-file ./config/.env.prod -f docker-compose.yml --project-directory . up  --build --remove-orphans


curl --request PUT http://gext-02.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.48:51000
curl --request PUT http://gext-02.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.49:51000
curl --request PUT http://gext-02.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.60:51000
curl --request PUT http://gext-02.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.61:51000
curl --request PUT http://gext-02.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.62:51000

# CORR CLuster

curl --request PUT http://gext-core.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.49:51000
curl --request PUT http://gext-core.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.60:51000
curl --request PUT http://gext-core.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.61:51000
curl --request PUT http://gext-core.rms-asp.com:8500/v1/agent/service/deregister/marie-gateway@172.20.10.62:51000