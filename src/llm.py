# src/llm.py

import os
from openai import OpenAI

class LLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEVAGI_AI_API_KEY"),
            base_url=os.getenv("DEVAGI_AI_ENDPOINT")
        )

    def generate_daily_report(self, markdown_content, dry_run=False):
        system_role = """
        你是一位细致且富有洞察力的项目分析师。你擅长总结项目更新并根据功能对信息进行分类。
        当你收到项目更新日志时，你将：
            1. 识别并分组相似的功能、改进和错误修复。
            2. 生成一份简洁且信息丰富的简报，总结项目的进展。
            3. 将简报清晰地分为三个部分：
                - **新增功能**
                - **主要改进**
                - **修复问题**
            4. 确保简报易于理解，并提供项目当前状态的清晰概览。
        """
        # prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        prompt = f"""
        以下是项目的最新进展，根据功能合并同类项，形成一份简报:\n\n{markdown_content}
        使用中文生成简报
        """
        if dry_run:
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            return "DRY RUN"

        print("Before call GPT")
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ]
        )
        print("After call GPT")
        print(response)
        return response.choices[0].message.content
