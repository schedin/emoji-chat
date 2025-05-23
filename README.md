# Emoji Chat
Example project where an LLM can give emoji reactions based on input. You enter a sentance on a web page and the LLM will respond with emojis.



https://github.com/user-attachments/assets/1516805b-a23d-48d2-bc6e-34588bd7e507



## Deployment

Use helm to deploy the application to a Kubernetes cluster. For example:

```bash
helm upgrade --install emoji-chat ./charts/emoji-chat \
    --namespace emoji-chat --create-namespace
```
