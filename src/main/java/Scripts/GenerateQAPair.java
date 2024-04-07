package Scripts;

import Reader.DocxReader.DocxReader;
import Reader.DocxReader.Rule.Interface.ReadRule;
import Reader.DocxReader.Rule.impl.SummaryPartRule;
import Reader.DocxReader.Rule.impl.VocabularyPartRule;
import Reader.DocxReader.SingletonDocxReader;
import Writer.XlsWriter.SingletonXlsWriter;
import Writer.XlsWriter.XlsWriter;

import java.util.*;

public class GenerateQAPair {
    static final ReadRule[] rules = new ReadRule[]{new SummaryPartRule("2"),new VocabularyPartRule()};

    static final String[][] concat = new String[][]{
            {"如何理解","怎么看待","什么是","如何解读"},
            {"的定义是什么","应该怎样理解","应该怎样解读"}
    };


    /**
     * word文档转换为QA对
     * @param args 0:规则 1:docx路径 2:xls目标路径 3:目标文件名
     */
    public static void main(String[] args) {
        String rule = args[0];
        String docxPath = args[1];
        String xlsPath = args[2];
        String xlsName = args[3];

        DocxReader reader = SingletonDocxReader.getDocxReader(rules[Integer.parseInt(rule)]);
        ArrayList<String> l = new ArrayList<>();
        reader.readDocSplits(docxPath, l);

        Map<String, List<String>> cols = generateQAPairs(l);
        XlsWriter writer = SingletonXlsWriter.getXlsWriter();
        writer.writeXls(cols,xlsPath,xlsName);
    }

    private static Map<String,List<String>> generateQAPairs(List<String> l){
        HashMap<String, List<String>> res = new HashMap<>();

        ArrayList<String> qs = new ArrayList<>();
        ArrayList<String> as = new ArrayList<>();

        Random random = new Random();

        for (int i = 0; i < l.size(); i++) {
            String text = l.get(i);
            if(i%2==0){
                int p = random.nextInt(concat.length);
                int q = random.nextInt(concat[p].length);
                if(p==0){
                    text = concat[p][q]+"\""+text+"\"";
                }else{
                    text = "\""+text+"\""+concat[p][q];
                }
                qs.add(text);
            }else{
                as.add(text);
            }
        }

        res.put("问题",qs);
        res.put("回答",as);

        return res;
    }
}
