# Emoji Chat
Example project where an LLM can give emoji reactions based on input. You enter a sentance on a web page and the LLM will respond with emojis.


https://raw.githubusercontent.com/schedin/emoji-chat/refs/heads/main/emoji-chat.mov


## Deployment

Use helm to deploy the application to a Kubernetes cluster. For example:

```bash
helm upgrade --install emoji-chat ./charts/emoji-chat \
    --namespace emoji-chat --create-namespace
```
