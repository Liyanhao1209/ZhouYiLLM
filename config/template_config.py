PROMPT_TEMPLATES = {
    # "mix_chat": """
    #     你是一个知无不言言无不尽的易学（周易）专家。先前我问了你一个易学方面的问题，你通过自身的能力、知识库检索的方式，给出了两个答案。另外，我通过询问智谱清言（一个在线大模型），得到了另外一个答案\n
    #     现在请你将这三个答案系统地整理成一篇针对原始问题的中文回答。\n
    #     请你直接了当地给出回答，请一定不要添加任何诸如:\n
    #     '根据您的要求，我将这两个答案系统地整理成一篇针对原始问题的中文回答。'、'好的，以下是xxx的回答’、'非常抱歉，我刚刚没有理解您的问题。'、'根据您的对话和我所掌握的资料，我为您整理了以下回答'等\n
    #     这样与实际答案无关紧要的话！\n
    #     此外，给出回答时，你一定不要重复原始问题！请务必记住，任何与答案正文无关的文本，均不要出现在回答中。\n
    #     原始问题:\n
    #     {question}\n
    #     你通过自身能力给出的解答如下:\n
    #     {answer1}\n
    #     你通过知识库检索给出的解答如下:\n
    #     {answer2}\n
    #     我通过在线大模型得到的解答如下:\n
    #     {answer3}\n
    #
    #     现在请你给出针对原始问题的中文回答。\n
    #     AI:
    # """
    "mix_chat": """
    你是一个知无不言言无不尽的易学（周易）专家。先前我问了你一个易学方面的问题，你通过自身的能力、知识库检索的方式，给出了两个答案。\n
    现在请你将这两个答案系统地整理成一篇针对原始问题的中文回答。并且尽可能多地融合这两个答案中在易学方面有价值的内容，使得答案尽可能饱满。\n
    请你直接了当地给出回答，请一定不要添加任何与实际答案无关紧要的话！\n
    此外，给出回答时，你一定不要重复原始问题！请务必记住，任何与答案正文无关的文本，均不要出现在回答中。再次强调一遍，你不需要跟我讲礼貌，请你按我说的，仅仅给出答案的正文！\n
    原始问题:\n
    {question}\n
    你通过自身能力给出的解答如下:\n
    {answer1}\n
    你通过知识库检索给出的解答如下:\n
    {answer2}\n

    现在请你给出针对原始问题的中文回答。\n
    AI:
        """,
    "online_llm_chat": """
    你是一个知无不言言无不尽的易学（周易）专家。现在我有一个易学方面的问题请你解答：\n
    {question}\n
    请你直接了当地给出回答，请一定不要添加任何与实际答案无关紧要的话！\n
    此外，给出回答时，你一定不要重复原始问题！请务必记住，任何与答案正文无关的文本，均不要出现在回答中。再次强调一遍，你不需要跟我讲礼貌，请你按我说的，仅仅给出答案的正文！\n
    
    现在请你给出针对原始问题的中文回答。\n
    AI:
        """
}


def get_mix_chat_prompt(question, history, answer1, answer2, answer3, template_name="mix_chat"):
    print(f'llm_chat:{answer1}\nkb_chat:{answer2}\nsearch_engine_chat:{answer3}')
    return PROMPT_TEMPLATES[template_name].format(question=question, history=history, answer1=answer1, answer2=answer2,
                                                  answer3=answer3)


def get_online_llm_chat_prompt(question,template_name="online_llm_chat"):
    return PROMPT_TEMPLATES[template_name].format(question=question)
