# Emoji Chat
Example project where an LLM can give emoji reactions based on input. You enter a sentance on a web page and the LLM will respond with emojis.

## Deployment

Use helm to deploy the application to a Kubernetes cluster. For example:

```bash
helm upgrade --install emoji-chat ./charts/emoji-react \
    --namespace emoji-react --create-namespace
```
