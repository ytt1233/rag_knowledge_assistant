from openai import OpenAI
from generator.base_generator import BaseGenerator


class DeepSeekGenerator(BaseGenerator):
    """
    Generator implementation based on DeepSeek API.
    """

    def __init__(
        self,
        model_name: str = "deepseek-chat",
        api_key: str = "sk-04577a9da3354fe193eea98f3472cf3f",
        base_url: str = "https://api.deepseek.com",
        temperature: float = 0.2
    ):
        """
        初始化 DeepSeek 生成器
        
        :param model_name: 模型名称，如 'deepseek-chat' 或 'deepseek-coder'
        :param api_key: DeepSeek API Key，建议通过环境变量获取
        :param base_url: API 基础地址，默认为官方地址
        :param temperature: 温度参数，控制随机性
        """
        self.model_name = model_name
        self.temperature = temperature
        
        # 如果未提供 api_key，尝试从环境变量获取
        if api_key is None:
            import os
            api_key = os.getenv("DEEPSEEK_API_KEY")
            
        if not api_key:
            raise ValueError("DeepSeek API Key is required. Set it via argument or DEEPSEEK_API_KEY environment variable.")

        # 初始化 OpenAI 兼容客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate an answer from the given prompt using DeepSeek API.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                # 可选：限制最大 token 数，防止过长响应
                # max_tokens=1024 
            )
            
            # 提取返回内容
            # OpenAI SDK 返回的对象结构中，内容位于 choices[0].message.content
            return response.choices[0].message.content
            
        except Exception as e:
            # 实际生产中建议更详细的错误处理
            raise RuntimeError(f"Failed to generate response from DeepSeek: {str(e)}")
