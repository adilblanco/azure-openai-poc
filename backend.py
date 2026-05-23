import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class AzureOpenAIBackend:

    def __init__(self, api_key, endpoint, deployment, temperature=1, max_tokens=1000, timeout=60, reasoning_effort=None):
        self.client = OpenAI(base_url=endpoint, api_key=api_key, timeout=timeout)
        self.deployment = deployment
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.reasoning_effort = reasoning_effort

    def predict(self, system_prompt, user_prompt, images=None):
        logger.info(f"Appel LLM: model={self.deployment}, max_tokens={self.max_tokens}, temperature={self.temperature}")

        content = [{"type": "text", "text": user_prompt}]

        if images:
            for img in images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{img['mime']};base64,{img['content']}"
                    },
                })
            logger.info(f"Images ajoutees au message: {len(images)} image(s)")

        extra = {}
        if self.reasoning_effort is not None:
            extra["reasoning_effort"] = self.reasoning_effort

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content},
            ],
            max_completion_tokens=self.max_tokens,
            response_format={"type": "json_object"},
            **extra,
        )

        content = response.choices[0].message.content or ""
        return json.loads(content)
