# 如何使用Self-QA脚本
运行本文件夹下的instruction_generation.py前，请务必运行java_scripts下的src\main\java\Scripts\GenerateWorkStation.java脚本，为指定的文件夹生成Workstation.txt文件，否则这个python脚本是不会运行成功的。
<br/><br/>
至于为什么要有这个Workstation.txt文件，请看blog：https://blog.csdn.net/lyh20021209/article/details/137696063?csdn_share_tail=%7B%22type%22%3A%22blog%22%2C%22rType%22%3A%22article%22%2C%22rId%22%3A%22137696063%22%2C%22source%22%3A%22lyh20021209%22%7D

4-20
补充完善了prompt
comparative_similarity.py使用如下：
已知有correct和updatePrompt两个json文件，将correct作为target文件，updatePrompt作为src文件，比较他们的相似度，然后将target文件中相似度低的加入到src文件中，最后输出到output_file文件中