# Emoji Chat
Example project where an LLM can give emoji reactions based on input. You enter a sentance on a web page and the LLM will respond with emojis.


https://github.com/schedin/emoji-chat/blob/e79d620be435bcc1dff352101b4b76565e5a308f/emoji-chat.mov


## Deployment

Use helm to deploy the application to a Kubernetes cluster. For example:

```bash
helm upgrade --install emoji-chat ./charts/emoji-chat \
    --namespace emoji-chat --create-namespace
```
