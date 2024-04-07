package Scripts;

import Reader.DocxReader.DocxReader;
import Reader.DocxReader.Rule.Interface.ReadRule;
import Reader.DocxReader.Rule.impl.SummaryPartRule;
import Reader.DocxReader.SingletonDocxReader;
import Writer.XlsWriter.SingletonXlsWriter;
import Writer.XlsWriter.XlsWriter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GenerateQAPair {
    static final ReadRule[] rules = new ReadRule[]{new SummaryPartRule("2"),new SummaryPartRule("2")};

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
        List<String> l = reader.readDoc(docxPath);

        Map<String, List<String>> cols = generateQAPairs(l);
        XlsWriter writer = SingletonXlsWriter.getXlsWriter();
        writer.writeXls(cols,xlsPath,xlsName);
    }

    private static Map<String,List<String>> generateQAPairs(List<String> l){
        HashMap<String, List<String>> res = new HashMap<>();

        ArrayList<String> qs = new ArrayList<>();
        ArrayList<String> as = new ArrayList<>();

        for (int i = 0; i < l.size(); i++) {
            if(i%2==0){
                qs.add(l.get(i));
            }else{
                as.add(l.get(i));
            }
        }

        res.put("问题",qs);
        res.put("回答",as);

        return res;
    }
}
