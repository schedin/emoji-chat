# Emoji Chat
Example project where an LLM can give emoji reactions based on input. You enter a sentance on a web page and the LLM will respond with emojis.

[![emoji-chat video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://raw.githubusercontent.com/schedin/emoji-chat/refs/heads/main/emoji-chat.mp4)



## Deployment

Use helm to deploy the application to a Kubernetes cluster. For example:

```bash
helm upgrade --install emoji-chat ./charts/emoji-chat \
    --namespace emoji-chat --create-namespace
```
