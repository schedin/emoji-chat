# Emoji Chat
Example project where an LLM can give emoji reactions based on input. You enter a sentance on a web page and the LLM will respond with emojis.
If you are unlucky the crazy and slightly indeterministic moderation filter (also LLM based) will reject your message. You can turn the moderation off using the checkbox.



https://github.com/user-attachments/assets/1516805b-a23d-48d2-bc6e-34588bd7e507



## Deployment

Use helm to deploy the application to a Kubernetes cluster. For example:

```bash
helm upgrade --install emoji-chat ./charts/emoji-chat \
    --namespace emoji-chat --create-namespace
```
